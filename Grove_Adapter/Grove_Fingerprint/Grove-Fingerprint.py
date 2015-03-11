#!/usr/bin/python

import wiringpi2

FINGERPRINT_OK = 0x00
FINGERPRINT_PACKETRECIEVEERR = 0x01
FINGERPRINT_NOFINGER = 0x02
FINGERPRINT_IMAGEFAIL = 0x03
FINGERPRINT_IMAGEMESS = 0x06
FINGERPRINT_FEATUREFAIL = 0x07
FINGERPRINT_NOMATCH = 0x08
FINGERPRINT_NOTFOUND = 0x09
FINGERPRINT_ENROLLMISMATCH = 0x0A
FINGERPRINT_BADLOCATION = 0x0B
FINGERPRINT_DBRANGEFAIL = 0x0C
FINGERPRINT_UPLOADFEATUREFAIL = 0x0D
FINGERPRINT_PACKETRESPONSEFAIL = 0x0E
FINGERPRINT_UPLOADFAIL = 0x0F
FINGERPRINT_DELETEFAIL = 0x10
FINGERPRINT_DBCLEARFAIL = 0x11
FINGERPRINT_PASSFAIL = 0x13
FINGERPRINT_INVALIDIMAGE = 0x15
FINGERPRINT_FLASHERR = 0x18
FINGERPRINT_INVALIDREG = 0x1A
FINGERPRINT_ADDRCODE = 0x20
FINGERPRINT_PASSVERIFY = 0x21

FINGERPRINT_STARTCODE = 0xEF01

FINGERPRINT_COMMANDPACKET = 0x1
FINGERPRINT_DATAPACKET = 0x2
FINGERPRINT_ACKPACKET = 0x7
FINGERPRINT_ENDDATAPACKET = 0x8

FINGERPRINT_TIMEOUT = 0xFF
FINGERPRINT_BADPACKET = 0xFE

FINGERPRINT_GETIMAGE = 0x01
FINGERPRINT_IMAGE2TZ = 0x02
FINGERPRINT_REGMODEL = 0x05
FINGERPRINT_STORE = 0x06
FINGERPRINT_DELETE = 0x0C
FINGERPRINT_EMPTY = 0x0D
FINGERPRINT_VERIFYPASSWORD = 0x13
FINGERPRINT_HISPEEDSEARCH = 0x1B
FINGERPRINT_TEMPLATECOUNT = 0x1D

wiringpi2.wiringPiSetup()
finger = wiringpi2.Serial('/dev/ttyAMA0', 115200)

class Fingerprint():
    def __init__(self):
        self.thePassword = 0
        self.theAddress = 0xffffffff
        finger.printf("hello fingerprint \n\r");

    def verifyPassword(self):
        packet = [FINGERPRINT_VERIFYPASSWORD, (self.thePassword >> 24), (self.thePassword >> 16),(self.thePassword >> 8), self.thePassword]
        #writePacket(theAddress, FINGERPRINT_COMMANDPACKET, 7, packet)
        len = getReply(packet)
        if len == 1 and packet[0] == FINGERPRINT_ACKPACKET and packet[1] == FINGERPRINT_OK:
            return True
        return false
'''        
    def getImage(self):
        packet = [FINGERPRINT_GETIMAGE]
        #writePacket(theAddress, FINGERPRINT_COMMANDPACKET, 3, packet)
        len = getReply(packet)
        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def image2Tz(self. slot):
        packet[] = [FINGERPRINT_IMAGE2TZ, slot]
        #writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def createModel(self):
        packet[] = [FINGERPRINT_REGMODEL]
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def storeModel(self, id):
        packet[] = [FINGERPRINT_STORE, 0x01, id >> 8, id & 0xFF]
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def deleteModel(self, id):
        packet[] = [FINGERPRINT_DELETE, id >> 8, id & 0xFF, 0x00, 0x01]
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)
        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def emptyDatabase(self):
        packet[] = [FINGERPRINT_EMPTY]
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)

        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1
        return packet[1]
        
    def fingerFastSearch(self):
        fingerID = 0xFFFF
        confidence = 0xFFFF
        # high speed search of slot #1 starting at page 0x0000 and page #0x00A3 
        packet[] = [FINGERPRINT_HISPEEDSEARCH, 0x01, 0x00, 0x00, 0x00, 0xA3]
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)

        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
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
        packet[] = {FINGERPRINT_TEMPLATECOUNT}
        writePacket(theAddress, FINGERPRINT_COMMANDPACKET, sizeof(packet)+2, packet)
        len = getReply(packet)

        if ((len != 1) && (packet[0] != FINGERPRINT_ACKPACKET)):
            return -1

        templateCount = packet[2]
        templateCount <<= 8
        templateCount |= packet[3]

        return packet[1]
    def writePacket(self, addr, packettype, len, packet):
        mySerial->write((uint8_t)(FINGERPRINT_STARTCODE >> 8));
        mySerial->write((uint8_t)FINGERPRINT_STARTCODE);
        mySerial->write((uint8_t)(addr >> 24))
        mySerial->write((uint8_t)(addr >> 16))
        mySerial->write((uint8_t)(addr >> 8))
        mySerial->write((uint8_t)(addr))
        mySerial->write((uint8_t)packettype)
        mySerial->write((uint8_t)(len >> 8))
        mySerial->write((uint8_t)(len))
        sum = (len>>8) + (len&0xFF) + packettype;
        for (uint8_t i=0; i< len-2; i++):
            mySerial->write((uint8_t)(packet[i]))
            sum += packet[i]
        mySerial->write((uint8_t)(sum>>8))
        mySerial->write((uint8_t)sum)

    def getReply(self):
        #reply[20], 
        idx = 0
        timer = 0         
        while True:
            while (!mySerial->available()):
                delay(1)
                timer += 1
        if(timer >= timeout):
            return FINGERPRINT_TIMEOUT
        # something to read!
        reply[idx] = mySerial->read()
        if ((idx == 0) && (reply[0] != (FINGERPRINT_STARTCODE >> 8))):
            continue
        idx += 1
        # check packet!
        if (idx >= 9):
            if ((reply[0] != (FINGERPRINT_STARTCODE >> 8))||(reply[1] != (FINGERPRINT_STARTCODE & 0xFF))):
                return FINGERPRINT_BADPACKET
            packettype = reply[6]
            uint16_t len = reply[7];
            len <<= 8
            len |= reply[8]
            len -= 2
           # Serial.print("Packet len"); Serial.println(len);
            if (idx <= (len+10)):
                continue
            packet[0] = packettype
            for i in range(0, len):
                packet[1+i] = reply[9+i]
            return len
'''
if __name__=="__main__":
    print 'start'
    fingerprint = Fingerprint()
