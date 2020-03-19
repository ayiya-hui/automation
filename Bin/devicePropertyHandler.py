import appHandler
import XMLHelper
import devicePropertyDataClass

ENTITY_VALUE='device/properties'

class devicePropertyHandler:
    def __init__(self, appServer):
        self.appHandler=appHandler.appHandler(appServer)

    def getDeviceProperty(self):
        self.appHandler.getData(ENTITY_VALUE)
        values=XMLHelper.unpickleXml(self.appHandler.xml, 'devicePropertiesList', objType='list')
        self.data=values

    def getIpbyProperty(self, propertyName, propertyValue):
        ipList=[]
        if not hasattr(self, 'data'):
            self.getDeviceProperty()
        for data in self.data:
            if len(data.properties):
                for pro in data.properties:
                    if pro.propertyName==propertyName.strip() and pro.propertyValue==propertyValue.strip():
                        if data.ipAddr not in ipList:
                            ipList.append(data.ipAddr)

        return ipList

if __name__=='__main__':
    import sys
    myProperty=devicePropertyHandler(sys.argv[1])
    ips=myProperty.getIpbyProperty('city', 'San Jose')
    print ips

