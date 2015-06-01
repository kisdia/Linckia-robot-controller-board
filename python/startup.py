import ConfigParser, os
from subprocess import call
import time

robot_config = ConfigParser.RawConfigParser()
robot_config.read('/etc/config/robot')

reset = robot_config.getint('network', 'reset')

if reset == 0:

    wifi_config =open('/etc/config/wireless','r')
    wifi_backup_config = open('/etc/config/wireless.backup','r')
    if wifi_config <> wifi_backup_config:
        call(["cp", "/etc/config/wireless.backup", "/etc/config/wireless"])
        
elif reset>0:
    reset = reset-1
    robot_config.set('network', 'reset', str(reset))
    robot_config.write('/etc/config/robot')
    
else:
    pass
    


