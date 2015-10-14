# wrap.py
# Coroutine wrapper around a socket object and serial object

from roboS import ReadWait, WriteWait
import socket
import serial
import var

class Socket(object):
	'wrapper for socket send/receive. i.e.: wi-fi'
	def __init__(self, sock):
		self.sock = sock
	
	def accept(self):
		yield ReadWait(self.sock)
		client, addr = self.sock.accept()
		yield Socket(client), addr
	
	def send(self, buffer):
		while buffer:
			yield WriteWait(self.sock)
			length = self.sock.send(buffer)
			buffer = buffer[length:]
	
	def recv(self, maxbytes):
		yield ReadWait(self.sock)
		try:
			yield self.sock.recv(maxbytes)
		except socket.error:
			print 'Socket error occurred. Traceback to follow'
	
	def close(self):
		yield self.sock.close()


class Serial(object):
	'wrapper for serial communication'
	def __init__(self, ser):
		self.ser = ser
	
#    def open_ser(self):
#        yield ReadWait(self.ser)
#        self.ser.open()

	def write(self, byte):
		yield WriteWait(self.ser)
		yield self.ser.write(byte)
	
	def read(self, maxbytes):
		yield ReadWait(self.ser)
		yield self.ser.read(maxbytes)
	
	def readline(self):
		yield ReadWait(self.ser)
		yield self.ser.readline()
	
	def close(self):
		yield self.ser.close()
