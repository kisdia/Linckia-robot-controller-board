import time
import os
from robot import *


command = ""
command_old = ""

start_time = time.clock()

timeout = 0.1 #timeout in seconds

while True:
	#read the new command
	try:
		command_file = open('/tmp/command','r')
	except IOError:
		command_file = None
	if command_file:
		command = command_file.read()
		command_file.close()
		#execute changes
		if command<>command_old:
			send(command+'\n')
			start_time = time.clock()
                	command_old=command
		else:
			if command_old <>"#mov(0)":
                		if time.clock()>start_time+timeout:
					command_stop = "#mov(0)"
					send(command_stop+'\n')
                                	start_time = time.clock()
	time.sleep(0.1)
