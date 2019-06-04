#!/usr/bin/python

#  In order to read a reg first a write through the serial bus should be done.
#  The ID and the Reg number incremented with 1 should be written.
#   eg: "130 201\n" will instantiate the read of register 200
#  D&W will respond with a string which contains the value of the reguster
#   eg: "130 201 21235" This means register 200 contains the value 21235
#                       For this reg a temp of 21.235 C
#
# LU_ID=130
# WP_ID=140
# Busmonitor=0
#
# nean.and.i@gmail.com
# version alpha v0.20180523
#

import serial
import re
import socket
import sys
import time


def get_lock(process_name):
    global lock_socket   # Without this our lock gets garbage collected
    lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    try:
        lock_socket.bind('\0' + process_name)
        print '# lock aeroserial'
    except socket.error:
        print '# lock exists'
        sys.exit()

get_lock('running_test')


#initialization and open the port
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


# LU ID = 130
LU = 130
# WP ID = 140
WP = 140

# dictionary
# https://docs.python.org/2/tutorial/datastructures.html#dictionaries

REG = {}
# variable = "ID" "register +1 !!!!!"
#
REG['innentemp.value'] = str(LU) + " " + str(200+1)
REG['aussentemp.value'] = str(LU) + " " + str(202+1)
REG['raumsolltemp.value'] = str(LU) + " " + str(5016+1)
REG['co2.value']  = str(LU) + " " + str(230+1)
REG['co2luefterstufe0.value']  = str(LU) + " " + str(5274+1)
REG['co2luefterstufe1.value']  = str(LU) + " " + str(5276+1)
REG['co2luefterstufe2.value']  = str(LU) + " " + str(5278+1)
REG['co2luefterstufe3.value']  = str(LU) + " " + str(5280+1)
REG['luefterstatus.value'] = str(LU) + " " + str(1066+1)
REG['beschattungstatus.value'] = str(LU) + " " + str(5336+1)
REG['beschattungtemp.value'] = str(LU) + " " + str(5338+1)
REG['beschattungaussentemp.value'] = str(LU) + " " + str(5340+1)
REG['beschattunganfoderungstatus.value'] = str(LU) + " " + str(1218+1)
#REG['revisionstuerstatus.value'] = str(LU) + " " + str(226+1)
REG['abluftprozent.value'] = str(LU) + " " + str(1094+1)
REG['abluftumin.value'] = str(LU) + " " + str(1186+1)
REG['zuluftprozent.value'] = str(LU) + " " + str(1092+1)
REG['zuluftumin.value'] = str(LU) + " " + str(1184+1)
#REG['abluftdifferenzdruck.value'] = str(LU) + " " + str(220+1)
#REG['zuluftdifferenzdruck.value'] = str(LU) + " " + str(218+1)
REG['abluftsollvolumenstrom.value'] = str(LU) + " " + str(1084+1)
REG['zuluftsollvolumenstrom.value'] = str(LU) + " " + str(1082+1)
#
# WP
REG['boilertemp.value'] = str(WP) + " " + str(212+1)
REG['boilerwaermepumpetemp.value'] = str(WP) + " " + str(214+1)
REG['waermepumpestatus.value'] = str(WP) + " " + str(1044+1)
REG['boilerverdampfregistertemp.value'] = str(WP) + " " + str(210+1)
# WP HST
REG['heizungplusstatus.value'] = str(WP) + " " + str(5492+1)
REG['heizstufe1anforderungstatus.value'] = str(WP) + " " + str(1032+1)
# = K-HST2 = PTC
REG['heizstufe2anforderungstatus.value'] = str(WP) + " " + str(1034+1)
# badplusstatu == elektroheizstababforderung == boilerheizstababforderung
#REG['badplusstatus.value'] = str(WP) + " " + str(5036+1)
REG['boilerheizstabanforderungstatus.value'] = str(WP) + " " + str(1038+1)
#
# EXT
#REG['extstatus.value'] = str(LU) + " " + str(252+1)
#REG['extanforderungstatus.value'] = str(LU) + " " + str(228+1)
#
# Betriebsstunden
# hst1/2 = min -> /60=h /24=t
#REG['heizstufe1stunden.value'] = str(WP) + " " + str(912+1)
#REG['heizstufe2stunden.value'] = str(WP) + " " + str(914+1)
#REG['elektroheizstabstunden.value'] = str(WP) + " " + str(922+1)
#REG['keineahnung.value'] = str(WP) + " " + str(1054+1)
#
# Errors WP
#REG['errorboilersensor.value'] = str(WP) + " " + str(830+1)
#REG['errorboilerhightemp.value'] = str(WP) + " " + str(810+1)
#REG['errorraumsensor.value'] = str(WP) + " " + str(804+1)
#REG['errorverdampfregistersensor.value'] = str(WP) + " " + str(808+1)
# Errors LU
#REG['errorco2sensor.value'] = str(LU) + " " + str(832+1)
#REG['errorzuluft.value'] = str(LU) + " " + str(824+1)
#REG['errorabluft.value'] = str(LU) + " " + str(826+1)
#REG['erroraussenluftsensor.value'] = str(LU) + " " + str(806+1)
# Errors sum
#REG['errorsum.value'] = str(WP) + " " + str(800+1)
#REG['error2sum.value'] = str(WP) + " " + str(7500+1)
# print(REG.get("co2","0"))


# debug
#for k,v in REG.items():
#    print k,':',v

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
        #write data
        #for k in REG.keys():
        #for k in REG.iterkeys():
        #for k, v in REG.iteritems():
        for k, v in sorted(REG.items()):
            # debug
            #print(REG.get(k, "error")
            #ask = REG.get(k,"130 5000")
            #
            #ser.write((str(REG.get(k,"130 5000")) + "\r\n").encode())
            if not len(v) > 0:
                break
            ser.write((v + "\r\n").encode())
            # debug
            #print "write data: " + REG[k]
            while True:
                # give the serial port sometime to receive the data
                time.sleep(0.2)
                response = ser.readline()
                if len(response) > 0:
                    # debug
                    #print(response)
                    value = response.split()
                    # debug
                    #print(value)
                    # check for proper return value
                    if str(v) == str(value[0] + " " + value[1]):
                        if value[2]:
                            if 'temp' in str(k):
                                value[2] = str(int(value[2])/1000.0)
                            if 'prozent' in str(k):
                                value[2] = str(int(value[2])/100.0)
                            # check if fan is on Man[0|]
                            if 'luefterstatus' in str(k) and int(value[2]) == 0:
                                print("# CRITICAL: luefterstatus is on Man[0], try to set it to AUTO")
                                ser.write(("130 5002 4\r\n").encode())
                                time.sleep(0.1)
                                value[2] = ser.readline().split()[2]
                                #print("luefterstatus.value " + str(int(ser.readline().split()[2]))
                                #ser.write(("130 1067\r\n").encode())
                                #time.sleep(0.1)
                            # print values
                            print k + " " + str(value[2])
                            # store or whatever correct value
                            REG[k] = str(value[2])
                            #file.write(k + " " + str(value[2]) + "\n")
                            #REG[k] = str(value[2])
                            # debug
                            #print k + "," + REG[k]
                            # flush input buffer, discarding all its contents
                        ser.flushInput()
                        # flush output buffer, aborting current output
                        ser.flushOutput()
                        break
                    else:
                        continue
                #time.sleep(0.5)
        ser.close()

        # Beschattung Winter/Sommer trigger
        if REG['beschattungaussentemp.value'] < REG['aussentemp.value']:
            REG['beschattungtemp.value'] = str(float(REG['beschattungtemp.value'])-0.5)
        else:
            REG['beschattungtemp.value'] = str(float(REG['beschattungtemp.value'])+1)

        # luefterstufe3-max
        REG['co2luefterstufe4.value'] = str(int(float(REG['co2luefterstufe3.value'])*1.2))
        # write to munin state file
        file = open("/var/lib/munin-node/plugin-state/dw.state", "w")
        for kf, vf in sorted(REG.items()):
            file.write(kf + " " + vf + "\n")
        file.close()
    except Exception, e1:
        print "error communicating...: " + str(e1)
else:
    print "cannot open serial port "

#EOF
