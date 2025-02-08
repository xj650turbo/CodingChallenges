# this file defines colors for common console output 
# and defines convenience functions:
# - colorString() - outputs a strinmg in color
# - isJupyter() - determines whether we're runing under Jupyter
# - clearOutput() - clears output for both console and Jupyter

import os
import sys
from enum import StrEnum
from IPython.display import clear_output


class ColorCodes(StrEnum):
    #dark colors
    Black   = '\033[30m'
    RRed    = '\033[31m'
    GGreen  = '\033[32m'
    YYellow = '\033[33m'
    BBlue   = '\033[34m'
    MMagenta= '\033[35m'
    CCyan   = '\033[36m'
    WWhite  = '\033[37m'
    #bright colors
    Grey    = '\033[90m'
    Red     = '\033[91m'
    Green   = '\033[92m'
    Yellow  = '\033[93m'
    Blue    = '\033[94m'
    Magenta = '\033[95m'
    Cyan    = '\033[96m'
    White   = '\033[97m'
    Reset   = '\033[0m'


def colorString(item, color):
    return color + str(item) + ColorCodes.Reset


def isJupyter():
    return 'ipykernel' in sys.modules
     

def clearOutput(wait = True):
    if isJupyter():
        clear_output(wait=wait)
    else:
        os.system('cls')