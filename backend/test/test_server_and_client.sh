#!/bin/bash
set -e

echo "Starting irrigation server..."
# Create log file with timestamp
LOG_FILE="/tmp/irrigator_server_$(date +%Y%m%d_%H%M%S).log"
echo "Server output will be logged to: $LOG_FILE"

# Use a wrapper script to capture only Python output
WRAPPER_SCRIPT="/tmp/run_server_$(date +%Y%m%d_%H%M%S).sh"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
exec bazel run //backend:start 2>&1 | grep -v "^INFO:\|^DEBUG:\|^WARNING:\|Loading:\|Analyzing:\|Building:\|Running:\|^$"
EOF
chmod +x "$WRAPPER_SCRIPT"

# Run the wrapper script with output redirection
"$WRAPPER_SCRIPT" >"$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Give server time to start up
echo "Waiting for server to start..."
sleep 5

# Function to find the actual Python server process
find_server_pid() {
    ps aux | grep "start.runfiles" | grep -v grep | awk '{print $2}' | head -1
}

# Function to cleanup on exit
cleanup() {
    echo "Cleaning up server process..."
    
    # Find the actual server process PID
    ACTUAL_SERVER_PID=$(find_server_pid)
    
    if [ -n "$ACTUAL_SERVER_PID" ]; then
        echo "Found server process (PID: $ACTUAL_SERVER_PID)..."
        # Try graceful shutdown first
        kill -TERM "$ACTUAL_SERVER_PID" 2>/dev/null || true
        
        # Wait up to 5 seconds for graceful shutdown
        for i in {1..5}; do
            if ! kill -0 "$ACTUAL_SERVER_PID" 2>/dev/null; then
                echo "Server stopped gracefully."
                break
            fi
            sleep 1
        done
        
        # Check if still running and force kill
        if kill -0 "$ACTUAL_SERVER_PID" 2>/dev/null; then
            echo "Force killing server..."
            kill -KILL "$ACTUAL_SERVER_PID" 2>/dev/null || true
            echo "Server force stopped."
        fi
    else
        echo "No server process found."
    fi
    
    # Also cleanup the bazel wrapper process if still running
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "Cleaning up bazel wrapper process..."
        kill -TERM "$SERVER_PID" 2>/dev/null || true
        sleep 1
        kill -KILL "$SERVER_PID" 2>/dev/null || true
    fi
    
    # Show log file location and recent errors if any
    echo "Server output logged to: $LOG_FILE"
    if [ -f "$LOG_FILE" ] && grep -q -i "error\|exception\|critical" "$LOG_FILE"; then
        echo "⚠️  Errors found in server log. Last few error lines:"
        grep -i "error\|exception\|critical" "$LOG_FILE" | tail -3
    fi
    
    # Cleanup wrapper script
    if [ -f "$WRAPPER_SCRIPT" ]; then
        rm -f "$WRAPPER_SCRIPT"
    fi
}

# Set trap to cleanup on script exit (success, failure, or interrupt)
trap cleanup EXIT INT TERM

# Wait a bit more and check if actual server process is running
ACTUAL_SERVER_PID=$(find_server_pid)
if [ -z "$ACTUAL_SERVER_PID" ]; then
    echo "Server failed to start - no process found with 'start.runfiles'"
    echo "Check server log for errors: $LOG_FILE"
    if [ -f "$LOG_FILE" ]; then
        echo "Last few lines from server log:"
        tail -10 "$LOG_FILE"
    fi
    exit 1
fi

echo "Server started successfully (PID: $ACTUAL_SERVER_PID)."
echo ""
echo "Choose test mode:"
echo "  1) Automatic test (runs test_rpc_client and exits)"
echo "  2) Interactive client (allows manual testing)"
echo ""
read -p "Enter choice (1 or 2): " CHOICE

case $CHOICE in
    1)
        echo "Running automatic RPC client test..."
        # Run the test client and capture exit code
        TEST_EXIT_CODE=0
        bazel run //backend/test:test_rpc_client || TEST_EXIT_CODE=$?

        # Report results
        if [ $TEST_EXIT_CODE -eq 0 ]; then
            echo "✓ RPC test completed successfully!"
            echo "✓ Cleaning up server..."
        else
            echo "✗ RPC test failed with exit code $TEST_EXIT_CODE"
            echo "✓ Cleaning up server..."
        fi

        # cleanup() will be called automatically due to EXIT trap
        exit $TEST_EXIT_CODE
        ;;
    2)
        echo "Starting interactive RPC client..."
        echo "The server will remain running until you exit the interactive client."
        echo "Use 'quit()' or Ctrl+C to exit and cleanup."
        
        # Run interactive client
        bazel run //backend/test:interactive_rpc_client
        
        echo "✓ Interactive session ended. Cleaning up server..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Please enter 1 or 2."
        echo "✓ Cleaning up server..."
        exit 1
        ;;
esac