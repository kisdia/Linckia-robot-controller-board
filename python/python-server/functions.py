#BUILT IN FUNCTIONS
#functions.py
#This file has a collection of function deffinitions
#which make controlling the robot easier
#these high level functions can be called instead of
#direct commands which makes control and AI code
#much more human readable

import time
import var
import logging
import socket
import serial
import struct

from wrap import Socket
from wrap import Serial
import math
from serial.serialutil import SerialException


def set(target,position, time = 0, duration = 0, delay = 0):
    target, position = int(target), int(position)
    position100 = int(position/100)
    position = position - position100
    command =  chr(255)+ chr(2)+chr(target)+chr(position100)+chr(position)+chr(0)+ chr(0)+chr(254)
    var.devices[0][2].write(command)

def get(target, time = 0, duration = 0, delay = 0):
    target = int(target)
    if target <0:
        targets = [0,1,2,3,4,5]
    else:
        targets =[target]

    for target in targets:
        command =  chr(255)+ chr(3)+chr(target)+chr(0)+chr(0)+chr(0)+ chr(0)+chr(254)
        var.devices[0][2].write(command)
        data = ""
        if var.devices[0][2].inWaiting()>5:
            data = var.devices[0][2].read(6)
        #if var.devices[0][2].inWaiting()>0:
        #    discard = var.devices[0][2].read(var.devices[0][2].inWaiting())
        #print target,len(data)
        if len(data)>5:
            #print ord(data[0]),ord(data[1]),ord(data[2]),ord(data[3]),ord(data[4]),ord(data[5])
            #if len(data)>5:
            #print ord(data[3]), ord(data[4])
            if ord(data[2])<6:
                var.data[ord(data[2])] = ord(data[3])*100+ord(data[4])
            #data = ord(data[3])*100+ord(data[4])
        #else:
            #data = 0
        #var.data[target] = data
    while var.devices[0][2].inWaiting()>5:
        data = var.devices[0][2].read(6)
        if ord(data[2])<6:
            var.data[ord(data[2])]= ord(data[3])*100+ord(data[4])
    if var.devices[0][2].inWaiting()>0:
        discard = var.devices[0][2].read(var.devices[0][2].inWaiting())
    
def mov(power,turn=0,time = 0, duration = 0, delay = 0):
    power, turn = int(power), int(turn)
    x = math.cos(math.radians(turn))*power*var.motors[0]/50 #% calibration doubled 100=> is 200% number between 0-200
    y = math.sin(math.radians(turn))*power*var.motors[3]/50
    right = x+ y
    left = x - y
    direction = 0
    if right <0:
        direction = 1
        right = abs(right)
    commandRight1 = chr(255)+chr(1)+chr(1)+chr(direction)+chr(int(round(right)))+chr(duration)+chr(0)+chr(254)
    commandRight2 = chr(255)+chr(1)+chr(2)+chr(direction)+chr(int(round(right)))+chr(duration)+chr(0)+chr(254)
    direction = 0
    if left <0:
        direction =1
        left = abs(left)
    commandLeft1 = chr(255)+chr(1)+chr(3)+chr(direction)+chr(int(round(left)))+chr(duration)+chr(0)+chr(254)
    commandLeft2 = chr(255)+chr(1)+chr(4)+chr(direction)+chr(int(round(left)))+chr(duration)+chr(0)+chr(254)
    var.devices[0][2].write(commandRight1)
    var.devices[0][2].write(commandRight2)
    var.devices[0][2].write(commandLeft1)
    var.devices[0][2].write(commandLeft2)
    
    
def arm(positions,times = [0,0,0,0,0]):
    for i in range(0,4):
        set(5-i,positions[i],times[i])
    

def Stop():
    "sets wheels to start position - stops wheels"
    mov(0)

