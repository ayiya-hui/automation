import telnetlib

class telnetHandler:
    """This class will take a target IP address, a user name, and a password, then handle a telnet session."""
    def __init__(self, target, user, password):
        self.host=target
        self.user=user
        self.password=password
        self.telnet=telnetlib.Telnet()

    def open(self):
        """This method will open a telnet session with authentication."""
        self.telnet.open(self.host)
        self.telnet.read_until('Username: ')
        self.telnet.write(self.user+'\n')
        self.telnet.read_until('Password: ')
        self.telnet.write(self.password+'\n')

    def execute(self, cmd):
        """This method will excute a telnet command."""
        self.telnet.write(cmd+'\r\n')
        self.telnet.read_until(' --More-- ')
        self.telnet.write('\r\n')
        print self.telnet.read_all().decode('ascii')

        return None

    def close(self):
        """This method will close the telnet session."""
        self.telnet.write('exit\n')
        self.telnet.close()


if __name__=='__main__':
    myTel=telnetHandler('172.16.3.2', 'cisco', 'cisco')
    myTel.open()
    data=myTel.execute('show process')
    print data
    myTel.close()
    print 'Done'

