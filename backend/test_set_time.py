import subprocess
import datetime

def set_system_time(epoch_seconds):
    # Convert the epoch time to a datetime object
    dt = datetime.datetime.fromtimestamp(epoch_seconds)

    # Format the date and time in the format expected by the date command
    # date_str = dt.strftime('%m%d%H%M%Y.%S')

    # Call the date command to set the system time
    # This must be run with sudo permissions
    subprocess.call(["date", f"""\"$(date -r {epoch_seconds} +'%y%m%d%H%M.%S')\""""])

if __name__ == "__main__":
    set_system_time(1000)