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
#websocket requirements
import re
from base64 import b64encode
from hashlib import sha1
websocket_answer = (
    'HTTP/1.1 101 Switching Protocols',
    'Upgrade: websocket',
    'Connection: Upgrade',
    'Sec-WebSocket-Accept: {key}\r\n\r\n',
)
GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
#end of websocket requirements

def handle_client(client, addr):
    'this function checks incoming traffic from connected clients'
    var.websocket = False
    while True:
        command = yield client.recv(1024) #receives one megabyte
        if not command:
            break
        if var.websocket == True:
            command = decodeCharArray(command)
            command_to_function(command)
            	
	if var.websocket == False:
            if "WebSocket" in command:
                try:
                    key = (re.search('Sec-WebSocket-Key:\s+(.*?)[\n\r]+', command)
                        .groups()[0]
                        .strip())
                    response_key = b64encode(sha1(key + GUID).digest())
                    response = '\r\n'.join(websocket_answer).format(key=response_key)
                    yield client.send(response)
                    var.websocket = True
                except AttributeError:
                    print "wrong websocket initialisation"
            else:
                command_to_function(command)
        	
    #var.websocket = False
    yield client.close()
    print "client closed"

def command_to_function(command):
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
        #if "get" in function_call:
        #    if var.data:
        #        #print var.data
        #        #if var.data<>var.data_old:
        #        yield client.send(str(var.data))
        #        #var.data_old=var.data

def decodeCharArray(stringStreamIn):
    
    # Turn string values into opererable numeric byte values
    byteArray = [ord(character) for character in stringStreamIn]
    datalength = byteArray[1] & 127
    indexFirstMask = 2

    if datalength == 126:
        indexFirstMask = 4
    elif datalength == 127:
        indexFirstMask = 10

    # Extract masks
    masks = [m for m in byteArray[indexFirstMask : indexFirstMask+4]]
    indexFirstDataByte = indexFirstMask + 4
    
    # List of decoded characters
    decodedChars = []
    i = indexFirstDataByte
    j = 0
    
    # Loop through each byte that was received
    while i < len(byteArray):
    
        # Unmask this byte and add to the decoded buffer
        decodedChars.append( chr(byteArray[i] ^ masks[j % 4]) )
        i += 1
        j += 1
    command = "".join(decodedChars)
    # Return the decoded string
    return command


    
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


