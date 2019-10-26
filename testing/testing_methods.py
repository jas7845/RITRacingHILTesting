import string

#formats the  message, pushes a command to a queue in actions for test
def check_msg(message):
    split_msg = message.split()  # separates msg where the paces are to a list of words
    # at this point it has the message from the GUI Entry part
    if (split_msg[0] == "CHK") or (split_msg[0] == "SET"):
        if split_msg[1].isnumeric():
            if (split_msg[2] == "0") or (split_msg[2] == "1"):
                print(message + " valid")
                return True;
            else:  # not 0 or 1 setting
                print("MSG is invalid, message must be 0 or 1")
        else:  # not valid pin number
            print("MSG is invalid, pin must be a number")
    elif split_msg[0] == "SND":
        if len(split_msg[1]) == 16 and all(c in string.hexdigits for c in split_msg[1]):  # len(split_msg[1]) == 16 and
            print(message + " valid")
            return True;
        else:
            print("Message is not hex " + message)
    else:  # not valid SET or CHK
        print("ID is invalid, must SET a pin, SND a CAN message, or CHK a message")
    return False;


def main():
    messages = ["SET 01 1", "CHK 23 0", "CHK ab 1", "SET 02 3", "SND 000000000000000A", "SND 0A"]
    for msg in messages:
        check_msg(msg)

main()

