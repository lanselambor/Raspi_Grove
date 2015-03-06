
apt-get update
#sudo apt-get upgrade

install tools
apt-get install python-pip
apt-get install python-setuptools
apt-get install python-dev
easy_install -U distribute
pip install RPi.GPIO
apt-get install i2c-tools python-smbus


#Install i2c module
echo "adding \"i2c-bcm2708 i2c-dev\" to /etc/modules\n"
chmod 666 /etc/modules

echo "i2c-bcm2708\ni2c-dev" >> /etc/modules
chmod 644 /etc/modules
cat /etc/modules


#reboot the systerm and check if i2c module install successfully
#i2cdetect -y -a 1
