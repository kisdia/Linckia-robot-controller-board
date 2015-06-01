"""initial setup of system depending on OS and robot"""

# Standard imports
import logging
import os
import re
import socket

# 3rd party imports
#import pydymx as dynamixel
import serial
import serial.tools.list_ports as listserial
#import cv

# Custom imports
import functions
import var

def setup():
    "Initialise loggers and devices"
    # Operating system and robot name
    var.os_name = os.name
    var.robot = socket.gethostname()
    #setup command pattern
    var.command_pattern_gen = re.compile(var.command_re,re.MULTILINE)
    var.command_pattern_arg = re.compile(var.arg_re)
    initialise_devices()



def initialise_devices():
    "Initialise devices"
    #USB or serial devices setup
    var.devices.append(['Arduino', '/dev/ttyACM0'])
    var.number_of_devices = len(var.devices)


def serial_setup():
    """Setup serial devices"""
    #following for loop sets up serial port according to built in devices, could use switch instead of if?
    #print var.devices
    for device in var.devices:
        new_device = serial.Serial(
                            port = device[1],
                            baudrate = 9600,
                            parity = 'N',
                            rtscts = False,
                            xonxoff = False,
                            timeout = 0,
                        )
        #new_device.open()
        device.append(new_device)
        new_device = None

    print '=' * 37
    print '{0:12} {1:15} {2:8}'.format('Device', 'Port', 'Baudrate')
    print '-' * 37
    for device in var.devices:
            print '{0:12} {1:15} {2:8}'.format(device[0], device[2].port, device[2].baudrate)
    if not var.devices:
        print "No devices"
    print '=' * 37
    #command = chr(255)+chr(1)+chr(1)+chr(1)+chr(180)+chr(0)+chr(0)+chr(254)
    #var.devices[0][2].write(command)


def closedown():
    """
    Close serial ports making them ready to be reopened.
    Should be called after every error.
    """
    functions.Stop()

    for i in xrange(len(var.devices) - 1, -1, -1):  # reverse iteration
        if len(var.devices[i]) > 2 and var.devices[i][2]:
            var.devices[i][2].close()
