import wiringpi2

OUTPUT=1
PIN_TO_PWM=1

wiringpi2.wiringPiSetup()
wiringpi2.softPwmCreate(1,0,10) #counting 100 ms

while(True):
    wiringpi2.softPwmWrite(1,1) #50ms high level pulses
    wiringpi2.delay(100)
