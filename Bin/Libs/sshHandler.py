try:
    import pexpect
except ImportError:
    print 'No pexpect module installed'

default_user='root'
default_password='ProspectHills'
default_prompt='#'
exp_deny='Permission denied'
cmd='ssh -o stricthostkeychecking=no %s@%s'

class SshHandler:
    def __init__(self, host, user=False, password=False, prompt=False):
        self.host=host
        if user:
            self.user=user
        else:
            self.user=default_user
        if password:
            self.password=password
        else:
            self.password=default_password
        if prompt:
            self.prompt=prompt
        else:
            self.prompt=default_prompt
        self.cmd=cmd % (self.user, self.host)
        self.conn=None

    def runCmd(self, cmdList):
        value=''
        self.conn=pexpect.spawn(self.cmd)
        h=self.conn.expect([pexpect.TIMEOUT, pexpect.EOF, 'password:'])
        if h==0:
            print 'connection time out'
        elif h==1:
            print 'EOF condtion. Cannot talk to %s' % self.host
        elif h==2:
            self.conn.sendline(self.password)
            i=self.conn.expect([exp_deny, pexpect.TIMEOUT, pexpect.EOF, self.prompt])
            if i==0:
                print 'Permission denied due to wrong password'
            elif i==1:
                print 'time out for log in'
            elif i==2:
                print 'EOF condition. Cannot talk to %s' % self.host
            elif i==3:
                for command in cmdList:
                    self.conn.sendline(command)
                    j=self.conn.expect([pexpect.TIMEOUT, pexpect.EOF, self.prompt])
                    if j==0:
                        print 'timeout: %s' % command
                    elif j==1:
                        print 'EOF condition. Cannot talk to host %s' % self.host
                    elif j==2:
                        value=self.conn.before
        return value

    def logout(self):
        self.conn.close()




