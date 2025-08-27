#!/usr/bin/env python3
"""
Interactive RPC client for manual testing
"""

import rpyc


def interactive_client():
    try:
        print("Connecting to irrigation RPC service...")
        conn = rpyc.connect("localhost", 18871)
        print("Connected! Available commands:")
        print("  status() - Check if service is running")
        print("  start() - Start the executor")
        print("  zones() - List all zones")
        print("  zone(id) - Get detailed zone info")
        print("  open(id) - Open zone by ID")
        print("  close(id) - Close zone by ID")
        print("  stop() - Stop the service")
        print("  quit() - Exit client")

        def status():
            return conn.root.AmIRunning()

        def start():
            print("Starting executor...")
            return conn.root.start()

        def zones():
            zones = conn.root.GetIrrigators()
            for i, zone in enumerate(zones):
                print(
                    f"Zone {i}: {zone.name} (Pin: {zone.gpio_pin}, Open: {zone.IsOpen()})"
                )
            return zones

        def zone(zone_id):
            return conn.root.GetZoneInfo(zone_id)

        def open_zone(zone_id):
            print(f"Opening zone {zone_id}...")
            return conn.root.OpenZone(zone_id)

        def close_zone(zone_id):
            print(f"Closing zone {zone_id}...")
            return conn.root.CloseZone(zone_id)

        def stop():
            print("Stopping service...")
            return conn.root.stop()

        # Make functions available in interactive mode

        while True:
            try:
                cmd = input("\nrpc> ").strip()
                if not cmd:
                    continue

                if cmd == "quit()":
                    break
                elif cmd == "status()":
                    print(status())
                elif cmd == "start()":
                    start()
                elif cmd == "zones()":
                    zones()
                elif cmd.startswith("zone(") and cmd.endswith(")"):
                    zone_id = int(cmd[5:-1])
                    info = zone(zone_id)
                    print(
                        f"Zone {zone_id}: {info.name} - Open: {info.IsOpen()}, Override: {info.IsOverride()}"
                    )
                elif cmd.startswith("open(") and cmd.endswith(")"):
                    zone_id = int(cmd[5:-1])
                    open_zone(zone_id)
                elif cmd.startswith("close(") and cmd.endswith(")"):
                    zone_id = int(cmd[6:-1])
                    close_zone(zone_id)
                elif cmd == "stop()":
                    stop()
                else:
                    print(
                        "Unknown command. Try: status(), start(), zones(), zone(0), open(0), close(0), stop(), quit()"
                    )

            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

        conn.close()
        print("Disconnected.")

    except Exception as e:
        print(f"Connection failed: {e}")


if __name__ == "__main__":
    interactive_client()
