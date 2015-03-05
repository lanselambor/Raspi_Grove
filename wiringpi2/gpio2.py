import wiringpi2
import time

PIN_OUT = 1

wiringpi2.wiringPiSetup()
io=wiringpi2.GPIO()
io.pinMode(PIN_OUT, io.OUTPUT)

while(True):
    io.digitalWrite(PIN_OUT, io.HIGH)
    #wiringpi2.digitalWrite(PIN_OUT,1)
    #time.sleep(0.5)
    #wiringpi2.digitalWrite(PIN_OUT,0)
    io.digitalWrite(PIN_OUT, io.LOW)
    #time.sleep(0.5)
