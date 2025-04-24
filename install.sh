#!/bin/bash

rebuild_env_file() {
    # Ask for ip address, login, password and save them to .env file
    echo "Please enter the IP address of the MQTT broker:"
    read -r ip_address
    echo "Please enter the login for the MQTT broker:"
    read -r login
    echo "Please enter the password for the MQTT broker:"
    read -r password

    # Create .env file
    echo "Creating .env file..."
    {
    echo "MQTT_BROKER_IP=$ip_address"
    echo "MQTT_BROKER_LOGIN=$login"
    echo "MQTT_BROKER_PASSWORD=$password"
    } > .env
    echo ".env file created successfully."
}

# Check if .env file already exists
if [ -f .env ]; then
    echo ".env file already exists. Do you want to overwrite it? (y/n)"
    read -r overwrite
    if [ "$overwrite" == "y" ]; then
        rebuild_env_file
    fi
else
    rebuild_env_file
fi



# Install dependencies
echo "Installing dependencies..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "Registering systemd service..."

INSTALL_DIR="$(pwd)"
sed "s|{{INSTALL_DIR}}|$INSTALL_DIR|g" mqttsensor.service.template > mqttsensor.service

cp mqttsensor.service /etc/systemd/system/mqttsensor.service
cp mqttsensor.timer /etc/systemd/system/mqttsensor.timer

systemctl daemon-reload
systemctl enable mqttsensor.service
sudo systemctl enable mqttsensor.timer
sudo systemctl start mqttsensor.timer

echo "Service installed and started successfully."
echo "To check the status of the service, use: systemctl status mqttsensor.service"
echo "To view logs, use: journalctl -u mqttsensor.service -f"
# echo "systemctl list-timers"