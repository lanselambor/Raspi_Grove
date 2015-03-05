import wiringpi

wiringpi.wiringPiSetup()

while(True):
    wiringpi.pwmWrite(1, 100)
    wiringpi.delay(10)
