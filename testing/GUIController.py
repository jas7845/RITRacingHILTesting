import ActionsForTest
from tkinter import *
from GUIView import GUI_View
from CommandLineView import commandline
import sys
import threading
import time

#  he imports other classes that i have not made yet, not sure if i need to do that


class GUI_Controller:
    actions = None
    GUI_View = None
    def __init__(self, master):
        if sys.argv[1] == "gui":
            self.GUI_view = GUI_View(master, self)
        else:
            self.GUI_view = commandline(self)

        self.actions = ArduinoActions(sys.argv[2], sys.argv[3], self.GUI_view)
        readThread = threading.Thread(target=self.actions.run)
        readThread.start()
        if sys.argv[1] == "cmd":
            self.GUI_view.run()

        if sys.argv[1] == "gui":
            self.periodic_call()
        print("Set up")     # why

    def exec_tests(self, filename):
        self.actions.commandQueue.put(self.actions.command("execTests", [filename]))

    def end(self):
        self.actions.threadActive = False

    # formats the  message, pushes a command to a queue in actions for test
    def send(self, msg):
        message = msg
        split_msg = msg.split()         # separates msg where the paces are to a list of words
        if (split_msg[0] == "CHK") or (split_msg[0] == "SET"):
            if split_msg[1].isnumeric():
                if(split_msg[2] == "0") or (split_msg[2] == "1"):
                    self.actions.commandQueue.put(self.actions.command("send", message))
                else:  # not 0  or 1 setting
                    self.GUI_view.printMsg("MSG is invalid, message must be 0 or 1")
            else:  #not  valid pin number
                self.GUI_view.printMsg("MSG is invalid, pin must be a number")
        else:   # not valid Set or CHK
            self.GUI_view.printMsg("ID is invalid, must be SET or CHK")

    def cancel_log(self):
        self.actions.commandQueue.put(self.actions.command("getCancel", []))

    def get_background(self):
        self.actions.commandQueue.put(self.actions.command("getBackground", [False]))

    def getN(self, n):
        inputCommand = self.actions.command("getN", [n])
        self.actions.commandQueue.put(inputCommand)

    # logs the command ind tha background, pushes it to queue
    def log(self):
        self.actions.commandQueue.put(self.actions.command("getBackground", [True]))

    def idle(self):
        self.actions.idle()

    def end_send(self):
        self.actions.doSend = False
        print(self.actions.doSend)

    def periodic_call(self):
        self.GUI_view.handle_print()
        self.GUI_view.root.after(200, self.periodic_call)

root = Tk()
controller = GUI_Controller(root)
if sys.argv[1] == "gui":
    root.mainloop()
