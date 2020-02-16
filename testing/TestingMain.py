import sys
import threading
from testing.TestArduino import *

actions = None

def main():
    # 1 is port, 2 is baudrate
    print("it")
    actions = TestArduino(sys.argv[1], sys.argv[2])
    readThread = threading.Thread(target=actions.run)
    readThread.start()


main()