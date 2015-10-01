#
# Linux code for uploading a compiled hex file to an Arduino Leonardo
# code to reset Leonard based on gitbub.com/Robot-Will/Stino.git
#

from __future__ import print_function

import serial
import time
import glob
from subprocess import call, STDOUT
import sys
from os.path import basename, isfile, exists

def list_serial_ports():
    serial_ports = []
    dev_path = '/dev/'
    dev_names = ['ttyACM*', 'ttyUSB*']
    for dev_name in dev_names:
        pattern = dev_path + dev_name
        serial_ports += glob.glob(pattern)
    return serial_ports

def remove_ports(now_ports, before_ports):
    ports = now_ports[:]
    for port in before_ports:
        if port in ports:
            ports.remove(port)
    return ports

def touch_port(serial_port, baudrate):
    ser = serial.Serial()
    ser.port = serial_port
    ser.baudrate = baudrate
    ser.bytesize = serial.EIGHTBITS
    ser.stopbits = serial.STOPBITS_ONE
    ser.parity = serial.PARITY_NONE
    try:
        ser.open()
    except serial.SerialException:
        pass
    else:
        ser.setDTR(True)
        time.sleep(0.022)
        ser.setDTR(False)
        ser.close()
        time.sleep(1)

def wait_for_port(upload_port, before_ports):
    elapsed = 0
    new_port = 'no_serial'
    while elapsed < 1000:
        now_ports = list_serial_ports()
        diff_ports = remove_ports(now_ports, before_ports)
        print('Ports {{0}}/{{1}} => {{2}}\\n', before_ports,
                          now_ports, diff_ports)
        if diff_ports:
            new_port = diff_ports[0]
            print('Found new upload port: {0}.\\n', new_port)
            break

        before_ports = now_ports
        time.sleep(0.25)
        elapsed += 25

        if ((elapsed >= 500) or elapsed >= 5000)\
                and (upload_port in now_ports):
            new_port = upload_port
            print('Uploading using selected port: {0}.\\n',
                              upload_port)
            break

    if new_port == 'no_serial':
        txt = "Couldn't find a Leonardo on the selected port. "
        txt += 'Check that you have the correct port selected. '
        txt += "If it is correct, try pressing the board's reset button "
        txt += 'after initiating the upload.\\n'
        print(txt)
    return new_port

def do_upload(serial_port, hex_file):
    before_ports = list_serial_ports()
    print("Forcing reset using 1200bps open/close on port {}".format(serial_port))
    touch_port(serial_port, 1200)
    time.sleep(0.4)
    serial_port = wait_for_port(serial_port, before_ports)
    err = call(["avrdude","-v", "-D", "-patmega32U4", "-cavr109", "-P{}".format(serial_port), "-b57600", "-Uflash:w:{}:i".format(hex_file)])
    print("avrdude returned with error {}".format(err), file=sys.stderr)

    return err

if __name__ == '__main__':

    retries = 3
    tries = 0

    if len(sys.argv) is not 3:
        print("Usage: leonardo_upload.py serial_port hex_file", file=sys.stderr)
        sys.exit(-1)
    
    serial_port = sys.argv[1]
    hex_file = sys.argv[2]

    if not exists(serial_port):
        print("serial_port does not exist: is Arduino bootloader installed?", file=sys.stderr)
        sys.exit(-2)

    if not isfile(hex_file):
        print("hex_file does not exist: check path", file=sys.stderr)
        sys.exit(-1)

    print("Uploading {}".format(basename(hex_file)))

    err = do_upload(serial_port, hex_file)

    if err:
        while tries < retries:
            tries += 1
            print("retrying upload {}/{}".format(tries, retries), file=sys.stderr)
            err = do_upload(serial_port, hex_file)
            if not err:
                break

    sys.exit(err)