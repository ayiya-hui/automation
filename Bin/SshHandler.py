try:
    import pexpect
except ImportError:
    print 'No pexpect module installed'


PROMPT='#'

class SshHandler:
    def __init__(self, host, user, password, prompt=None):
        self.host=host
        self.user=user
        self.password=password
        if prompt:
            self.prompt=prompt
        else:
            self.prompt=PROMPT
        self.cmd='ssh '+self.user+'@'+self.host
        self.conn=None

    def runCmd(self, preCmdList, condition=None, commandList=None):
        self.conn=pexpect.spawn(self.cmd)
        self.conn.expect('password:')
        self.conn.sendline(self.password)
        self.conn.expect(self.prompt)
        for command in preCmdList:
            self.conn.sendline(command)
            self.conn.expect(self.prompt)
        value=self.conn.before
        print value
        #value=self.__strip_output(self.conn.before)
        if condition and commandList:
            if condition in value:
                for cmd in commandList:
                    self.conn.sendline(command)
                    self.conn.expect(self.prompt)
                    value=self.__strip_output(self.conn.before)

        return value

    def logout(self):
        self.conn.close()


    def __strip_output(self, response):
        newline=[]
        temp=response.split('\r\n')
        temp.remove(temp[0])
        temp.remove(temp[-1])
        for line in temp:
            newline.append(line.strip())

        return ' '.join(newline)

