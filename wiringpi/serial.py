import wiringpi
import time

serial=wiringpi.Serial('/dev/ttyAMA0', 9600)
while(True):
    time.sleep(0.5)
    serial.printf("hello")
    serial.printf('byebye')
