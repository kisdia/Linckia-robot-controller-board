#variables for global use

import ConfigParser

###PLATFORM INFORMATION
#operating system
operation = 0 #counting how many operations the log files logged on this computer
os_name = None
location = None

###LOGGING
feedback = False
sys_logger = None
metric_logger = None

###System check
run = True
on = False

###NETWORK INFORMATION
#ports
soc = None
port = 2000

websocket = False
###DEVICES

#devices
devices = [] # stores all device information connected by USB or serial. It is a list of list, for each device storing [Name, Path or Port, pyserial object, wrapped object]
number_of_devices = 0
serial_start = 0

#motor calibration
robot_config = ConfigParser.RawConfigParser()
robot_config.read('/etc/config/robot')
motors = [robot_config.getint('robot', 'motor1'),robot_config.getint('robot', 'motor2'),robot_config.getint('robot', 'motor3'),robot_config.getint('robot', 'motor4')]

#time checks
beat = 0

#sub command cache
sub_command = None

#arduino command cache
current_arduino_no = 0
write_to_arduino = None
convert = True

###COMMANDS
command_re = r'^#(?P<cmd>[a-z]{3})\((?P<args>(?:,?(?:-?\d{1,4}\b|[a-z]+)){0,5})\)[\r\n]?'
arg_re = r'(?:-?\d{1,4}\b|[a-z]+)'
command_pattern_gen = None
command_pattern_arg = None
#command = None
data = [0,0,0,0,0,0]
data_old = [0,0,0,0,0,0]
start_feedback = [2,1,1,0,10,0] #turn on motor feedback interval of 1000 millisec
lost_data = None

#driving
turn=0
angles = [0,0,0]
speed = 0
