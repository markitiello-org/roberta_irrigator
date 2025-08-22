#!/usr/bin/env python3
"""
Simple RPC client to test irrigation system communication
"""
import rpyc
import sys

def test_rpc_connection():
    try:
        print("Connecting to irrigation RPC service on localhost:18871...")
        conn = rpyc.connect("localhost", 18871)
        
        print("✓ Connection established")
        
        # Test health check
        print("\n--- Health Check ---")
        is_running = conn.root.AmIRunning()
        print(f"Service running: {is_running}")
        
        # Get all irrigators/zones
        print("\n--- Zone Information ---")
        zones = conn.root.GetIrrigators()
        print(f"Found {len(zones)} zones:")
        for i, zone in enumerate(zones):
            print(f"  Zone {i}: {zone.name} (GPIO pin: {zone.gpio_pin}, Open: {zone.IsOpen()})")
        
        # Test individual zone info
        if zones:
            print(f"\n--- Detailed Zone 0 Info ---")
            zone_info = conn.root.GetZoneInfo(0)
            print(f"Name: {zone_info.name}")
            print(f"GPIO Pin: {zone_info.gpio_pin}")
            print(f"Is Open: {zone_info.IsOpen()}")
            print(f"Is Override: {zone_info.IsOverride()}")
        
        # Manual control test (commented out for safety)
        # print("\n--- Manual Control Test ---")
        # print("Opening zone 0 for 3 seconds...")
        # conn.root.OpenZone(0)
        # time.sleep(3)
        # conn.root.CloseZone(0)
        # print("Zone 0 closed")
        
        conn.close()
        print("\n✓ All tests passed!")
        return True
        
    except ConnectionRefusedError:
        print("✗ Connection refused - is the service running?")
        print("Start with: bazel run //backend:start")
        return False
    except Exception as e:
        print(f"✗ RPC test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_rpc_connection()
    sys.exit(0 if success else 1)