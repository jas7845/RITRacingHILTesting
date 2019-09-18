"""
Actions class interprets the actions in the command line
runs a separate thread to process info
uses command queue to pass info from command to arduino
command tuple: command and argument that gets pushed to the queue
"""

import datetime
import xlwt
import time
import serial
from collections import namedtuple
from queue import Queue

class arduino_actions():

    msg_line = 1
    arduinoData = None
    doInfiniteLog = False
    doSend = False
    threadActive = False
    commandQueue = Queue()  # queue that contains the commands
    command = namedtuple('command', 'cmd args')
    arduino_com = None
    baudrate = None
    view = None
    filter_active = None
    test = namedtuple('test', 'test_name test_op test_data test_timeout')

    filter_item = namedtuple('Filter', ['item', 'type'])
    filters = []

    def __init__(self, arudino_com, baudrate, view):
        self.arduino_com = arudino_com
        self.baudrate = baudrate
        self.view = view

    # sends message to the arduiono
    def send(self, msg):
        self.view.printMsg("Sent: " + msg + "\n")
        self.write_arduino((msg.strip('\n')).encode('utf-8'))


    def write_arduino(self, msg):
        self.arduinoData.write(msg)


    # Opens a file and sends an array of lines to send_mult
    def read_multiple(self, filename):
        with open(filename) as file:
            self.send_Mult(file.readlines())  # readlines returns a list of lines
        filename.close()    #I added this to his?


    # sends the message in the lines using send function
    def send_mult(self, msgs):
        for msg in msgs:
            if self.doSend:                 # doSend: bool we set false in the beginning
                if msg[0:5] == "delay":
                    delay_time = float(msg[6:])
                    time.sleep(0.003)
                else:
                    self.send(msg)
                    time.sleep(0.003)


    def get(self, msgNum):
        self.arduinoData.write('LOG'.encode('utf-8'))
        f = open("results.txt",  "w+")
        for i in range(int(msgNum)):
            get_msg = self.formattedRead(True)
            if get_msg != '':
                self.view.printMsg(get_msg.strip('\n'))
                f.write(get_msg)
        self.arduinoData.write('IDL'.encode('utf-8'))
        f.close()


    #continuously loop and read messages until you stop logging (bool set to false)
    def infiniteLog(self, doPrint):
        self.doInfiniteLog = True
        file = open("results.txt", "a")
        self.arduinoData.write('LOG'.encode('utf-8'))
        while self.doInfiniteLog:
            get_msg = self.formattedRead(True)
            if get_msg != "":
                file.write(get_msg)
                if doPrint:
                    self.view.printMsg(get_msg)
            self.handleCommands() #call handle command so it will go back tohandle command
        file.close()
        #self.arduinoData.write('IDL'.encode('utf-8'))

    def formattedRead(self, timeStamp):
        get_msg = self.arduinoData.readline()
        msg_txt = (get_msg.decode("utf-8")).strip(' \t\n\r')
        if self.filter_active and not self.filter_text(msg_txt):
            return ""
        if msg_txt != "":
            msg_txt = "0" + msg_txt.upper()
            if timeStamp:
                msg_txt = msg_txt + "   " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f') + "\n"
        return msg_txt

    #checks if the queue is empty
    #takes the  command from command touple and checks what they are
    #send command calls send  in actions for test which actually sends the message
    def handleCommands(self):
        if not self.commandQueue.empty():
            sent_command = self.commandQueue.get()
            if sent_command.cmd == "getN":
                self.get(sent_command.args[0])
            elif sent_command.cmd == "send":    # is a button on gui
                self.send(sent_command.args[0])
            elif sent_command.cmd == "sendMult":    #is a button on gui i got rid of this one b/c file loop?
                self.doSend = True
                self.send_multiple(sent_command.args[0])
            elif sent_command.cmd == "getCancel":
                self.doInfiniteLog = False
            elif sent_command.cmd == "getAll":
                self.get(-1)
            elif sent_command.cmd == "getBackground": #button log data logs it in the background, specifies where to log in the background
                if not self.doInfiniteLog: # function will passively log in the background
                    self.infiniteLog(sent_command.args[0])
            elif sent_command.cmd == "execTests":       # is a button on gui
                self.doSend= True
                self.exec_tests(sent_command.args[0])
            elif sent_command.cmd == "cancelSend":      # is a button on gui
                self.doSend=False
            return True
        else:
            return False

   def run(self):
        self.arduinoData = serial.Serial(self.arduino_com, self.baudrate, timeout=0.5)
        self.threadActive = True
        while self.threadActive:
            self.handleCommands() #infinite loop to keeps running commands


