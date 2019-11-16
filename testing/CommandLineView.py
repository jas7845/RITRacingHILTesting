"""
Will do everything through the command line rather than GUI
"""
import os.path
from os import path


class CommandLine:
    controller = None
    backgroundLogger = None
    currentlyThreading = False

    def __init__(self, controller):
        self.controller = controller

    def printMsg(self, msg):
        print(msg)

    def idle(self):

        while 1:
            print("Welcome to HIL tester. Type help to see a list of commands.")
            request = input(">")
            direction = request.split(" ")

            if self.controller.validate_command(request):
                self.controller.send(request)
            elif direction[0] == "GET":
                if len(direction) == 2:
                    if direction[1] == "-b":
                        if not self.currentlyThreading:
                            self.controller.get_background()
                    elif direction[1] == "-c":
                        self.controller.cancel_log()
                        #self.actions.idle()
                    else:
                        self.controller.getN(direction[1])
                        #self.actions.get(direction[1])
                else:
                    print("Not valid, please specify how many you would like")
            elif direction[0] == "LOG":  # is there a way to check if it is logging already
                self.controller.log()
            elif direction[0] == "IDLE":
                self.controller.idle()
            elif direction[0] == "help":
                print("SET/CHK [PORT] [0/1] will set a pin or check a pin")
                print("SND [PORT] [16 diget hex number] will end a CAN message")
                print("[filename] will send a list of commands located in a specific file")
                print("GET [N] will log the next N received messages on the screen and output to a text file")
                print("GET -b will log all messages to a text file in the background")
                print("GET -c will cancel a background log")
                print("LOG will continuously log messages. Not recommended because you cant leave this mode")
                # confused between get and check functions, they  are different, is GET only for the
                #   command line / gui? but then what is check

    # why is this method even here
    def handle_print(self):
        print("Nothing")

    def run(self):
        self.idle()

