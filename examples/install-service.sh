#!/bin/bash
SERVICE_PATH=/etc/systemd/system/pimoroni-trackball.service

read -r -d '' UNIT_FILE << EOF
[Unit]
Description=Track Ball Service
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/evdev-mouse.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "Installing udev rule"
sudo cp 10-trackball.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules

echo "Installing evdev"
sudo apt install python-evdev

echo "Installing Track Ball library"
cd ../library
sudo python setup.py install
cd ../examples

echo "Installing service to: $SERVICE_PATH"
echo "$UNIT_FILE" > $SERVICE_PATH
systemctl daemon-reload
systemctl enable pimoroni-trackball.service
systemctl start pimoroni-trackball.service
systemctl status pimoroni-trackball.service
