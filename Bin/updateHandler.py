import getUpdateInfo

class updateHandler:
    def __init__(self):
        pass

    def getData(self, dbServer):
        self.dbServer=dbServer
        self.dbData={}
        self.dbData['eventtype']=self._getDataWithType('eventtype')
        self.dbData['rule']=self._getDataWithType('rule')
        self.dbData['report']=self._getDataWithType('report')

    def saveToFile(self, fileName):
        myFile=open('./'+fileName, 'w')

        myFile.write(str(self.dbData))
        myFile.close()

    def _getDataWithType(self, type):
        myrawData=getUpdateInfo.getData(self.dbServer, type)
        myData=myrawData[type]

        return myrawData

if __name__=='__main__':
    import sys
    myUpdate=updateHandler()
    myUpdate.getData(sys.argv[1])
    myUpdate.saveToFile(sys.argv[2])
    print 'Done'







