import appHandler
import XMLHelper
import orgDataClass
from xml.dom.minidom import parseString

QUERY_STRING='config/Domain'

class orgHandler:
    def __init__(self, appServer, user=False, password=False):
        self.appHandler=appHandler.appHandler(appServer, user, password)

    def getOrgs(self):
        self.appHandler.getEvent("GET", urlString=QUERY_STRING)
        root=parseString(self.appHandler.xml[0].encode('ascii','xmlcharrefreplace'))
        myNode=root.getElementsByTagName("domains")[0]
        orgs=XMLHelper.unpickle(XMLHelper._getElementChilds(myNode), 'org', type='list')
        self.orgs=[]
        for org in orgs:
            if org.initialized=='true':
                self.orgs.append(org)

    def getOrgIDfromName(self, orgName):
        orgId=''
        for org in self.orgs:
            if org.name.title()==orgName.title():
                orgId=org.domainId

        return orgId

    def getOrgIDfromIP(self, ip):
        custId=[]
        for org in self.orgs:
            #check exclude
            if org.excludeRange=='':
                #check include
                result=self.check(ipAddr, org.includeRange)
                if result=="true":
                    custId.append(org.domainId)
            else:
                result=self.check(ipAddr, org.excludeRange)
                if result=="false":
                    result=self.check(ipAddr, org.includeRange)
                    if result=="true":
                        custId.append(org.domainId)
                else:
                    break

        if len(custId)==1:
            value=custId[0]
        else:
            value="1"

        return value

    def check(self, ipAddr, data):
        exStack=data.split(",")
        for single in exStack:
            if '-' in single:
                result=self.checkRange(ipAddr, single)
                if result=="true":
                    return result
            else:
                if single==ipAddr:
                    result="true"
                    return result
                else:
                    result="false"
        return result

    def checkRange(self, ipAddr, range):
        result="false"
        test1="false"
        test2="false"
        test3="false"

        myStack=ipAddr.split(".")
        rangeStack=range.split("-")
        rangeStart=rangeStack[0].split(".")
        rangeEnd=rangeStack[1].split(".")

        #check what kind of network
        network=""
        if rangeStart[0]==rangeEnd[0]:
            network="A"
            if rangeStart[1]==rangeEnd[1]:
                network="B"
                if rangeStart[2]==rangeEnd[2]:
                    network="C"

        if int(myStack[1]) >= int(rangeStart[1]) and int(myStack[1])<=int(rangeEnd[1]):
            test1="true"

        if int(myStack[2]) >=int(rangeStart[2]) and int(myStack[2])<=int(rangeEnd[2]):
            test2="true"

        if int(myStack[3]) >=int(rangeStart[3]) and int(myStack[3])<=int(rangeEnd[3]):
            test3="true"

        if network=="A":
            if test1=="true":
                return "true"
        elif network=="B":
            if test1=="true" and test2=="true":
                return "true"
        else:
            if test1=="true" and test2=="true" and test3=="true":
                return "true"

        return result

    def findCustName(self, custId):
        custName=''
        for org in self.orgs:
            if custId==org.domainId:
                custName=org.name

        return custName

if __name__=='__main__':
    server='192.168.20.116'
    myHandler=orgHandler(server)
    myHandler.getOrgs()
    id=myHandler.getOrgIDfromName('MSFT')
    print id
    print 'Done'
