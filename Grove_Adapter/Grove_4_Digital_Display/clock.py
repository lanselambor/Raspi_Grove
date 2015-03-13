from Grove_4_Digital_Display import *
import time
import string

# systerm clock
second = string.atoi( time.strftime('%S') )
minute = string.atoi( time.strftime('%M') )
hour = string.atoi( time.strftime('%H') )

point = 1
mode = 2  # mode = 2, show minute and second; mdoe = 0, show hour and minute
timelist = [hour/10, hour%10, minute/10, minute%10, second/10, second%10]
tm1637 = TM1637(0, 1)


def clock_show(timelist):
    global mode
    for i in range(4):
        tm1637.display(i, timelist[i+mode])   

def clock():
    global timelist
    global second 
    global minute 
    global hour

    time.sleep(1)
    second += 1
    if second == 60:
        second = 0
        minute += 1
    if minute == 60:
        minute = 0
        hour += 1
    if hour == 24:
        hour = 0
    timelist = [hour/10, hour%10, minute/10, minute%10, second/10, second%10]

while True:
    point = ~point
    tm1637.point(point)
    clock()
    clock_show(timelist)
    print time.strftime('%c')

