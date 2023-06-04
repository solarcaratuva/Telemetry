import subprocess

def set_system_time(epoch_seconds):
    subprocess.run(["sudo", "date", "-s", f"@{epoch_seconds}"])

if __name__ == "__main__":
    set_system_time(10000000)