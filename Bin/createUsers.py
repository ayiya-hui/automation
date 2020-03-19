import XMLHelper
import configModel
import xml.dom.minidom as dom
import randomGen

SYS='Group@PH_SYS_DEVICE_'
PRE='hostIpAddr IN(Group@PH_SYS_DEVICE_Network) OR reptDevIpAddr IN (Group@PH_SYS_DEVICE_Network) OR srcIpAddr IN
(Group@PH_SYS_DEVICE_Network) OR destIpAddr IN
(Group@PH_SYS_DEVICE_Network)'
DATA={'full':'','read-only':'','network':'hostIpAddr IN (Group@PH_SYS_DEVICE_Network) OR
reptDevIpAddr IN (Group@PH_SYS_DEVICE_Network) OR srcIpAddr IN
(Group@PH_SYS_DEVICE_Network) OR destIpAddr IN
(Group@PH_SYS_DEVICE_Network)'}

def createUsers(number, custName, adminUser, adminPass, include, exclude=False):
    myCustList=[]
    for i in range(number):
        if custName=="random":
            myCustName="autoCust"+str(i+1)
        else:
            myCustName=custName

        if include=="random":
            myInclude=randomGen.getRandomIPAddr()

        myCustFullName="Full name for "+myCustName
        myDesc="Autotest the customer "+myCustName
        adminEmail=adminUser.split("/")[1]+'@test.com'

        myCust=CustModel.customer(myCustName, myCustFullName, myDesc, adminUser, adminPass, adminEmail, myInclude, excludeRange=exclude)
        myCustList.append(myCust)

    myObj=CustModel.config(myCustList)
    node=XMLHelper.pickle(root=myObj, fabric=dom.Document(), elementName='config')

    return node.toxml()

def createRoleProfile(name):
    profile=configModel.RbacProfile()
    proName=None
    proDesc=None
    proConfig=None
    eventFilter=createEventFilter(name)

    if name=="full":
        proName="Full Admin"
        proDesc="A role for unrestricted administrators. Users having this role have full access to the AccelOps system without any restriction."
        proConfig='<?xml version="1.0" encoding="UTF-8"?><profile><groupNodes/><leafNodes/></profile>'

    elif name=="read-only":
    elif name=="network":
    elif name=="server":
    elif name=="storage":
    elif name=="windows":
    elif name=="linux":
    elif name=="help desk":
    elif name=="executive":
    elif name=="system":
    elif name=="security":
    elif name=="db":


def createEventFilter(name):
    eventFilter=configModel.eventFilter()
    constr=DATA[name]
    eventFilter.fillInfo(constr)

    return eventFilter



if __name__=='__main__':
    import sys
    import ComHandler

    DEFAULT_ADMIN="super/admin"
    DEFAULT_PASSWORD="admin*1"
    appServer=sys.argv[1]
    inXml=createCustList(int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    myHandler=ComHandler.comHandler(appServer, appServer, DEFAULT_ADMIN, DEFAULT_PASSWORD)
    queryString="custMgmt/add"
    myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
    print "Done"


