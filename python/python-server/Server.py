"""
Robot Server

A coroutine task using the built in OS which enables remote clients to connect
to the robot and send commands which are then forwarded to serial, and stream
back feedback from serial and video from USB devices over network.
"""
#==============================================================================
# Authors:   Aron Kisdi, Christina McQuirk, Wayne Tubby, Adrian Coveney
# Copyright: Copyright (c) 2010-2012 Science and Technology Facilities Council
# Contact:   aron.kisdi@stfc.ac.uk
#==============================================================================

# Standard imports
from socket import (socket,
                    AF_INET,
                    SOCK_STREAM,
                    SOL_SOCKET,
                    SO_REUSEADDR)

# Custom imports
import functions as f
#import new_API_functions as functions #uncomment this when GUI is sending new API commands
import Setup
from roboS import NewTask
import var
from wrap import Socket
from wrap import Serial


def handle_client(client, addr):
    'this function checks incoming traffic from connected clients'
    while True:
        command = yield client.recv(1024) #receives one megabyte
        if not command:
            break
        #command = command.rstrip() #remove line break characters
                #commands = re.findall(var.command_re,command, re.MULTILINE)
        #print "command received" , command
        commands = var.command_pattern_gen.findall(command)
        for command in commands:
            function_call = command[0]
            args = var.command_pattern_arg.findall(command[1])
            #print "calling", function_call, args
            try:
                methodToCall = getattr(f,function_call)
                methodToCall(*args)
            except AttributeError:
                print "unknown command function"
            if "get" in function_call:
                if var.data:
                    #print var.data
                    #if var.data<>var.data_old:
                    yield client.send(str(var.data))
                    #var.data_old=var.data		
    #f.Stop()
    yield client.close()
    print "client closed"

    
def serial_feedback(ser, client):
    'forwards serial or USB data to socket (wireless)'  
    while True:
        data = yield ser.read(6)
        if not data:
            break
        print "data received"
        for c in data:
            intdata.append(ord(c))
            strdata = strdata + str(ord(c))+","
        strdata =strdata[:-1]+ ";"
        print strdata
        yield client.send(strdata)

def server(port):
    rawsock = socket(AF_INET, SOCK_STREAM)
    rawsock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    rawsock.bind(("", port))
    rawsock.listen(5)
    
    var.soc = rawsock

    soc = Socket(rawsock)

    while True:
        print "listening to client"
        client, addr = yield soc.accept()
        yield NewTask(handle_client(client, addr))
        print "client keep listening"        


