import wiringpi2

getData = int()
analogVal = int()

class I2C_ADC():
    def __init__(self):
        self.ADDR_ADC121 = 0x55
        self.V_REF = 3.00
        self.REG_ADDR_RESULT = 0x00
        self.REG_ADDR_ALERT = 0x01
        self.REG_ADDR_CONFIG = 0x02
        self.REG_ADDR_LIMITL = 0x03
        self.REG_ADDR_LIMITH = 0x04
        self.REG_ADDR_HYST = 0x05
        self.REG_ADDR_CONVL = 0x06
        self.REG_ADDR_CONVH = 0x07
        
        self.fd = wiringpi2.wiringPiI2CSetup(self.ADDR_ADC121)
        # Configuration Register
        wiringpi2.wiringPiI2CWriteReg8(self.fd, self.REG_ADDR_CONFIG, 0x20)        
        
    def read_adc(self):
        data = 0x0000
        data = wiringpi2.wiringPiI2CReadReg16(self.fd, self.REG_ADDR_RESULT)
        wiringpi2.delay(1)
        return data
        
if __name__=="__main__":
    while True:
	adc = I2C_ADC()
	print 'sensor value ', float(adc.read_adc() / 655.35), '%'
	wiringpi2.delay(1000)
        
