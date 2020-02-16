
import datetime
import time
import serial
from collections import namedtuple
import queue
import sys


class TestArduino():

    msg_line = 1
    arduinoData = None
    doInfiniteLog = False
    doSend = False
    threadActive = False
    commandQueue = queue.Queue(100)  # queue that contains the commands
    command = namedtuple('command', 'cmd args')
    arduino_com = None
    baudrate = 0
    port = None
    view = None
    filter_active = None
    test = namedtuple('test', 'test_name test_op test_data test_timeout')

    filter_item = namedtuple('Filter', ['item', 'type'])
    filters = []

    def __init__(self, arudino_com, baudrate):
        self.arduino_com = arudino_com
        self.baudrate = baudrate
        # changed so that i can try to run it and see if it works

    def write_arduino(self, msg):
        self.arduinoData.write((msg.strip('\n')).encode('utf-8'))
        time.sleep(2)  # added so that it wouldnt send them all at the same time

    def formatted_read(self, time_stamp):  # had argument "timeStamp"
        # commented out for testing :
        msg_txt = ""
        #while self.arduinoData.in_waiting:
        #    pass
        get_msg = self.arduinoData.readline()
        msg_txt = (get_msg.decode("utf-8")).strip(' \t\n\r')
        return msg_txt

    '''
    def run(self):
        self.arduinoData = serial.Serial(self.baudrate, self.port, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.arduinoData.reset_input_buffer()
        self.threadActive = True
        while self.threadActive:
            self.main()  # infinite loop to keep running commands
    '''

    @property
    def handleCommands(self):
        keep_going = True
        print("Input: ")
        while keep_going:

            request = input(">")
            direction = request.split(" ")
            if direction[0] == "SND":
                self.write_arduino(request)
                time.sleep(2)
            elif direction[0] == "CHK":
                print("Output: " +self.formatted_read(False))
            else:
                keep_going = False

    def run(self):
        print("run")
        self.arduinoData = serial.Serial(self.arduino_com, self.baudrate, timeout=0.5, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
        self.arduinoData.reset_input_buffer()
        self.threadActive = True
        while self.threadActive:
            self.handleCommands  # infinite loop to keep running commands

