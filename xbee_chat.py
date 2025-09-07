#!/usr/bin/env python3
import argparse, sys, threading, time
import serial

PORT = "COM6"
BAUD = 9600

def receiver(ser, stop_flag):
    buf = bytearray()
    while not stop_flag["stop"]:
        chunk = ser.read(1024)  # non-blocking due to timeout
        if chunk:
            buf.extend(chunk)
            while b"\n" in buf:
                line, _, buf = buf.partition(b"\n")
                msg = line.decode("utf-8", errors="replace").rstrip("\r")
                # Print incoming on its own line, restore prompt
                sys.stdout.write(f"\n<REMOTE> {msg}\n> ")
                sys.stdout.flush()
        else:
            time.sleep(0.02)

def main():
    p = argparse.ArgumentParser(description="XBee transparent-mode chat")
    p.add_argument("--name", default="Me", help="Name prefix for your messages")
    args = p.parse_args()

    ser = serial.Serial(PORT, BAUD, timeout=0.05)
    stop_flag = {"stop": False}

    t = threading.Thread(target=receiver, args=(ser, stop_flag), daemon=True)
    t.start()

    try:
        print("Connected. Type messages and press Enter to send. Ctrl+C to quit.")
        sys.stdout.write("> "); sys.stdout.flush()
        while True:
            try:
                text = input()
            except EOFError:
                break
            out = f"{args.name}: {text}\n"
            ser.write(out.encode("utf-8"))
            ser.flush()
            sys.stdout.write("> "); sys.stdout.flush()
    except KeyboardInterrupt:
        pass
    finally:
        stop_flag["stop"] = True
        t.join(timeout=0.5)
        ser.close()

if __name__ == "__main__":
    main()