import string


# formats the  message, pushes a command to a queue in actions for test
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


def fix_string(message):
    string_message = str(message)
    for i in range(len(message)):
        print(message[i])
        if message[i] > 200:
            print(message[i] >> 5)
    print(message)
    return message


def main():
    # Serial.println : Prints data to the serial port as human-readable ASCII text followed by a carriage return character
    # (ASCII 13, or '\r') and a newline character (ASCII 10, or '\n')

    # The line terminator is always b'\n' for binary files

    o1 = b'\x17\x16\xebC\xe1setup\r\n'  # message should be set up, what does the rest of it mean
    #o.decode("utf-8")                  # has invalid continuation bytes on xeb in position 2, basically the
                                        # number (eb = 235) is not a  unicode character
    print((fix_string(o1).decode("utf-8")).strip(' \t\n\r'))
    o2 = b'\x17\x16\x11C\x11setup\r\n'
    # b'R\xd1\x8b\n'       b't\xabhVH\xf8setup\r\n'    b' \x16oH\xf8.\x00;\xe6setup\r\n'
    o3 = b'\xf7setup\r\n'
    o4 = b'\x17setup\r\n'
    #print((o4.decode("utf-8")).strip(' \t\n\r'))


main()
