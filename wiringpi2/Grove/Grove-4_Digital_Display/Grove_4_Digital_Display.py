import wiringpi2
import time
import sys

wiringpi2.wiringPiSetup()

#OW = 0


class TM1637():
    def __init__(self, Clk, Data):
	self.TubeTab = [0x3f,0x06,0x5b,0x4f,\
		    0x66,0x6d,0x7d,0x07,\
		    0x7f,0x6f,0x77,0x7c,\
		    0x39,0x5e,0x79,0x71]
	self.Cmd_SetData = 0
	self.Cmd_SetAddr = 0
	self.Cmd_DispCtrl = 0
	# definitions for TM1637
	self.ADDR_AUTO = 0x40
	self.ADDR_FIXED = 0x44
	self.STARTADDR = 0xc0
	# definitions for the clock point of the digit tube
	self.POINT_ON = 1
	self.POINT_OFF = 0
	# definitions for brightness
	self.BRIGHT_DARKEST = 0
	self.BRIGHT_TYPICAL = 2
	self.BRIGHTEST = 7

	self._PointFlag = False # _PointFlag=1:the clock point on

	self.Clkpin = Clk
	self.Datapin = Data
	wiringpi2.pinMode(self.Clkpin, 1)
	wiringpi2.pinMode(self.Datapin, 1 )

        self.clearDisplay()

    def writeByte(self, wr_data):  
        for i in range(0, 8):
            wiringpi2.digitalWrite(self.Clkpin, 0)
            if 0 != wr_data & 0x01:
                wiringpi2.digitalWrite(self.Datapin, 1)
            else:
              wiringpi2.digitalWrite(self.Datapin, 0)
            wr_data >>= 1
            wiringpi2.digitalWrite(self.Clkpin, 1)
        wiringpi2.digitalWrite(self.Clkpin, 0)
        wiringpi2.digitalWrite(self.Datapin, 1)
        wiringpi2.digitalWrite(self.Clkpin, 1)
        wiringpi2.pinMode(self.Datapin, 0)

        count = 0
        while 1 == wiringpi2.digitalRead(self.Datapin):
           count += 1    
           if(count == 200):
              wiringpi2.pinMode(self.Datapin, 1)
              wiringpi2.digitalWrite(self.Datapin, 0)
              count = 0
           wiringpi2.pinMode(self.Datapin, 0)
        wiringpi2.pinMode(self.Datapin, 1)

    def start(self):
        wiringpi2.digitalWrite(self.Clkpin, 1)
        wiringpi2.digitalWrite(self.Datapin, 1)
        wiringpi2.digitalWrite(self.Clkpin, 0)
        wiringpi2.digitalWrite(self.Datapin, 0)

    def stop(self):
        wiringpi2.digitalWrite(self.Clkpin, 0)
        wiringpi2.digitalWrite(self.Datapin, 0)
        wiringpi2.digitalWrite(self.Clkpin, 1)
        wiringpi2.digitalWrite(self.Datapin, 1)

#    def display(self, DispData):
#        #print 'display'
#        SegData = [0, 0, 0, 0]
#        for i in range(0, 4):
#           SegData[i] = DispData[i]
#        self.coding(SegData)
#        self.start()
#        self.writeByte(ADDR_AUTO)
#        self.stop()
#        self.start()
#        self.writeByte(self.Cmd_SetAddr)
#        for i in range(0, 4):
#            self.writeByte(SegData[i])
#        self.stop()
#        self.start()
#        self.writeByte(self.Cmd_DispCtrl)
#        self.stop()

    def display(self, BitAddr, DispData):
        SegData = self.coding(DispData)
        self.start()
        self.writeByte(self.ADDR_FIXED) 
        self.stop()
        self.start()
        self.writeByte(BitAddr | 0xc0)
        self.writeByte(SegData)
        self.stop()
        self.start()
        self.writeByte(self.Cmd_DispCtrl) 
        self.stop()

    def clearDisplay(self):
        self.display(0x00, 0x7f)
        self.display(0x01, 0x7f)
        self.display(0x02, 0x7f)
        self.display(0x03, 0x7f)

    def set(self, brightness, SetData, SetAddr):
        self.Cmd_SetData = SetData
        self.Cmd_SetAddr = SetAddr
        self.Cmd_DispCtrl = 0x88 + brightness # Set the brightness and it takes effect the next time it displays.

    def point(self, PointFlag):
        self._PointFlag = PointFlag

#    def coding(self, DispData):
#        #print 'coding'
#        PointData = 0
#        if(self._PointFlag == POINT_ON):
#            PointData = 0x80
#        else:
#            PointData = 0
#        for i in range(0, 4):
#            if(DispData[i] == 0x7f):
#                PointData[i] = 0x00
#                DispData[i] = TubeTab[DispData[i]] + PointData

    def coding(self, DispData):
        if self._PointFlag == self.POINT_ON:
            PointData = 0x80
        else:
            PointData = 0
        if DispData == 0x7f:
            DispData = 0x00 + PointData # The bit digital tube off
        else:
            DispData = self.TubeTab[DispData] + PointData
        return DispData

if __name__ == "__main__":
    tm1637 = TM1637(0, 1)
    tm1637.clearDisplay()
    tm1637.set(tm1637.BRIGHT_TYPICAL, 0x40, 0xc0)
    while True:
        for i in range(10):
            time.sleep(1)
            tm1637.display(0,i)
            
