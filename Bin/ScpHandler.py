import pexpect

class ScpHandler:
    def __init__(self, host, user, password):
        self.host=host
        self.user=user
        self.password=password

    def putFile(self, source, dest):
        cmd='scp '+source+' '+self.user+'@'+self.host+':'+dest
        __execute(cmd)

    def putDir(self, source):
        cmd='scp -r '+source+' '+self.user+'@'+self.host+':'+dest
        self.__execute(cmd)

    def getFile(self, source):
        cmd='scp '+self.user+'@'+self.host+':'+source+' ./'
        self.__execute(cmd)

    def getDir(self, source):
        cmd='scp -r'+self.user+'@'+self.host+':'+source+' ./'
        self.__execute(cmd)

    def __execute(self, cmd):
        child=pexpect.spawn(cmd)
        child.expect('password:')
        child.sendline(self.password)
        child.expect(pexpect.EOF)
        child.close()
