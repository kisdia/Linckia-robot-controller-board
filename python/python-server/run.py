"""Start all code running on robot. Neither system nor robot dependent."""

# Standard imports
import time
import traceback

# Custom imports
import Setup
import var
from roboS import Scheduler
from Server import server
from serial import SerialException


# The following while loop keeps restarting the program if there is an error
# It will stop if errors occur too frequently

FREQ_LIMIT = 4     # limit on frequency of errors in seconds

START = 0

DELTA = FREQ_LIMIT  # done so first error doesn't count towards limit

while DELTA >= FREQ_LIMIT:
    try:
        try:
            Setup.setup()
            Setup.serial_setup()
        except StandardError:
            print "serial setup error"
            time.sleep(2)
            if var.serial_start == 0:
                var.serial_start = 1
            elif var.serial_start ==1:
                var.serial_start = 0
            Setup.setup()
            Setup.serial_setup()
        SCHED = Scheduler()
        SCHED.new(server(var.port))
        SCHED.mainloop()
        
    except StandardError:
        print "standard error"
	print traceback.format_exc()
	#print var.devices
	#print var.devices[0][2].isOpen()
	#break
        STOP = time.time()
        DELTA = STOP - START
        
        if var.soc:
            var.soc.close()  # close socket so it's free to reconnect on restart
        START = time.time()

