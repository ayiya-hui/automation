import os
import time

def checkPHStatus(interval, fileName):
    fileHandle=open(fileName, 'w')
    while 1:
        lines=cmdReturn('phstatus.sh')
        for line in lines:
            fileHandle.write(line)
        time.sleep(interval)

def cmdReturn(cmd):
    fin, fout=os.popen4(cmd)
    lines=fout.readlines()

    return lines

if __name__=='__main__':
    import sys
    checkPHStatus(float(sys.argv[1]), sys.argv[2])
