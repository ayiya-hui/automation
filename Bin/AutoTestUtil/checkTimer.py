import Libs.sshHandler as sshHandler
import Util.timeUtility as timeUtility
import datetime
import time

class checkTimer:
    def __init__(self, host, user=False, pwd=False, ppt=False):
        self.localtime=None
        self.remotetime=None
        self.host=host
        self.user=user
        self.password=pwd
        self.prompt=ppt

    def compareTime(self):
        now=datetime.datetime.now()
        newNow, uNow, h1, h2=timeUtility.getTimeNow()
        timeHolder=newNow.ctime().split()
        timeHolder.insert(-1, time.strftime('%Z'))
        self.localtime=' '.join(timeHolder)
        self.remotetime=self.getRemotetime()
        if self.remotetime:
            rNow, rZone=timeUtility.getUTimeFromString(self.remotetime)
            print 'Local time: %s' % self.localtime
            print 'Remote time: %s' % self.remotetime
            reset=self.needReset(uNow, rNow)
            if reset:
                self.setRemotetime()
                self.compareTime()
        else:
            print 'No remote time received. Skip the time sync.'

    def needReset(self, local, remote):
        diff=abs(int(local)-int(remote))
        if diff>60:
            print 'Time is off over %i minute(s)' % int(diff/60)
            print 'reset the remote time.'
            return True
        else:
            print 'Time is sync (diff in %i seconds)' % int(diff)
            return False

    def getRemotetime(self):
        mySsh=sshHandler.SshHandler(self.host, user=self.user, password=self.password, prompt=self.prompt)
        value=mySsh.runCmd(['date'])
        myV=''
        if value:
            myV=value.split('\n')[1].strip().replace('  ',' ')

        return myV

    def setRemotetime(self):
        mySsh=sshHandler.SshHandler(self.host, user=self.user, password=self.password, prompt=self.prompt)
        value=mySsh.runCmd(['date -s "%s"' % self.localtime])


if __name__=='__main__':
    import sys
    server=sys.argv[1]
    myCheck=checkTimer(server)
    myCheck.compareTime()
    print 'task down'
