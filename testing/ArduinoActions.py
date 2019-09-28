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
from serial import Serial


class ArduinoActions():

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
        filename.close()    #I added this to his?

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
            self.handleCommands  #call handle command so it will go back to handle command
        file.close()
        #self.arduinoData.write('IDL'.encode('utf-8'))

    # has stuff about the filter that needs to get rid of
    # Think this is getting data from the arduino and formatting it
    def formattedRead(self, timeStamp):
        get_msg = self.arduinoData.readline()
        msg_txt = (get_msg.decode("utf-8")).strip(' \t\n\r')
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
        test_list = self.read_test_file(filename)
        if test_list == "fnf":  # file not found
            return
        for test in test_list:
            if self.doSend:
                print(self.doSend)
                curr_test_name = test.test_name
                if test.test_op == "send":
                    self.send_Mult(test.test_data)
                elif test.test_op == "check":
                    result = self.check_responses(test.test_data, test.test_timeout)
                    if result != "success":
                        self.view.printMsg("Failed test: " + curr_test_name + "\n failed on: " + result + "\n")
                    else:
                        self.view.printMsg("Test: " + curr_test_name + " succeeded \n")

    # Not really sure what this is doing, should be comparing the received messages with the response
    #   list but  im not sure how, something to do with "X" in the string
    def check_responses(self, response_list, timeout):
        got_all_messages = False
        start_time = time.time()
        while not got_all_messages and (time.time()-start_time) <= timeout:
            received_msg = self.formattedRead(False).strip('|')
            msg_to_remove = []
            # To compare each message we need to split the ID and message into their respective
            # hex values
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

    # most of this is based on the way that the file / strings are formatted - not sure how to do that
    # what is /send vs send, /check vs check and /test vs test?
    def read_test_file(self, filename):
        tests = []
        try:
            with open(filename) as test_line:
                in_test = False
                in_sending = False
                in_checking = False
                msg_to_send = []
                msg_to_check = []
                test_name = ""
                timeout = 1
                for line in test_line.readlines():
                    split = line.strip().split(',')
                    if len(split) > 0:
                        if split[0][0:2] != "//":  # not sure why this is here
                            if in_test:
                                if in_sending:
                                    if split[0][1:len(split[0]) - 1] != "/send":
                                        if split[0][0:3] == "SND" or split[0][0:3] == "del":
                                            msg_to_send.append(split[0][0:24].strip())
                                    else:
                                        tests.append(self.test(test_name=test_name, test_op="send", test_data=msg_to_send, test_timeout=0))
                                        msg_to_send = []
                                        in_sending = False
                                elif in_checking:
                                    if split[0][1:len(split[0]) - 1] != "/check":
                                        check = split[0][0:20]
                                        msg_to_check.append(check)
                                    else:
                                        tests.append(self.test(test_name=test_name, test_op="check", test_data=msg_to_check, test_timeout=timeout))
                                        in_checking = False
                                        msg_to_check = []
                                elif split[0][1:len(split[0]) - 1] == "send":
                                    in_sending = True
                                elif split[0][1:] == "check":
                                    in_checking = True
                                    timeout = float(split[1][8:len(split[1]) - 1])
                                elif split[0][1:len(split[0]) - 1] == "/test":
                                    in_test = False
                                    msg_to_send = []
                                    msg_to_check =[]
                            else:
                                if split[0][1:] == "test":
                                    test_name = split[1][10:len(split[1]) - 2]
                                    in_test = True
            return tests
        except:
            self.view.printMsg("File not found \n")
            return "fnf"

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

    #checks if the queue is empty
    #takes the  command from command touple and checks what they are
    #send command calls send  in actions for test which actually sends the message
    @property
    def handleCommands(self):
        if not self.commandQueue.empty():
            sent_command = self.commandQueue.get()
            if sent_command.cmd == "getN":
                self.get(sent_command.args[0])
            elif sent_command.cmd == "send":            # is a button on gui
                self.send(sent_command.args[0])
            elif sent_command.cmd == "sendMult":        # is a button on gui i got rid of this one b/c file loop?
                self.doSend = True
                self.send_multiple(sent_command.args[0])
            elif sent_command.cmd == "getCancel":
                self.doInfiniteLog = False
            elif sent_command.cmd == "getAll":          # am not using
                self.get(-1)
            elif sent_command.cmd == "getBackground":   # button log data logs it in the background, specifies where to log in the background
                if not self.doInfiniteLog:              # function will passively log in the background
                    self.infiniteLog(sent_command.args[0])
            elif sent_command.cmd == "execTests":       # is a button on gui
                self.doSend= True
                self.exec_tests(sent_command.args[0])   # what is exec tests vs send? i guess send has lessfunctionality
            elif sent_command.cmd == "cancelSend":      # is a button on gui
                self.doSend=False
            return True
        return False

    def run(self):
        self.arduinoData = serial.Serial(self.arduino_com, self.baudrate, timeout=0.5)
        self.threadActive = True
        while self.threadActive:
            self.handleCommands  #infinite loop to keeps running commands


