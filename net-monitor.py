import time
import psutil
import json
import urllib.request
import requests
import sys

import subprocess

class Converter:
    def __init__(self):
        pass

    def toMegabytes(self, value):
        return value/1024./1024.*4

    def toKilobytes(self, value):
        return value/1024.*2


class Error(Exception):
    '''
        Base class for exceptions.
    '''
    pass

class ConnectionError(Error):

    def __init__(self):
        self.message = ": device is not connected to any network"

    def throwError(self):
        return self.__class__.__name__ + self.message


class BandwidthMonitor:

    def __init__(self):
        # variables
        self.old_value = 0
        self.total = 0
        self.path = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"]
        self.connected = None
        self.conv = Converter()
        self.init = False
        self.NOT_NOTIFIED = True
        self.previous = None

    def isConnected(self):
        ''' 
            Returns 'True' if the device is 
            connected to any wireless 
            network.

            Else, returns 'False'
        '''
        output = str(subprocess.check_output(self.path))
        if 'Off' in output:
            return False

        return True

    def isSwitched(self):
        return self.getSSID() != self.previous and self.previous != None

    def getSSID(self):
        '''
            Returns the SSID of the
            wireless netowork the device
            is connected to.
        '''

        if not self.isConnected():
            try:
                raise ConnectionError
            except Error as err:
                print ( err.throwError() )
                exit()

        output = str(subprocess.check_output(self.path))
        toFind = ' SSID: '

        try:
            index = output.index(toFind)
        except:
            return self.getSSID()

        name = ""
        index += len(toFind)
        char = output[index]

        while char != '\\' :
            name += char
            index += 1
            char = output[index]

        return name

    def resetVals(self):
        self.old_value = 0
        self.total = 0
        # self.previous = self.getSSID()
        # self.connected = self.isConnected()

    def write(self, message):
        sys.stdout.write(str(message) + "\n")
        sys.stdout.flush()

    def updateInfo(self, delay=3):
        '''
            Updates the bandwidth usage
            and the estimated download speed, 
            per 'delay' seconds.

            By default, delay is 3 seconds.
        '''
        notifs = 0

        if not self.isConnected():
            try:
                raise ConnectionError
            except Error as err:
                print (err.throwError())

        while self.isConnected():


            new_value = psutil.net_io_counters().bytes_recv 
            dif = new_value - self.old_value


            if self.old_value:
                self.total += dif
                # if self.conv.toMegabytes(self.total) > 1 and self.NOT_NOTIFIED:
                #     self.NOT_NOTIFIED = False
                #     self.write('OverLimit')
        

            self.old_value = new_value

            command = sys.stdin.readline()
            command = command.split('\n')[0]
            if command == "send-info":
                # sys.stdout.write(str(convert_to_mbit(total)) + "\n")
                # sys.stdout.flush()
                self.write(self.conv.toMegabytes(self.total))

            if self.isSwitched():
                break

            time.sleep(delay)

        self.write("DISCON")
        return 


    def listenForConnection(self, delay=3):
        '''
            Checks if the device has 
            connected to any network
            per 'delay' seconds.

            By default, delay is 3 seconds.
        '''

        while not self.isConnected():
            time.sleep(delay)

        if not self.init:
            self.init = True

        ssid = self.getSSID()
        if ssid == '':
            return self.listenForConnection()
        self.previous = ssid
        self.write("CON:" + str(self.getSSID()))
        return

    def run(self, delay=3):
        time.sleep(delay)
        self.write("Listening...")
        self.listenForConnection()

        while self.init:
            # if self.isSwitched():
            #     self.write("Switching...")
            #     self.listenForConnection()
            #     self.write("Switched")
            if self.isConnected() and not self.isSwitched():
                self.write("Connected...")
                self.updateInfo()
                self.resetVals()
            else:
                self.write("Listening...")
                self.listenForConnection()
            time.sleep(delay)



if __name__ == '__main__':
    bm = BandwidthMonitor()
    bm.run()
