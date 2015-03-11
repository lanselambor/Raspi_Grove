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
	self.ratio = 0
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

#        print 'second = ',second, ' s'
        while time.time() - second <= seconds:
            if 0 == wiringpi2.digitalRead(self.input):
                pass
            else:
                v_state = 1

            while v_state == wiringpi2.digitalRead(self.input):
                self.lowpulseoccupancy += 1
                wiringpi2.delay(1)
            while v_state != wiringpi2.digitalRead(self.input):
                self.highpulseoccupancy += 1
                wiringpi2.delay(1)
        print 'self.highpulseoccupancy ', self.highpulseoccupancy, 'ms' 
	print 'self.lowpulseoccupancy ', self.lowpulseoccupancy, 'ms' 
        if 0 != self.lowpulseoccupancy:
	    self.ratio = self.lowpulseoccupancy * 100.0 / (self.lowpulseoccupancy + self.highpulseoccupancy)
	    #self.concentration = 1.1* math.pow(self.ratio, 3) - 3.8*pow(self.ratio, 2) + 520 * self.ratio + 0.62  #using spec curve
	    return self.ratio #, self.concentration


#	if (0 == wiringpi2.digitalRead(input)): 
#	    self.flag = True
#	    while 0 == wiringpi2.digitalRead(input):
#                pass
#
#
#	if self.flag:
#	    self.duration = wiringpi2.millis() - self.time1
#	    self.time1 = wiringpi2.millis()
#	    self.lowpulseoccupancy += self.duration
#	    
#	    if wiringpi2.millis() - self.time2 >= self.sampletime_ms:
#		self.ratio = self.lowpulseoccupancy * 1.0 / self.sampletime_ms   # integer percentage 0~100
#		self.concentration = 1.1* math.pow(self.ratio, 3) - 3.8*pow(self.ratio, 2) + 520 * self.ratio + 0.62  #using spec curve
#		print self.lowpulseoccupancy,  self.ratio,  self.concentration
#		self.lowpulseoccupancy = 0
#		self.time2 = wiringpi2.millis()
#	    self.flag = False

if __name__=="__main__":
    dust = Dust_Sensor(0)
    while True:
       ratio =  0
       ratio = dust.read(5)
       print 'ratio = ',ratio 
        
