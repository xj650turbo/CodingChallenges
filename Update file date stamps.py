import os
import time
from datetime import datetime

update = False
directory = "\\\\zcloud\\video\\Quadcopter\\ttt"

logFileName = os.path.join(directory, "aaa_log.csv")
logFile = open(logFileName, 'w')
logFile.write("Updated?, Original Last Modified, Date from file name, File name, new file name, New last updated, x, y, z, z, z, z, z\n")

files = os.listdir(directory)


for file in files:
    fullFilePath = os.path.join(directory, file)
    if os.path.isfile(fullFilePath):
        lastModified = os.stat(fullFilePath).st_mtime
        hrTime = time.ctime(lastModified)    
        dt = datetime.fromtimestamp(lastModified) # create datetime object
        dtFormatted = dt.strftime("%Y/%m/%d")

        split = file.split(" ")
        dateTS = split[0]
        if len(dateTS) == 6 and dateTS.isdigit():
            dateTS = "20" + dateTS[0:2] + "/" + dateTS[2:4] + "/" + dateTS[4:6]
            tupleNameTs_FileTs = (dateTS, dtFormatted)
            updateNeeded = dateTS != dtFormatted
            logFile.write(("+," if updateNeeded else "-,"))
            logFile.write(str(dateTS) + ",")
            logFile.write(str(dtFormatted) + ",")
            logFile.write(file + ",")

            print(("+ " if updateNeeded else "- "), end=" ")
            print(tupleNameTs_FileTs, end=" ")
            print(file)
            newFileName = " ".join(split[1:])
            extSplit = newFileName.split(".")
            newFileName = f"{extSplit[0]} {tupleNameTs_FileTs[0].replace('/', '-')}.{extSplit[1].lower()}"
            newFullFilePath = os.path.join(directory, newFileName)
            print(fullFilePath, newFullFilePath)
            logFile.write(newFileName + ",")
            if update:
                os.rename(fullFilePath, newFullFilePath)
            if updateNeeded:
                targetYMD = tupleNameTs_FileTs[0].split("/")
                targetDate = datetime(year=int(targetYMD[0]), month=int(targetYMD[1]), day=int(targetYMD[2]), hour=0, minute=0, second=0)
                targetTimestamp = time.mktime(targetDate.timetuple())
                print(targetDate, targetTimestamp)
                logFile.write(str(targetDate) + ",")
                if update:
                    os.utime(newFullFilePath, (targetTimestamp, targetTimestamp))
            else:
                targetTimestamp = lastModified
                print(dt, targetTimestamp)
                logFile.write(str(hrTime) + ",")
                if update:
                    os.utime(newFullFilePath, (targetTimestamp, targetTimestamp))

            logFile.write("\n")

logFile.close()

