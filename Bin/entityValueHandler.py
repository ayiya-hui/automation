import appHandler
import XMLHelper
import entityValueDataClass

ENTITY_VALUE='namedValue/group?name=%s'

class entityValueHandler:
    def __init__(self, appServer):
        self.appHandler=appHandler.appHandler(appServer)

    def getEntityValue(self, value):
        param=ENTITY_VALUE % value
        param=param.replace('"', '')
        self.appHandler.getData(param)
        values=XMLHelper.unpickleXml(self.appHandler.xml, 'entityValues', objType='list')
        if len(values):
            self.data=values[0].values
        else:
            print 'no data return'



if __name__=='__main__':
    import sys
    myEntity=entityValueHandler(sys.argv[1])
    myEntity.getEntityValue(sys.argv[2])

