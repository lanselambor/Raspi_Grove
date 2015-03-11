import wiringpi2

wiringpi2.wiringPiSetup()

# how many timing transitions we need to keep track of. 2 * number bits + extra

MAXTIMINGS = 85

DHT11 = 11
DHT22 = 22
DHT21 = 21
AM2301 = 21

# input pin
#pin  = 0
#count = 15

class DHT():
    def __init__(self, pin, count):        
        self._pin = pin
        self._count = count
        self.firstreading = True
        self._lastreadtime = long()
        self.data = [0 for i in range(6)]
    
    def begin(self):
        wiringpi2.pinMode(self._pin, 0)
        wiringpi2.digitalWrite(self._pin, 1)        
        
    def readTemperature(self):
        pass
        
    def convertCtoF(self, c):
        return float(c * 9 /5 +32)
    
    def readHumidity(self):
        pass
        
    def read(self):
        laststate, counter, j, i = 1, 0, 0, 0  
        currenttime = long()
        
        # pull the pin high and wait 250 milliseconds
        wiringpi2.digitalWrite(self._pin, 1)
        wiringpi2.delay(250)
        
        currenttime = wiringpi2.millis()
        if currenttime < self._lastreadtime:
            # ie there was a rollover
            self._currenttime = 0
        
        if False == self.firstreading and currenttime - self._lastreadtime < 2000:
            return True  # return last correct measure
            
        self.firstreading = False
        self._lastreadtime = wiringpi2.millis()
        print 'lastreadtime: ', self._lastreadtime, 'ms'
        
        data = [0 for i in range(6)]
        
        # now pull it low for ~20 milliseconds
        wiringpi2.pinMode(self._pin, 1)
        wiringpi2.digitalWrite(self._pin, 0)
        wiringpi2.delay(1)
        wiringpi2.digitalWrite(self._pin, 1)
        wiringpi2.delayMicroseconds(20)
        wiringpi2.pinMode(self._pin, 0)
        
        # read for timmings
        for i in range(85):
            counter = 0
            time1 = wiringpi2.micros()
            while laststate == wiringpi2.digitalRead(self._pin):
                counter += 1
#                print 'counter: ', counter, 'us'
                wiringpi2.delayMicroseconds(1)
                if counter == 255:
                    break
            print 'duration', wiringpi2.micros() - time1, 'us', 'counter has ', counter, ' times'
            laststate = wiringpi2.digitalRead(self._pin)
            print 'laststate is ', laststate
            if counter == 255:
                break
            if i >= 4 and i%2 == 0:
                data[j/8] <<= 1
                if counter > self._count:
                    data[j/8] |= 1
                j += 1
            
        if j >= 40 and data[4] == (data[0]+data[1]+data[2]+data[3]) & 0xFF :
            return True
        print data

        return False
            
    def test(self):
        time1 = wiringpi2.micros()
        duration = wiringpi2.micros() - time1
        print 'one cmd duration ',duration,  'us'
        wiringpi2.delay(1000)
            
if __name__=="__main__":
    dht = DHT(0, 60)
    wiringpi2.delay(2000) 
    dht.begin()
    while True:
        dht.test()
        dht.read()
        
            
