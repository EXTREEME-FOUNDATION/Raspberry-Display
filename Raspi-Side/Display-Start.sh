sudo systemctl stop getty@tty1.service
sudo systemctl daemon-reload
sudo cat /home/pi/Programmz/Test/tpn.tm > /dev/tty1

cd /home/pi/Programmz/Test
sudo python3 App.py
