#!/usr/bin/python

import wiringpi2
import time



wiringpi2.wiringPiSetup()

class Fingerprint():
    def __init__(self):
        self.FINGERPRINT_OK = 0x00
        self.FINGERPRINT_PACKETRECIEVEERR = 0x01
        self.FINGERPRINT_NOFINGER = 0x02
        self.FINGERPRINT_IMAGEFAIL = 0x03
        self.FINGERPRINT_IMAGEMESS = 0x06
        self.FINGERPRINT_FEATUREFAIL = 0x07
        self.FINGERPRINT_NOMATCH = 0x08
        self.FINGERPRINT_NOTFOUND = 0x09
        self.FINGERPRINT_ENROLLMISMATCH = 0x0A
        self.FINGERPRINT_BADLOCATION = 0x0B
        self.FINGERPRINT_DBRANGEFAIL = 0x0C
        self.FINGERPRINT_UPLOADFEATUREFAIL = 0x0D
        self.FINGERPRINT_PACKETRESPONSEFAIL = 0x0E
        self.FINGERPRINT_UPLOADFAIL = 0x0F
        self.FINGERPRINT_DELETEFAIL = 0x10
        self.FINGERPRINT_DBCLEARFAIL = 0x11
        self.FINGERPRINT_PASSFAIL = 0x13
        self.FINGERPRINT_INVALIDIMAGE = 0x15
        self.FINGERPRINT_FLASHERR = 0x18
        self.FINGERPRINT_INVALIDREG = 0x1A
        self.FINGERPRINT_ADDRCODE = 0x20
        self.FINGERPRINT_PASSVERIFY = 0x21

        self.FINGERPRINT_STARTCODE = 0xEF01

        self.FINGERPRINT_COMMANDPACKET = 0x1
        self.FINGERPRINT_DATAPACKET = 0x2
        self.FINGERPRINT_ACKPACKET = 0x7
        self.FINGERPRINT_ENDDATAPACKET = 0x8

        self.FINGERPRINT_TIMEOUT = 0xFF
        self.FINGERPRINT_BADPACKET = 0xFE

        self.FINGERPRINT_GETIMAGE = 0x01
        self.FINGERPRINT_IMAGE2TZ = 0x02
        self.FINGERPRINT_REGMODEL = 0x05
        self.FINGERPRINT_STORE = 0x06
        self.FINGERPRINT_DELETE = 0x0C
        self.FINGERPRINT_EMPTY = 0x0D
        self.FINGERPRINT_VERIFYPASSWORD = 0x13
        self.FINGERPRINT_HISPEEDSEARCH = 0x1B
        self.FINGERPRINT_TEMPLATECOUNT = 0x1D

        self.thePassword = 0
        self.theAddress = 0xffffffff

        self.fd = wiringpi2.serialOpen('/dev/ttyAMA0', 57600)
        

    def verifyPassword(self):
        packet = [self.FINGERPRINT_VERIFYPASSWORD, (self.thePassword >> 24), (self.thePassword >> 16),(self.thePassword >> 8), self.thePassword]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, 7, packet)
        len = getReply(packet)
        if len == 1 and packet[0] == self.FINGERPRINT_ACKPACKET and packet[1] == self.FINGERPRINT_OK:
            return True
        return false

    def getImage(self):
        packet = [FINGERPRINT_GETIMAGE]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, 3, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def image2Tz(self, slot):
        packet = [self.FINGERPRINT_IMAGE2TZ, slot]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def createModel(self):
        packet = [self.FINGERPRINT_REGMODEL]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def storeModel(self, id):
        packet = [self.FINGERPRINT_STORE, 0x01, id >> 8, id & 0xFF]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def deleteModel(self, id):
        packet = [self.FINGERPRINT_DELETE, id >> 8, id & 0xFF, 0x00, 0x01]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def emptyDatabase(self):
        packet = [self.FINGERPRINT_EMPTY]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        return packet[1]
        
    def fingerFastSearch(self):
        fingerID = 0xFFFF
        confidence = 0xFFFF
        # high speed search of slot #1 starting at page 0x0000 and page #0x00A3 
        packet = [self.FINGERPRINT_HISPEEDSEARCH, 0x01, 0x00, 0x00, 0x00, 0xA3]
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1  and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        fingerID = packet[2]
        fingerID <<= 8
        fingerID |= packet[3]
        confidence = packet[4]
        confidence <<= 8
        confidence |= packet[5]
        return packet[1]

    def getTemplateCount(self):
        templateCount = 0xFFFF
        # get number of templates in memory
        packet = {self.FINGERPRINT_TEMPLATECOUNT}
        writePacket(self.theAddress, self.FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if len != 1 and packet[0] != self.FINGERPRINT_ACKPACKET:
            return -1
        templateCount = packet[2]
        templateCount <<= 8
        templateCount |= packet[3]
        return packet[1]

    def writePacket(self, addr, packettype, len, packet):
        wiringpi2.serialPutchar(self.fd, self.FINGERPRINT_STARTCODE >> 8)
        wiringpi2.serialPutchar(self.fd, self.FINGERPRINT_STARTCODE & 0xff)
        wiringpi2.serialPutchar(self.fd, ( addr >> 24 ) & 0xFF )
        wiringpi2.serialPutchar(self.fd, ( addr >> 16 ) & 0xFF )
        wiringpi2.serialPutchar(self.fd, ( addr >> 8 ) & 0xFf )
        wiringpi2.serialPutchar(self.fd, addr & 0xFF )
        wiringpi2.serialPutchar(self.fd, packettype )
        wiringpi2.serialPutchar(self.fd, len >> 8 )
        wiringpi2.serialPutchar(self.fd, len )
        sum = 0x000
        sum = (len>>8) + (len&0xFF) + packettype

        for i in range(0, len - 2):
            wiringpi2.serialPutchar(self.fd, packet[i] )
            sum += packet[i]
        wiringpi2.serialPutchar(self.fd, sum>>8 )
        wiringpi2.serialPutchar(self.fd, sum )

    def getReply(self):
        reply = [0x00 for i in range(20)]
        idx = 0x00
        timer = 0x0000         
        while True:
            while  0 == wiringpi2.serialDataAvail():
                wiringpi2.delay(1)
                timer += 1
                if(timer >= timeout):
                    return self.FINGERPRINT_TIMEOUT
                # something to read!
                reply[idx] = wiringpi2.serialGetchar(self.fd)
                if ((idx == 0) and (reply[0] != (self.FINGERPRINT_STARTCODE >> 8))):
                    continue
                idx += 1
                # check packet!
                if idx >= 9:
                    if ((reply[0] != (self.FINGERPRINT_STARTCODE >> 8)) or (reply[1] != (self.FINGERPRINT_STARTCODE & 0xFF))):
                        return self.FINGERPRINT_BADPACKET
                    packettype = reply[6]
                    len = reply[7]
                    len <<= 8
                    len |= reply[8]
                    len -= 2
                    # Serial.print("Packet len"); Serial.println(len);
                    if idx <= (len+10):
                        continue
                    packet[0] = packettype
                    for i in range(0, len):
                        packet[1+i] = reply[9+i]
                    return len

if __name__=="__main__":
    print 'start'
    fp = Fingerprint()
    p = [0x33, 0x44]
    while True:
        fp.writePacket(0x11111111, 0x02, 0x02, p)
        wiringpi2.serialPutchar(fp.fd, 0x00 )
        time.sleep(1) 
        
