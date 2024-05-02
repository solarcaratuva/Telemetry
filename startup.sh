#!/bin/bash
export DISPLAY=:0
sleep 5
/usr/local/bin/serve -l 12345 -s /home/cwise/solar/TelemetryBuild/frontend/build &
chromium-browser --app=http://localhost:12345 --start-fullscreen &
sleep 10
/home/cwise/backend.sh &
/usr/bin/unclutter -idle 0

# lxterminal --command "bash -c 'python /home/solarcar/Telemetry/backend/serial_logger.py; exec bash'"