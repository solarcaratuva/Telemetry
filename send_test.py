import sys
import time

DEBUG_FILE = "debug_log.txt"

def log(msg):
    # Print to terminal (USB serial)
    try:
        print(msg)
    except Exception:
        pass

    # Also log to file so we know it ran
    try:
        with open(DEBUG_FILE, "a") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def main():
    log("[BOOT] XBee TX test starting")

    counter = 0

    while True:
        msg = "[XBEE TX] hello {}".format(counter)

        log(msg)

        # ALSO write directly to stdout (extra safe)
        try:
            sys.stdout.write(msg + "\r\n")
        except Exception:
            pass

        counter += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
