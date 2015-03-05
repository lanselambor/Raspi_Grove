import wiringpi
import time

PIN_OUT = 1
wiringpi.wiringPiSetup()
wiringpi.pinMode(PIN_OUT,1)

while(True):
    wiringpi.digitalWrite(PIN_OUT,1)
    #time.sleep(0.5)
    wiringpi.digitalWrite(PIN_OUT,0)
    #time.sleep(0.5)
