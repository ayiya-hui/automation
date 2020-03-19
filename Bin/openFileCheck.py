import os
from socket import *
import datetime

CMD="ps -ef | grep java | grep PELaunch | grep -v grep | awk '{print $2}'"
CMD1='ls /proc/$PID/fd | wc -l'
DEFAULT_PORT=514
NORMAL='PHL_INFO'
ALERT='PHL_ALERT'
MSG=': [PH_DEV_MON_PROC_FD_COUNT]:[eventSeverity]=$LEVEL, [procName]=glassfish, [reptDevIpAddr]=$LOCALHOST, [hostIpAddr]=$LOCALHOST, [hostName]=$LOCALNAME, [fdCount]=$COUNT'



def openFileCheck():
    f=os.popen(CMD)
    pid=f.readline().strip()
    f=os.popen(CMD1.replace('$PID', pid))
    count=f.readline().strip()
    localname=gethostname()
    localhost=gethostbyname(localname)
    sock=socket(AF_INET, SOCK_DGRAM)
    sock.connect((localhost, DEFAULT_PORT))
    if int(count)>800:
        level=ALERT
    else:
        level=NORMAL
    msg=MSG.replace('$LEVEL', level).replace('$LOCALHOST', localhost).replace('$LOCALNAME', localname).replace('$COUNT', count)
    now=datetime.datetime.now().ctime()
    sock.sendall(now+msg)
    sock.close()



if __name__=='__main__':
    openFileCheck()
