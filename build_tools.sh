#!/bin/bash
echo 'Installing...'
apt-get update

#install tools
apt-get install i2c-tools python-smbus python-pip python-setuptools python-dev
pip install RPi.GPIO
easy_install -U distribute

if grep -q "i2c-dev" /etc/modules; then
	echo "I2C-dev already there"
else
	echo i2c-dev >> /etc/modules
	echo "I2C-dev added"
fi
if grep -q "i2c-bcm2708" /etc/modules; then
	echo "i2c-bcm2708 already there"
else
	echo i2c-bcm2708 >> /etc/modules
	echo "i2c-bcm2708 added"
fi

#reboot the systerm and check if i2c module install successfully
#i2cdetect -y -a 1
