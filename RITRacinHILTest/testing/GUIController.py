from ActionsForTest import *
from tkinter import *
from GUIView import GUI_View
from CommandLineView import commandline
import sys
import threading
import time

#  he imports other classes that i have not made yet, not sure if i need to do that

class GUIController:
    actions = None
    GUI_View = None
    def __init__(self, master):
        if sys.argv[1] == "gui":
            self.GUI_view = GUI_View(master, self)
        else:
            self.GUI_view = commandline(self)

        self.actions = arduino_actions(sys.argv[2], sys.argv[3], self.GUI_view)
        readThread = threading.Thread(target=self.actions.run)
        readThread.start()
        if sys.argv[1] == "cmd":
            self.GUI_view.run()

        if sys.argv[1] == "gui":
            self.periodic_call()
        print("Set up")     # why

