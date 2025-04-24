#!/bin/bash
# Stop and remove systemd service
echo "Stopping and disabling systemd service..."

systemctl stop mqttsensor.timer

systemctl disable mqttsensor.service
systemctl disable mqttsensor.timer

rm /etc/systemd/system/mqttsensor.service
rm /etc/systemd/system/mqttsensor.timer

systemctl daemon-reload

echo "Systemd mqttsensor service stopped and removed successfully."
