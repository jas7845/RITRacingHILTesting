from testing.ArduinoActions import *
from tkinter import *
from testing.GUIView import GUIView
from testing.CommandLineView import CommandLine
import sys
import threading
import os
import time

#  he imports other classes that i have not made yet, not sure if i need to do that


class GUIController:
    actions = None
    GUI_view = None
    logging = False;

    def __init__(self, master):
        if sys.argv[1] == "gui":
            self.GUI_view = GUIView(master, self)
        else:
            self.GUI_view = CommandLine(self)

        self.actions = ArduinoActions(sys.argv[2], sys.argv[3], self.GUI_view)
        readThread = threading.Thread(target=self.actions.run)
        readThread.start()
        if sys.argv[1] == "cmd":
            self.GUI_view.run()

        if sys.argv[1] == "gui":
            self.periodic_call()
        print("Set up")     # why

    def send_mult(self, filename):
        # self.actions.commandQueue.put(self.actions.command("sendMult", [filename]))
        try:
            with open(filename) as test_line:
                for line in test_line.readlines():
                    message = line;
                    toke = line.strip().split(',')
                    if len(toke) > 0 and toke[0][0:2] != "//":
                        if toke[0][0:3] == "SND" and self.check_msg(message):
                            self.actions.commandQueue.put(self.actions.command("send", message))
                        elif toke[0][0:3] == "CHK" and self.check_msg(message):
                            self.actions.commandQueue.put(self.actions.command("check", message))
                            # need something to carry out check function

        except FileNotFoundError:
            self.view.printMsg("File not found \n")
            return "fnf"

    def check_msg(self, message):
        split_msg = message.split()  # separates msg where the paces are to a list of words
        # at this point it has the message from the GUI Entry part
        if (split_msg[0] == "CHK") or (split_msg[0] == "SET"):
            if split_msg[1].isnumeric():
                if (split_msg[2] == "0") or (split_msg[2] == "1"):
                    return True;
                else:  # not 0 or 1 setting
                    self.GUI_view.printMsg("MSG is invalid, message must be 0 or 1")
            else:  # not valid pin number
                self.GUI_view.printMsg("MSG is invalid, pin must be a number")
        else:  # not valid Set or CHK
            self.GUI_view.printMsg("ID is invalid, must be SET or CHK")
        return False;

    def exec_tests(self, filename):
        self.actions.commandQueue.put(self.actions.command("execTests", [filename]))

    def end(self):
        self.actions.threadActive = False

    # checks if message formatted like a test and sends it
    # else checks if a file, run through file and send each send message and record each check message
    # formats the entry message, pushes a command to a queue in actions for test
    def send(self, msg):
        message = msg
        if self.check_msg(msg):
            self.actions.commandQueue.put(self.actions.command("send", message))
        elif os.msg.isfile(msg):  # check to see if the message is a file
            self.send_mult(msg)
        # at this point it has the message from the GUI Entry part


    def cancel_log(self):
        self.actions.commandQueue.put(self.actions.command("getCancel", []))

    def get_background(self):
        self.actions.commandQueue.put(self.actions.command("getBackground", [False]))

    def getN(self, n):
        inputCommand = self.actions.command("getN", [n])
        self.actions.commandQueue.put(inputCommand)

    # logs the command in the background, pushes it to queue
    def log(self):
        if self.logging:  # if logging then stop
            self.actions.commandQueue.put(self.actions.command("getCancel", []))
            self.logging = False;
        else:
            self.actions.commandQueue.put(self.actions.command("getBackground", [True]))
            self.logging = True;

    def idle(self):
        self.actions.idle()

    def end_send(self):
        self.actions.doSend = False
        print(self.actions.doSend)

    def periodic_call(self):
        self.GUI_view.handle_print()
        self.GUI_view.master.after(200, self.periodic_call)  # master was root


master = Tk()
controller = GUIController(master)
if sys.argv[1] == "gui":
    master.mainloop()
