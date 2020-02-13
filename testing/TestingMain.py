import sys
import threading
from testing.TestArduino import *


def main():
    # 1 is port, 2 is baudrate
    TestArduino(sys.argv[1], sys.argv[2])

main()
