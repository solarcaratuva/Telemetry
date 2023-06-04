import subprocess
import datetime

def set_system_time(epoch_seconds):
    # Convert the epoch time to a datetime object
    # dt = datetime.datetime.fromtimestamp(epoch_seconds)

    # Format the date and time in the format expected by the date command
    # date_str = dt.strftime('%y%m%d%H%M.%S')
    # Call the date command to set the system time
    # This must be run with sudo permissions
    subprocess.call(["sudo", "date", "-s", f"'@{epoch_seconds}'"])

if __name__ == "__main__":
    set_system_time(1000)