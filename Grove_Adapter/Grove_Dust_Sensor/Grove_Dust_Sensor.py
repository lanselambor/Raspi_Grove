import wiringpi2
import time
import math

wiringpi2.wiringPiSetup()

class Dust_Sensor():
    def __init__(self, inputPin):
	self.duration = 0
	self.lowpulseoccupancy = long()
        self.highpulseoccupancy = long() 
	self.sampletime_ms = 3000  #30s
	self.time1 = wiringpi2.millis()  # ms
	self.time2 = wiringpi2.millis()  # ms
	self.ratio = float()
	self.concentration = 0 
	self.flag = False
	self.input = inputPin # pin 0 input
        
	wiringpi2.pinMode(self.input, 0)

    # parameter duration(seconds) of once read
    def read(self, seconds):
        self.ratio = 0.0
        self.concentration = 0.0
        self.lowpulseoccupancy = 0
        self.highpulseoccupancy = 0

        v_state = 0
        second = time.time()

        while time.time() - second <= seconds:
            while 1 == wiringpi2.digitalRead(self.input):
                self.lowpulseoccupancy += 1
                wiringpi2.delayMicroseconds(1)
            while 0 == wiringpi2.digitalRead(self.input):
                self.highpulseoccupancy += 1
                wiringpi2.delayMicroseconds(1)
        print 'duration ', time.time() - second, 's '   
        print 'self.highpulseoccupancy ', self.highpulseoccupancy, 'us'  
	print 'self.lowpulseoccupancy ', self.lowpulseoccupancy, 'us' 
        if 0 != self.lowpulseoccupancy:
	    self.ratio = self.lowpulseoccupancy * 100.0 / (self.lowpulseoccupancy + self.highpulseoccupancy)
	    #self.concentration = 1.1* math.pow(self.ratio, 3) - 3.8*pow(self.ratio, 2) + 520 * self.ratio + 0.62  #using spec curve
	    return self.ratio #, self.concentration

if __name__=="__main__":
    dust = Dust_Sensor(0)
    while True:
       ratio =  0
       ratio = dust.read(5)
       print 'ratio = ',ratio 
        
