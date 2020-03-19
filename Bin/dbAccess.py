import pgdb

DEFAULT_PORT=5432
DEFAULT_USER='phoenix'
DEFAULT_PASSWORD='J23lMBSo5DQ!'
#DEFAULT_PASSWORD='kd8@paL5Dcy'
DEFAULT_DATABASE='phoenixdb'

class dbUtility:
    def __init__(self, host, port=False, user=False, password=False, database=False):
        if port:
            self.host=host+':'+port
        else:
            self.host=host+':'+str(DEFAULT_PORT)
        if user:
            self.user=user
        else:
            self.user='phoenix'
        if password:
            self.password=password
        else:
            self.password='J23lMBSo5DQ!'
        if database:
            self.database=database
        else:
            self.database='phoenixdb'



    def connect(self):
        try:
            self.conn=pgdb.connect(dsn=None, user=self.user, password=self.password, host=self.host, database=self.database)
        except:
            print "Exception encountered connecting database."

    def close(self):
        self.conn.close()

    def execute(self, cmd):
        myCur=self.conn.cursor()
        myVal=myCur.execute(cmd)
        print 'myVal %s' % myVal
        row=''
        if myVal!=None:
            row=myCur.fetchall()
        myCur.close()

        return row

if __name__=='__main__':
    dbServer='192.168.20.116'
    myDb=dbUtility(dbServer)
    myDb.connect()
    cmd='Select * from ph_sys_conf'
    val=myDb.execute(cmd)
    print 'my data %s' % val
    myDb.close()
