import wiringpi

OUTPUT=1
PIN_TO_PWM=1

wiringpi.wiringPiSetup()
wiringpi.softPwmCreate(1,0,100) #counting 100 ms

while(True):
    wiringpi.softPwmWrite(1,50) #50ms high level pulses
    wiringpi.delay(100)
