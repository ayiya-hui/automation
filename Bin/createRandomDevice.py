import ComHandler
import createDevice
import time

DEFAULT_ADMIN="super/admin"
DEFAULT_PASSWORD="admin*1"

def createRandomDevice(appServer, deviceType, custId, number):
     myHandler=ComHandler.comHandler(appServer, appServer, DEFAULT_ADMIN, DEFAULT_PASSWORD)
     inXml=createDevice.createRandomDeviceList(deviceType, custId, number)
     queryString="discovered/discover?sync=true"
     myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
     print "Done"

if __name__=='__main__':
    import sys
    number=int(sys.argv[4])
    if number > 200:
        count=number/200
        for i in range(0, count):
            createRandomDevice(sys.argv[1],sys.argv[2], sys.argv[3],200)
            time.sleep(5)
    else:
        createRandomDevice(sys.argv[1],sys.argv[2], sys.argv[3],number)



