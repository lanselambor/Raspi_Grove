import wiringpi2
import time

PIN_OUT = 1
wiringpi2.wiringPiSetup()
wiringpi2.pinMode(PIN_OUT,1)

while(True):
    wiringpi2.digitalWrite(PIN_OUT,1)
    #time.sleep(0.5)
    wiringpi2.digitalWrite(PIN_OUT,0)
    #time.sleep(0.5)
