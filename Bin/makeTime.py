import datetime
import time

DAY=["Day", "Days", "day", 'days']
HOUR=["Hour", "Hours", "hour", "hours"]
MINUTE=["Minute", "Minutes", "minute", "minutes"]

def MakeTime(startTime, endTime):
    timeParam={}
    duration=''
    startParam=startTime.split(" ")
    if startParam[1] in DAY:
        duration=startParam[0]+'d'
        sDelta=datetime.timedelta(int(startParam[0]))
    elif startParam[1] in HOUR:
        duration=startParam[0]+'h'
        sDelta=datetime.timedelta(0,0,0,0,0,int(startParam[0]))
    elif startParam[1] in MINUTE:
        duration=startParam[0]+'m'
        sDelta=datetime.timedelta(0,0,0,0,int(startParam[0]))
    else:
        print "Time Unit is not correct. Exit."
        exit()
    endParam=startTime.split(" ")
    if endParam[1] in DAY:
        eDelta=datetime.timedelta(int(endParam[0]))
    elif endParam[1] in HOUR:
        eDelta=datetime.timedelta(0,0,0,0,0,int(endParam[0]))
    elif endParam[1] in MINUTE:
        eDelta=datetime.timedelta(0,0,0,0,int(endParam[0]))
    else:
        print "Time Unit is not correct. Exit."
        exit()

    eTimeNow=datetime.datetime.now()-eDelta
    sTimeNow=eTimeNow-sDelta

    sTimeParam={}
    sTimeParam['cTime']=sTimeNow.isoformat(" ").split(".")[0]
    sTimeParam['uTime']=str(int(time.mktime(sTimeNow.timetuple())))

    eTimeParam={}
    eTimeParam['cTime']=eTimeNow.isoformat(" ").split(".")[0]
    eTimeParam['uTime']=str(int(time.mktime(eTimeNow.timetuple())))

    timeParam['startTime']=sTimeParam
    timeParam['endTime']=eTimeParam
    timeParam['duration']=duration

    return timeParam




