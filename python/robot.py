import time
import socket
import var

def move(direction, speed = 80):
	if direction == "forward":
		send("#mov("+str(speed)+")\n")
	elif direction == "back":
		send("#mov("+str(-speed)+")\n")
	elif direction == "left":
		send("#mov("+str(speed)+", -90)\n")
	elif direction == "right":
		send("#mov("+str(speed)+", 90)\n")
	else:
		send("#mov(0)\n")

def stop():
	move('stop')
	
def delay(seconds):
	time.sleep(seconds)

def send(data):
	var.s.sendall(data)
	
def local_connect():
	host, port = "localhost", 2000
	while var.s is None:
		var.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
		    var.s.connect((host, port))
                except socket.error: #Exception, e:
                    #print e
                    var.s = None
                    time.sleep(2)
		
def read():
	send("#get(-1)\n")
	try:
	    data = var.s.recv(1024)
	except socket.timeout:
		pass
	data_file = open('/home/data','r')
	data=data_file.read()
	data_file.close()
	
	return data	

while var.s == None:
	try:
		local_connect()
		var.s.settimeout(0.5)
	except socket.error:
		pass
