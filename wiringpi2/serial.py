import wiringpi2
import time

serial=wiringpi2.Serial('/dev/ttyAMA0', 115200)
sentence = ['a','b','c','d','e','f','g']
def test(arr, len):
    for i in range(0, len):
        serial.printf("\n\r", arr[i])
while(True):
    time.sleep(0.5)
    test(sentence, 7)
    #serial.printf("hello\n\r")
    #serial.printf('byebye')
    #serial.putchar(0x0a)
    #serial.putchar(0x0d)
    #serial.printf('this is enter and return \n\r') 
