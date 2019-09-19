
#formats the  message, pushes a command to a queue in actions for test
def send(msg):   # should have self
    split_msg = msg.split()         # separates msg where the paces are to a list of words
    if (split_msg[0] == "CHK") or (split_msg[0] == "SET"):      # checks first word in  three letters  (CHK or  SET)
        if split_msg[1].isnumeric():
            if(split_msg[2] == "0") or  (split_msg[2] == "1"):# pin number should be less than than 100
                #self.actions.commandQueue.put(self.actions.command("send", ["SND " + msg.upper()]))
                print("your message is properly formatted!")
            else:
                print("not 0 or 1")
                #self.GUI_view.printMsg("MSG is invalid, message must be 0 or 1")
        else:
            print("Not a valid  pin number")
                #self.GUI_view.printMsg("MSG is invalid, pin must be a number")
    else:
        print("not a valid command; SET or CHK")
            #self.GUI_view.printMsg("ID is invalid, must be 3 hex characters")

def main():
    messages = ["SET 01 1", "CHK 23 0", "CHK ab 1", "SET 02 3"]
    for msg in messages:
        send(msg)

main()

