import wiringpi2
import time
import sys

wiringpi2.wiringPiSetup()

# definitions for TM1637
ADDR_AUTO = 0x40
ADDR_FIXED = 0x44
STARTADDR = 0xc0
# definitions for the clock point of the digit tube
POINT_ON = 1
POINT_OFF = 0

# definitions for brightness
BRIGHT_DARKEST = 0
BRIGHT_TYPICAL = 2
BRIGHTEST = 7

# GPIO
OUTPUT = 1
INPUT = 0
HIGH = 1
LOW = 0

TubeTab = [0x3f,0x06,0x5b,0x4f,\
            0x66,0x6d,0x7d,0x07,\
            0x7f,0x6f,0x77,0x7c,\
            0x39,0x5e,0x79,0x71]

class TM1637():
    def __init__(self, Clk, Data):
        self.Cmd_SetData = 0
        self.Cmd_SetAddr = 0
        self.Cmd_DispCtrl = 0
        self._PointFlag = False # _PointFlag=1:the clock point on

        self.Clkpin = Clk
        self.Datapin = Data
        wiringpi2.pinMode(self.Clkpin, OUTPUT)
        wiringpi2.pinMode(self.Datapin, OUTPUT )
    
    def blink(self):
        wiringpi2.digitalWrite(self.Clkpin, HIGH)
        wiringpi2.digitalWrite(self.Datapin, HIGH)
        wiringpi2.digitalWrite(self.Clkpin, LOW)
        wiringpi2.digitalWrite(self.Datapin, LOW)

    def init(self):   # To clear the display
        print 'init'
        self.clearDisplay()
        print 'clearDisplay'

    def writeByte(self, wr_data):  # write 8bit data to tm1637
        print 'writeByte'
        for i in range(0, 8):
           wiringpi2.digitalWrite(self.Clkpin, LOW)
           if(wr_data & 0x01):
              print 'wr_data & 0x01 = ', wr_data & 0x01  
              wiringpi2.digitalWrite(self.Datapin, HIGH)
           else:
              print 'wr_data = ', wr_data
              wiringpi2.digitalWrite(self.Datapin, LOW)
           wr_data >>= 1
           print i
           wiringpi2.digitalWrite(self.Clkpin, HIGH)
        wiringpi2.digitalWrite(self.Clkpin, LOW)
        wiringpi2.digitalWrite(self.Datapin, HIGH)
        wiringpi2.digitalWrite(self.Clkpin, HIGH)
        wiringpi2.pinMode(self.Datapin, INPUT)
        
        count = 0
        while(wiringpi2.digitalRead(self.Datapin)):
           count += 1    
           if(count == 200):
              wiringpi2.pinMode(self.Datapin, OUTPUT)
              wiringpi2.digitalWrite(self.Datapin, LOW)
              count = 0
           wiringpi2.pinMode(self.Datapin, INPUT)
        wiringpi2.pinMode(self.Datapin, OUTPUT)

    def start(self):
        #print 'start'
        wiringpi2.digitalWrite(self.Clkpin, HIGH)
        wiringpi2.digitalWrite(self.Datapin, HIGH)
        wiringpi2.digitalWrite(self.Clkpin, LOW)
        wiringpi2.digitalWrite(self.Datapin, LOW)

    def stop(self):
        #print 'stop'
        wiringpi2.digitalWrite(self.Clkpin, LOW)
        wiringpi2.digitalWrite(self.Datapin, LOW)
        wiringpi2.digitalWrite(self.Clkpin, HIGH)
        wiringpi2.digitalWrite(self.Datapin, HIGH)

    def display(self, DispData):
        #print 'display'
        SegData = [0, 0, 0, 0]
        for i in range(0, 4):
           SegData[i] = DispData[i]
        self.coding(SegData)
        self.start()
        self.writeByte(ADDR_AUTO)
        self.stop()
        self.start()
        self.writeByte(self.Cmd_SetAddr)
        for i in range(0, 4):
            self.writeByte(SegData[i])
        self.stop()
        self.start()
        self.writeByte(self.Cmd_DispCtrl)
        self.stop()

    def display_2(self, BitAddr, DispData):
        print 'display_2'
        SegData = self.coding_2(DispData)
        self.start()
        print 'ADR_FIXED', ADDR_FIXED
        self.writeByte(ADDR_FIXED) 
        self.stop()
        self.start()
        print 'bug1'
        self.writeByte(BitAddr | 0xc0)
        print 'bug2' 
        self.writeByte(SegData)
        self.stop()
        self.start()
        self.writeByte(self.Cmd_DispCtrl) 
        self.stop()

    def clearDisplay(self):
        #print 'clearDisplay'
        self.display_2(0x00, 0x7f)
        self.display_2(0x01, 0x7f)
        self.display_2(0x02, 0x7f)
        self.display_2(0x03, 0x7f)

    def set(self, brightness):
        #print 'set'
        #self.Cmd_SetData = SetData
        #self.Cmd_SetAddr = SetAddr
        self.Cmd_DispCtrl = 0x88 + brightness # Set the brightness and it takes effect the next time it displays.

    def point(self, PointFlag):
        #print 'point'
        self._PointFlag = PointFlag

    def coding(self, DispData):
        #print 'coding'
        PointData = 0
        if(self._PointFlag == POINT_ON):
            PointData = 0x80
        else:
            PointData = 0
        for i in range(0, 4):
            if(DispData[i] == 0x7f):
                PointData[i] = 0x00
                DispData[i] = TubeTab[DispData[i]] + PointData
    def coding_2(self, DispData):
        print 'coding_2'
        PointData = 0
        if(self._PointFlag == POINT_ON):
            PointData = 0x80
        else:
            PointData = 0
        if(DispData == 0x7f):
            DispData = 0x00 + PointData # The bit digital tube off
        else:
            DispData = TubeTab[DispData] + PointData
        return DispData

if __name__ == "__main__":
    #while True:
    tm1637 = TM1637(1, 2)
    tm1637.init()
    tm1637.set(BRIGHT_TYPICAL)
    #NumTab = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    NumTab = [0,1,2,3,4,5,6,7,8,9]
    print sys.getsizeof(NumTab)
    ListDisp = [0,0,0,0]
    time.sleep(0.15)
    i = 0
    count = 0
    while True:
        count += 1
        if(count == 10):
            count = 0 
        for BitSelect in range(0, 4):
            ListDisp[BitSelect] = NumTab[i]
            i += 1
            if(i == 10):
                i = 0
        print 'ready to display'
        tm1637.display_2(0, ListDisp[0])
        print 'display one'
        tm1637.display_2(1, ListDisp[1])
        tm1637.display_2(2, ListDisp[2])
        tm1637.display_2(3, ListDisp[3])
        time.sleep(0.3)
