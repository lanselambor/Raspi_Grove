from wiringpi2 import *
import time

dev_1 = 0x68


wiringPiSetup()

#instant a object
i2c = I2C()
print 'instance done' 

fd_1 = i2c.setup(0x68)
print 'device addr done'

while True:
    time.sleep(0.5)
    wiringPiI2CWrite(fd_1,0x20)
    wiringPiI2CWrite(fd_1,0x20)
    wiringPiI2CWrite(fd_1,0x20)
    print 'Write done'


