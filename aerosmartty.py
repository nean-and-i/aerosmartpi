#!/usr/bin/python

#  In order to read a reg first a write through the serial bus should be done.
#  The ID and the Reg number incremented with 1 should be written.
#   eg: "130 201\n" will instantiate the read of register 200
#  D&W will respond with a string which contains the value of the reguster
#   eg: "130 201 21235" This means register 200 contains the value 21235
#                       For this reg a temp of 21.235 C
#
# https://github.com/diresi/drexel-und-weiss
# https://github.com/Bernator/smarthome/tree/develop/plugins/drexelundweiss
#
# LU_ID=130
# WP_ID=140
# Busmonitor=0
#
# nean.and.i@gmail.com
# version alpha v0.20170105
#

import serial
import re
import socket
import sys
import time
import argparse
#import datetime
#
#today = datetime.date.today()
#today.strftime('%Y%m%d')

################################################################################
# arguments

parser = argparse.ArgumentParser(description='Aerosmart TTY API ***|\|***')
parser.add_argument('-type','--type', type=int, help='LU=130 or WP=140',required=True)
parser.add_argument('-m','--modbusid', type=int, help='Modbus ID (for read +1 !)',required=True)
parser.add_argument('-v','--value',type=int, help='value for write', required=False)
args = parser.parse_args()

#checks args
if args.type == 130 or args.type == 140:
    print args.type
else:
    parser.print_help()
    sys.exit(0)

if args.value:
    send = str(args.type) + " " + str(args.modbusid) + " " + str(args.value)
    check = str(args.type) + " " + str(args.modbusid + 1)
else:
    send = str(args.type) + " " + str(args.modbusid)


################################################################################
# lock process

def get_lock(process_name):
    global lock_socket   # Without this our lock gets garbage collected
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        print ("################################################################################" )
        print '# LOCK aeroserial'
        print ("################################################################################" )
    except socket.error:
        print ("################################################################################" )
        print '# ERROR, LOCK exists'
        print ("################################################################################" )
        sys.exit()

get_lock('running_test')


################################################################################
# Serial port specs
# initialization and open the port

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS     #number of bits per bytes
ser.parity = serial.PARITY_NONE     #set parity check: no parity
ser.stopbits = serial.STOPBITS_ONE  #number of stop bits
#ser.timeout = None                 #block read
ser.timeout = 0                     #non-block read
#ser.timeout = 2                    #timeout block read
ser.xonxoff = True                  #disable software flow control
ser.rtscts = False                  #disable hardware (RTS/CTS) flow control
ser.dsrdtr = False                  #disable hardware (DSR/DTR) flow control
ser.writeTimeout = 2                #timeout for write


################################################################################


try:
    ser.open()
except Exception, e:
    print "error open serial port: " + str(e)
    exit()

if ser.isOpen():
    try:
        # flush input buffer, discarding all its contents
        ser.flushInput()
        # flush output buffer, aborting current output
        ser.flushOutput()
        #
        #print(solltemp)
        # DEBUG
        print "write data: " + send
        # write to aerosmart
        ser.write((send + "\r\n").encode())
        #
        time.sleep(0.1)
        #
        #
        if args.value:
            time.sleep(0.1)
            print "check data: " + check
            # read register
            ser.write(( check + "\r\n").encode())
        #
        while True:
            # t1 = time for internal processing: 40ms per device
            time.sleep(0.05)
            response = ser.readline()
            if len(response) > 0:
                # DEBUG
                #print "DEBUG:\n" + response
                value = response.split()
                # DEBUG
                #print(value)
                # check for proper return value
                # DEBUG
                #print(value[2])
                #
                # check for proper return value
                #if str(args.modbusid) == str(value[1]):
                if str(value[2]):
                    print "OK:\n" + str(value[0]) + " " + str(value[1]) + " " + str(value[2])
                    # flush input buffer, discarding all its contents
                    ser.flushInput()
                    # flush output buffer, aborting current output
                    ser.flushOutput()
                    break                        #
                else:
                    #print"ERROR :\n" + response
                    continue
        #
        ser.close()
    except Exception, e1:
        print "error communicating...: " + str(e1)
else:
    print "cannot open serial port "

#EOF
