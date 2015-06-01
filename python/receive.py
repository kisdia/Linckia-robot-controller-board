import time
from robot import *

#storage [motor1,motor2,motor3,motor4,pwm1,pwm2,pwm3,pwm4]
#command = [0,0,0,0,0,0,0]
#command_old = [0,0,0,0,0,0,0]
i=0

data = ""
data_old =""

var.s.settimeout(1)

while True:
	send("#get(-1)\n")

	try:
	    data = var.s.recv(1024)
	    
	except socket.timeout:
		pass
		
        #print data
	if data<>data_old:
		data_file = open('/home/data','w')
		data_file.write(data[1:-1])
		data_file.close()
	
		data_old=data
		
	time.sleep(1.0)
