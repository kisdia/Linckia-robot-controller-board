import time
from robot import *

command = ""
command_old = ""

start_time = time.clock()

timeout = 0.1 #0.1 is roughly 10 seconds

while True:
	#read the new command
	command_file = open('/home/command','r')
	command = command_file.read()
	command_file.close()

	#execute changes
	if command<>command_old:
		send(command+'\n')
		start_time = time.clock()
                command_old=command
	else:
		#print command_old
		if command_old <>"#mov(0)":
                	if time.clock()>start_time+timeout:
				command_stop = "#mov(0)"
				send(command_stop+'\n')
                                start_time = time.clock()
	time.sleep(0.2)
	