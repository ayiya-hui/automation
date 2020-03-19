import XMLHelper
import xml.dom.minidom as dom
import randomGen
from pickClass import pickleClass

class config(pickleClass):
    def __init__(self, customers=[]):
        self.customers=customers

class customer(pickleClass):
    def __init__(self,name,fullName,description,adminUser,adminPwd,adminEmail,includeRange,excludeRange=False):
        self.name=name
        self.fullName=fullName
        self.description=description
        self.adminUser=adminUser
        self.adminPwd=adminPwd
        self.adminEmail=adminEmail
        self.includeRange=includeRange

        if excludeRange:
            self.excludeRange=excludeRange


def createCustList(number, custName, adminUser, adminPass, include, exclude=False):
    myCustList=[]
    for i in range(number):
        if custName=="random":
            myCustName="autoCust"+str(i+1)
        else:
            myCustName=custName

        if include=="random":
            myInclude=randomGen.getRandomIPAddr()
        else:
            myInclude=include

        myCustFullName="Full name for "+myCustName
        myDesc="Autotest the customer "+myCustName
        adminEmail=adminUser+'@test.com'

        myCust=customer(myCustName, myCustFullName, myDesc, adminUser, adminPass, adminEmail, myInclude, excludeRange=exclude)
        myCustList.append(myCust)

    myObj=config(myCustList)
    node=XMLHelper.pickle(root=myObj, fabric=dom.Document(), elementName='config')
    print node.toxml()
    return node.toxml()

if __name__=='__main__':
    import sys
    #import ComHandler
    import appHandler

    DEFAULT_ADMIN="super/admin"
    DEFAULT_PASSWORD="admin*1"
    appServer=sys.argv[1]
    inXml=createCustList(int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    #myHandler=ComHandler.comHandler(appServer, appServer, DEFAULT_ADMIN, DEFAULT_PASSWORD)
    myHandler=appHandler.appHandler(appServer)
    queryString="custMgmt/add"
    #myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
    myHandler.putData(queryString, inXml)
    print "Done"


