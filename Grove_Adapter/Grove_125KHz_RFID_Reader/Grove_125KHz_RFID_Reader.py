import wiringpi2
import time
import threading
import signal
import sys
 
buf = [0] * 64
flag = True
s = wiringpi2.serialOpen("/dev/ttyAMA0", 9600)        

def RFID():
    print 'thread start ', threading.currentThread().getName()
    
    count = 0 
    global flag
    global buf
    
    while flag == True:
        if wiringpi2.serialDataAvail(s):
            print 'readout: ',
            while wiringpi2.serialDataAvail(s):                                
                buf[count] = wiringpi2.serialGetchar(s)
                count += 1                 
                if count == 64:                    
                    break                    
#            for i in range(0,count):   
#                print '%x'%(buf[i]),   #to hex
#            print ''
           
            for i in range(0,count):   
                print chr( buf[i] ),   #to ASCII              
            print ''              
            
            for i in range(0, count):
                buf[i] = 0
            count = 0     

if __name__ == "__main__":
    t = threading.Thread(target=RFID)
    t.start()

    def do_exit(signalnum = None, handler = None):
        global flag
        flag = False
        t.join()        
        print '\nexit..'
        sys.exit()
        
    signal.signal(signal.SIGINT, do_exit)        
    signal.signal(signal.SIGHUP, do_exit)
    signal.signal (signal.SIGQUIT, do_exit)
       
    while True:
        print "[%s: ]  "%( threading.currentThread().getName() )
        time.sleep(1)
   

