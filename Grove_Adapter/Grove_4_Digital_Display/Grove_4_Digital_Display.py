#!/usr/bin/python
# import time
import RPi.GPIO as io
import signal 
import time 

class TM1637():        
    def __init__(self, Clk, Data):
        self.Clkpin = Clk
        self.Datapin = Data    
        io.setmode(io.BCM)
        io.setup(self.Clkpin, io.OUT)
        io.setup(self.Datapin, io.OUT)    
        io.output(self.Datapin, io.LOW)
        io.output(self.Clkpin, io.LOW)
        
        self.TubeTab = [0x3f,0x06,0x5b,0x4f,\
            0x66,0x6d,0x7d,0x07,\
           0x7f,0x6f,0x77,0x7c,\
           0x39,0x5e,0x79,0x71]
           
        # definitions for TM1637
        self.ADDR_AUTO  = 0x40
        self.ADDR_FIXED = 0x44
        self.STARTADDR  = 0xc0 
        # definitions for the clock point of the digit tube 
        self.POINT_ON   = 1
        self.POINT_OFF  = 0
        # definitions for brightness
        self.BRIGHT_DARKEST = 0
        self.BRIGHT_TYPICAL = 2
        self.BRIGHTEST      = 7
        
        self.Cmd_SetData = 0
        self.Cmd_SetAddr = 0
        self.Cmd_DispCtrl = 0
        self._PointFlag = 0     # PointFlag=1:the clock point on
        
        print 'begin' 
     

    def init(self):        # To clear the display
        self.clearDisplay()
        print 'init'
        
    def writeByte(self, wr_data):     # write 8bit data to tm1637        
        count1 = 0
        for i in range(0, 8):
            io.output(self.Clkpin, io.LOW)
            if wr_data & 0x01:
                io.output(self.Datapin, io.HIGH)
            else: 
                io.output(self.Datapin, io.LOW)
            wr_data >> 1
            io.output(self.Clkpin, io.HIGH)
            
        io.output(self.Clkpin, io.LOW)
        io.output(self.Datapin, io.LOW)
        io.output(self.Clkpin, io.HIGH)
        io.setup(self.Datapin, io.IN)
        
        while io.input(self.Datapin):
            count1 += 1
            if count1 == 200:
                io.setup(self.Datapin, io.OUT)
                io.output(self.Datapin, io.LOW)
                count1 = 0
            io.setup(self.Datapin, io.IN)
            
        io.setup(self.Datapin, io.OUT)        

        print 'writeByte'
        
    def start(self): # send start bits
        io.output(self.Clkpin, io.HIGH)
        io.output(self.Datapin, io.HIGH)
        io.output(self.Datapin, io.LOW)
        io.output(self.Clkpin, io.LOW)
        
        print 'start'
        
    def stop(self): # send stop bits
        io.output(self.Clkpin, io.LOW)
        io.output(self.Datapin, io.LOW)
        io.output(self.Datapin, io.HIGH)
        io.output(self.Clkpin, io.HIGH)
        
        print 'stop'
        
    def display_1(self, DispData):
        SegData = [0, 0, 0, 0]
        
        for i in range(0, 4):
            SegData[i] = DispData[i]
        
        self.coding_1(SegData)
        self.start()
        self.writeByte(self.ADDR_AUTO)
        
        for i in range(0, 4):
            self.writeByte(SegData[i])
        
        self.stop()
        self.start()
        self.writeByte(self.Cmd_DispCtrl)
        self.stop()
        
        print 'display_1'
        
    def display_2(self, BitAddr, DispData):
        SegData = self.coding_2(DispData)
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
        
        print 'display_2'
        
    def clearDisplay(self):
        self.display_2(0x00,0x7f)
        self.display_2(0x01,0x7f)
        self.display_2(0x02,0x7f)
        self.display_2(0x03,0x7f)
        
        print 'clearDisplay'
        
    def set(self, SetData = 0x40, SetAddr = 0xc0):# To take effect the next time it displays.
        brightness = self.BRIGHT_TYPICAL
        self.Cmd_SetData = SetData
        self.Cmd_SetAddr = SetAddr
        self.Cmd_DispCtrl = 0x88 + brightness
        print 'set'
        
    def point(self, PointFlag): # whether to light the clock point ":".To take effect the next time it displays.
        self._PointFlag = PointFlag
        
        print 'point'
        
    def coding_1(self, DispData):
        PointData = 0
        
        if self._PointFlag == self.POINT_ON:
            PointData = 0x80
        else:
            PointData = 0
        for i in range(0, 4):
            if DispData[i] == 0x7f: 
                DispData[i] = 0x00
            else:
                DispData[i] = self.TubeTab[i] + PointData
            
        print 'coding'
    
    def coding_2(self, DispData):
        PointData = 0
        if self._PointFlag == self.POINT_ON: 
            PointData = 0x80
        else:
            PointData = 0
        if DispData == 0x7f:
            DispData = 0x00 + PointData
        else:
            DispData = self.TubeTab[DispData] + PointData
        return DispData
        
        
        
# Called on process interruption. Set all pins to "Input" default mode.
def endProcess(signalnum = None, handler = None):
    # io.output(tm1637.Datapin, io.LOW)
    # io.output(tm1637.Clkpin, io.LOW)
    io.cleanup()
    exit(0)

# Prepare handlers for process exit
signal.signal(signal.SIGTERM, endProcess)
signal.signal(signal.SIGINT, endProcess)
signal.signal(signal.SIGHUP, endProcess)
signal.signal (signal.SIGQUIT, endProcess)


if __name__ == "__main__":
    # Clk = 2
    # Dio = 3
    # tm1637 = TM1637(Clk, Dio)
    # io.setup(tm1637.Datapin, io.IN)    
    # io.setup(tm1637.Clkpin, io.IN)    
    # tm1637.set()
    # tm1637.init()
    # tm1637.point(tm1637.POINT_ON)
    # TimeDisp = [0x01,0x02,0x03,0x04]
    # tm1637.display_1(TimeDisp)
    # while True:
        # time.sleep(2)
        # tm1637.display_1(TimeDisp)
        # print 'hello'
        
    io.setmode(io.BCM)
    io.setup(3, io.OUT)
    io.output(3, io.LOW)
    io.setup(2, io.OUT)
    io.output(2, io.LOW)
    io.setup(3, io.IN)
    io.setup(2, io.IN)
    
    while True:        
         if io.HIGH == io.input(3):
            print 'Datapin HIGH...'
        # if io.HIGH == io.input(tm1637.Clkpin):
            # print 'Clkpin HIGH...'
        time.sleep(0.1)

