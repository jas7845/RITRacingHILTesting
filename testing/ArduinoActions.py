"""
Actions class interprets the actions in the command line
runs a separate thread to process info
uses command queue to pass info from command to arduino
command tuple: command and argument that gets pushed to the queue
"""

import datetime
import time
import serial
from collections import namedtuple
import queue

class ArduinoActions():

    msg_line = 1
    arduinoData = None
    doInfiniteLog = False
    doSend = False
    threadActive = False
    commandQueue = queue.Queue(100)  # queue that contains the commands
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
        # changed so that i can try to run it and see if it works
        self.view = view

    # sends message to the arduiono
    def send(self, msg):
        print("send in AA " + msg)
        self.view.printMsg("Sent: " + msg + "\n")
        # can msg should be something like 'SND CHK 002 0000000000000005' according to his
        self.write_arduino((msg.strip('\n')).encode('utf-8'))

    def set(self, msg):
        print("set in AA " +msg)
        self.view.printMsg("Set Sent: " + msg + "\n")
        self.write_arduino((msg.strip('\n')).encode('utf-8'))

    def checkCAN(self, msg, timeout):
        print("check in AA " + msg)
        self.view.printMsg("Checking: " + msg + "\n")
        result = self.check_responses(msg, timeout)
        if result != "success":
            self.view.printMsg("Failed test: " + msg + "\n failed on: " + result + "\n")
        else:
            self.view.printMsg("Test: " + msg + " succeeded \n")

    def write_arduino(self, msg):
        self.arduinoData.write(msg)

        # send the message via serial to the main

    # sends the message in the lines using send function
    def send_mult(self, msgs):
        for msg in msgs:
            if self.doSend:  # doSend: bool we set false in the beginning
                if msg[0:5] == "delay":
                    delay_time = float(msg[6:])
                    time.sleep(0.003)
                else:
                    self.send(msg)
                    time.sleep(0.003)

    # Opens a file and sends an array of lines to send_mult
    def read_multiple(self, filename):
        with open(filename) as file:
            self.send_Mult(file.readlines())  # readlines returns a list of lines
        filename.close()    # I added this to his?

    # writes the message to a file "results.txt"
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

    # continuously loop and read messages until you stop logging (bool set to false)
    # write the results to "results.txt"
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
            self.handleCommands  # call handle command so it will go back to handle command
        file.close()
        self.arduinoData.write('IDL'.encode('utf-8'))

    # has stuff about the filter that needs to get rid of
    # Think this is getting data from the arduino and formatting it
    # TODO: change for send and set messages -- do we even need this?
    def formattedRead(self, timeStamp):
        # commented out for testing :
        # get_msg = self.arduinoData.readline()
        # msg_txt = (get_msg.decode("utf-8")).strip(' \t\n\r')
        get_msg = self.commandQueue.get()
        self.commandQueue.put(get_msg)
        msg_txt = get_msg.cmd

        # if self.filter_active and not self.filter_text(msg_txt):
        #    return ""
        if msg_txt != "":
            msg_txt = "0" + msg_txt.upper()
            if timeStamp:
                msg_txt = msg_txt + "   " + datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f') + "\n"
        return msg_txt

    # handles send and check messages?
    def exec_tests(self, filename):
        print("Doing tests")
        self.view.printMsg("-------------Test------------\n")
        test_list = self.read_test_file(filename)  # returns a list of tests
        if test_list == "fnf":  # file not found
            return
        for test in test_list:
            if self.doSend:
                print(self.doSend)
                curr_test_name = test.test_name
                if test.test_op == "send":
                    self.send_Mult(test.test_data)
                elif test.test_op == "check":
                    # check responses takes a response list and timeout
                    result = self.check_responses(test.test_data, test.test_timeout)
                    if result != "success":
                        self.view.printMsg("Failed test: " + curr_test_name + "\n failed on: " + result + "\n")
                    else:
                        self.view.printMsg("Test: " + curr_test_name + " succeeded \n")

    # Not really sure what this is doing, should be comparing the received messages with the response
    #    list but  im not sure how, something to do with "X" in the string
    def check_responses(self, response_list, timeout):
        got_all_messages = False
        start_time = time.time()
        while not got_all_messages and (time.time()-start_time) <= timeout:
            received_msg = self.formattedRead(False).strip('|')
            msg_to_remove = []
            # To compare each message we need to split the ID and message into their respective hex values
            if received_msg != "":
                id = received_msg.split(' ')[0]     # send or check
                msg = received_msg.split(' ')[1]    # which pin to go to
                self.view.printMsg("received: " + received_msg + "\n")
                for i in range(len(response_list)):
                    check_id = response_list[i].split(' ')[0]
                    check_msg = response_list[i].split(' ')[1]
                    msg_match = True
                    if check_id == id:
                        for j in range(len(msg)):
                            if check_msg[j] != "X":
                                if check_msg[j] != msg[j]:
                                    msg_match = False
                        if msg_match:
                            msg_to_remove.append(response_list[i])
                for i in msg_to_remove:
                    response_list.remove(i)
                # This line will remove a response from a list if it is in the response list
                # response_list[:] = [checkMsg for checkMsg in response_list if not (int(checkMsg.split(' ')[0], 16) == idVal
                #                                                                    and int(checkMsg.split(' ')[1], 16) == msgVal)]
        if len(response_list) == 0:
            return "success"
        else:
            return response_list[0]

    def idle(self):
        self.view.printMsg("Idle\n")
        self.arduinoData.write('IDL'.encode('utf-8'))

    def log_loop(self):
        self.write_arduino('LOG'.encode())
        with open("results.txt", "w+") as file:
            while True:
                msg = self.formattedRead(True)
                file.write(msg)
                self.view.printMsg(msg.strip('\n'))

    # checks if the queue is empty
    # takes the  command from command touple and checks what they are
    # send command calls send  in actions for test which actually sends the message
    @property
    def handleCommands(self):
        # TODO: edit execTests and send and sendMult to comply w new controller
        if not self.commandQueue.empty():
            sent_command = self.commandQueue.get()

            if type(sent_command) is str:
                print("type string: " + sent_command)
                return False
            else:
                print(sent_command)

            if sent_command.cmd == "getN":
                self.get(sent_command.args[0])          # writes data to results.txt file
            elif sent_command.cmd == "send":            # is a button on gui
                self.send(sent_command.args)
            elif sent_command.cmd == "set":
                self.set(sent_command.args)
            elif sent_command.cmd == "check":
                self.checkCAN(sent_command.args, 2)  #should be different but how
            elif sent_command.cmd == "checkCAN":
                self.checkCAN(sent_command.args, 2)
            elif sent_command.cmd == "getCancel":
                self.doInfiniteLog = False
            elif sent_command.cmd == "getAll":          # am not using
                self.get(-1)
            elif sent_command.cmd == "getBackground":   # button log data logs it in the background, specifies where to log in the background
                if not self.doInfiniteLog:
                    self.infiniteLog(sent_command.args[0])# function will passively log in the background
            elif sent_command.cmd == "cancelSend":  # is a button on gui
                self.doSend = False
            # do not think i need these two:
            """elif sent_command.cmd == "sendMult":        # is a button on gui i got rid of this one b/c file loop?
                self.doSend = True
                self.send_multiple(sent_command.args[0])
            elif sent_command.cmd == "execTests":       # is a button on gui
                self.doSend= True
                self.exec_tests(sent_command.args[0])   # what is exec tests v send? i guess send has less functionality
            """
            return True
        else:
            return False

    def run(self):
        self.arduinoData = serial.Serial(self.arduino_com, self.baudrate, timeout=0.5)
        self.threadActive = True
        while self.threadActive:
            self.handleCommands  # infinite loop to keep running commands

