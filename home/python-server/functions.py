#BUILT IN FUNCTIONS
#functions.py
#This file has a collection of function deffinitions
#which make controlling the robot easier
#these high level functions can be called instead of
#direct commands which makes control and AI code
#much more human readable

import time as t
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
	#position100 = int(position/100)
	#position = position - position100
	command =  chr(255)+ chr(2)+chr(target+1)+chr(position)+chr(0)+chr(0)+ chr(0)+chr(254)
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
		if len(data)>5:
			if ord(data[2])<6:
				var.data[ord(data[2])] = ord(data[3])*100+ord(data[4])
	while var.devices[0][2].inWaiting()>5:
		data = var.devices[0][2].read(6)
		if ord(data[2])<6:
			var.data[ord(data[2])]= ord(data[3])*100+ord(data[4])
	if var.devices[0][2].inWaiting()>0:
		discard = var.devices[0][2].read(var.devices[0][2].inWaiting())

def wheel(wheel_id, speed, accel_duration=0):
	direction = 0
	if speed<0:
		direction=1
	command = chr(255)+chr(1)+chr(wheel_id)+chr(direction)+chr(abs(speed))+chr(accel_duration)+chr(0)+chr(254)
	var.devices[0][2].write(command)

def mov(power,turn=0,time = 0, duration = 0, delay = 0):
	power, turn, time, duration, delay = int(power), int(turn), int(time), int(duration), int(delay)
	x = math.cos(math.radians(turn))*power
	y = math.sin(math.radians(turn))*power
	if abs(turn)==90:
		var.turn = 90
		set(0,160)
		set(1,160)
		set(2,160)
		t.sleep(4)
	elif turn<>var.turn:
		var.turn = turn
		set(0, 45-turn)
		set(1, 45+turn)
		set(2, 45-turn)
		if turn<>0:
			if var.speed<>power:
				t.sleep(3)
	right = x+ y
	left = x - y
	direction = 0
	if right <0:
		direction = 1
		right = abs(right)
	commandRight1 = chr(255)+chr(1)+chr(1)+chr(direction)+chr(int(round(right)))+chr(duration)+chr(0)+chr(254)
	commandRight2 = chr(255)+chr(1)+chr(3)+chr(direction)+chr(int(round(right)))+chr(duration)+chr(0)+chr(254)
	direction = 0
	if left <0:
		direction = 1
		left = abs(left)
	commandLeft1 = chr(255)+chr(1)+chr(2)+chr(direction)+chr(int(round(left)))+chr(duration)+chr(0)+chr(254)
	commandLeft2 = chr(255)+chr(1)+chr(4)+chr(direction)+chr(int(round(left)))+chr(duration)+chr(0)+chr(254)
	var.speed = power
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

