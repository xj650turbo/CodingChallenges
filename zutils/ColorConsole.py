# this file defines colors for common console output

from enum import StrEnum

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