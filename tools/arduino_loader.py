#!/usr/bin/python
#!/usr/bin/env python

import serial, sys, time
import subprocess

serialPort = "/dev/ttyACM0"

ser = serial.Serial(
    port=serialPort,
    baudrate=1200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
ser.isOpen()
ser.close()             # close port

###sleeptime
time.sleep(2)
###sleep is over

def execute(command):    
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line) # yield line

execute(["avrdude","-v", "-patmega32U4", "-cavr109", "-P/dev/ttyACM0", "-b57600", "-Uflash:w:/tmp/mounts/Disc-A1/Asteroidea_v2_test.cpp.hex:i"])

 
