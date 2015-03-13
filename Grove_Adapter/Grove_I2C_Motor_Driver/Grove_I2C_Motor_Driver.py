import wiringpi2
import time
 
class Motor():
    def __init__(self):
	self.MotorSpeedSet=0x82
	self.PWMFrequenceSet=0x84
	self.DirectionSet=0xaa
	self.MotorSetA=0xa1
	self.MotorSetB=0xa5
	self.Nothing=0x01
	self.EnableStepper=0x1a
	self.UnenableStepper=0x1b
	self.Stepernu=0x1c
	self.I2CMotorDriverAdd=0x0f   # Set the address of the I2CMotorDriver
	# set the steps you want, if 255, the stepper will rotate continuely
	
	self.i2c_fd = wiringpi2.wiringPiI2CSetup(self.I2CMotorDriverAdd)
    
    def SteperStepset(self, stepnu):
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.Stepernu, self.Nothing<<8 | stepnu) # transmit to device I2CMotorDriverAdd

    #######################################
    # Enanble the i2c motor driver to drive a 4-wiringpi2 stepper. the i2c motor driver will
    #driver a 4-wiringpi2 with 8 polarity  .
    #Direction: stepper direction  1/0
    #motor speed: defines the time interval the i2C motor driver change it output to drive the stepper
    #the actul interval time is : motorspeed * 4ms. that is , when motor speed is 10, the interval time 
    #would be 40 ms
    #########################################
    def StepperMotorEnable(self,Direction, motorspeed):
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.EnableStepper, motorspeed<<8 | Direction) # transmit to device I2CMotorDriverAdd
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.EnableStepper, motorspeed<<8 | Direction) # transmit to device I2CMotorDriverAdd

    #function to uneanble i2C motor drive to drive the stepper.
    def StepperMotorUnenable(self,):
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.UnenableStepper, self.Nothing<<8 | self.Nothing) # transmit to device I2CMotorDriverAdd
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.UnenableStepper, self.Nothing<<8 | self.Nothing) # transmit to device I2CMotorDriverAdd

    ###################################
    #Function to set the 2 DC motor speed
    #motorSpeedA : the DC motor A speed should be 0~255
    #motorSpeedB: the DC motor B speed should be 0~255

    def MotorSpeedSetAB(self,MotorSpeedA , MotorSpeedB): 
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.MotorSpeedSet, MotorSpeedB<<8 | MotorSpeedA) # transmit to device I2CMotorDriverAdd
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.MotorSpeedSet, MotorSpeedB<<8 | MotorSpeedA) # transmit to device I2CMotorDriverAdd

    #set the prescale frequency of PWM, 0x03 default
    def MotorPWMFrequenceSet(self,Frequence):      
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.PWMFrequenceSet, self.Nothing<<8 | Frequence) # transmit to device I2CMotorDriverAdd
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.PWMFrequenceSet, self.Nothing<<8 | Frequence) # transmit to device I2CMotorDriverAdd

    #set the direction of DC motor. 
    def MotorDirectionSet(self,Direction):       #  Adjust the direction of the motors 0b0000 I4 I3 I2 I1
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.DirectionSet, self.Nothing<<8 | Direction) # transmit to device I2CMotorDriverAdd
        wiringpi2.wiringPiI2CWriteReg16(self.i2c_fd, self.DirectionSet, self.Nothing<<8 | Direction) # transmit to device I2CMotorDriverAdd


    def MotorDriectionAndSpeedSet(self,Direction, MotorSpeedA, MotorSpeedB):    #you can adjust the driection and speed together
        self.MotorDirectionSet(Direction)
        self.MotorSpeedSetAB(MotorSpeedA,MotorSpeedB)  

if __name__=="__main__":  
    
    motor = Motor()
    # the following code sent commands to motor driver to drive DC motor
    while True:  
        print 'set DC motor'
	wiringpi2.delay(10) #this delay needed
	motor.MotorSpeedSetAB(255,255)#defines the speed of motor 1 and motor 2
	motor.MotorDirectionSet(0b0101)  #0b0101  Rotating in the opposite direction
        time.sleep(0.1)
	motor.MotorDirectionSet(0b1010)  #"0b1010" defines the output polarity, "10" means the M+ is "positive" while the M- is "negtive"
        time.sleep(0.1)
    
  

