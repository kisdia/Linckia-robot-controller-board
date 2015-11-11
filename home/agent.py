import time
from robot import *

#storage [motor1,motor2,motor3,motor4,pwm1,pwm2,pwm3,pwm4]
#command = [0,0,0,0,0,0,0]
#command_old = [0,0,0,0,0,0,0]
i=0


var.s.settimeout(0.5)
while True:
	#read the new command
	command_file = open('/home/command','r')
	command = command_file.read()
	#i=0
	#for line in command_file:
	#	command[i]=line
	#	i=i+1
	
	#execute changes
	send(command+'\n')
	command_file.close()
        i=i+1
        if i==10:
	    #read data
	    send("#get(-1)\n")
	    #data_file = open('/home/data','w')
            i=0
        try:
	    data = var.s.recv(1024)
	    print data
        except socket.timeout:
            pass
	    #data_file.write(data)
	    #data_file.close()
	time.sleep(0.2)
