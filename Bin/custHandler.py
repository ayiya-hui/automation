import XMLHelper
from appHandler import appHandler
from IPy import IP
import custDataClass
import collectorDataClass
import timeUtility
import xml.dom.minidom as dom

OPTIONS=['Customer', 'CustomerCollector']
DOMAIN_QUERY='config/Domain'
DOMAIN='domains'
COLLECTOR_QUERY='config/eventCollector'
EVENT_COLLECTOR='eventCollectors'
LIST='list'
DEFAULT_ADMIN='admin'
DEFAULT_ADMIN_PASSWORD='admin*1'
DEFAULT_EMAIL='admin@accelops.net'
DEFAULT_EPS=100
ADD_CUST='customer/add'
AUTO_CUST='AutoCust'
AUTO_COLLECTOR='AutoCollector'
MAX_DEV=500
DEFAULT_DAY=100

class custHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.appHandler=appHandler(appServer)

    def getNextCustomerAndCollectorId(self):
        if not hasattr(self, 'customers'):
            self.getCustomer()
        custIds=[]
        collectorIds=[]
        for customer in self.customers:
           custIds.append(int(customer.domainId))
        collectors=self.getCollector()
        if len(collectors):
            for collector in collectors:
                if hasattr(collector, 'collectorId') and collector.collectorId:
                    collectorIds.append(int(collector.collectorId))
        custIds.sort()
        self.nextCustId=custIds[-1]+1
        if len(collectorIds):
            collectorIds.sort()
            self.nextCollectorId=collectorIds[-1]+1
        else:
            self.nextCollectorId=10000

    def isCustomerExist(self, customerName):
        exist=False
        customers=self.getCustomer()
        for customer in customers:
            if customerName==customer.name:
                exist=True

        return exist

    def createCustomers(self, custName, include=[], exclude=[], collector=False, ip=False, maxDev=MAX_DEV, eps=DEFAULT_EPS, day=DEFAULT_DAY, number=1):
        myCustList=[]
        if not hasattr(self, 'nextCustId') and not hasattr(self, 'nextCollectorId'):
            self.getNextCustomerAndCollectorId()

        if collector:
            myCollector=collector
        else:
            myCollector=False
        baseIp=False
        if ip:
            baseIp=ip
        else:
            myIp=False
        for i in range(number):
            if number==1 or i==0:
                myName=custName
            else:
                myName=custName+str(i)
            if myCollector:
                if myCollector==AUTO_COLLECTOR:
                    myCollector=myName+'-'+myCollector

            custId=self.nextCustId+i
            myCollectorId=self.nextCollectorId+i
            if baseIp:
                myIp=IP(IP(baseIp).int()+i).strNormal()
            if len(include) and (len(include)-1)<i:
                myInc=include[i]
            else:
                myInc=False
            if len(exclude) and (len(exclude)-1)<i:
                myExc=exclude[i]
            else:
                myExc=False
            if not self.isCustomerExist(myName):
                myCust=self._createCustomerObj(myName, custId, include=myInc, exclude=myExc, collector=myCollector, collectorId=myCollectorId, ip=myIp, maxDev=maxDev, eps=eps, day=day)
                myCustList.append(myCust)

        self.uploadCustomer(myCustList)

        return [customer.name for customer in myCustList]

    def _createCustomerObj(self, custName, custId, include=False, exclude=False, collector=False, collectorId=False, ip=False, maxDev=MAX_DEV, eps=DEFAULT_EPS, day=DEFAULT_DAY):
        myCust=custDataClass.customer()
        myCust.name=custName
        myCust.custId=custId
        myCust.adminUser=DEFAULT_ADMIN
        myCust.adminPwd=DEFAULT_ADMIN_PASSWORD
        myCust.adminEmail=DEFAULT_EMAIL
        if include:
            myCust.includeRange=include
        if exclude:
            myCust.excludeRange=exclude
        myCust.custResource=custDataClass.custResource()
        myCust.custResource.configItem=maxDev
        myCust.custResource.custId=myCust.custId
        if collector:
            myCollector=collectorDataClass.eventCollector()
            delattr(myCollector, 'attribute')
            myCollector.name=collector
            myCollector.collectorId=collectorId
            myCollector.eps=eps
            myCollector.startTime, uTime=timeUtility.getTimeNow()
            myCollector.endTime=timeUtility.getFutureTime(day)
            if ip:
                myCollector.ipAddr=ip
            myCust.collectors.append(myCollector)
            myCust.svcUser=myCollector.collectorId
            myCust.svcPwd='admin*1'
            myCust.custResource.collectorId=myCollector.collectorId
            myCust.custResource.creationTime=myCollector.startTime
            myCust.custResource.diskQuote=0
            myCust.custResource.duration=0
            myCust.custResource.endTime=0
            myCust.custResource.eps=0
            myCust.custResource.id=0
            myCust.custResource.lastModified=0
            myCust.custResource.ownerId=0
            myCust.custResource.registered='true'
            myCust.custResource.startTime=0
            myCust.custResource.targetCustId=0

        return myCust

    def uploadCustomer(self, objList):
        if len(objList):
            inXml=self.createXml(objList)
            print inXml
            self.appHandler.putData(ADD_CUST, inXml)

    def createXml(self, objList):
        node=XMLHelper.pickle(root=objList, fabric=dom.Document(), elementName='customers')

        return node.toxml()

    def getCustomer(self):
        self.appHandler.getData(DOMAIN_QUERY)
        domains=XMLHelper.unpickleXml(self.appHandler.xml, DOMAIN, objType=LIST)
        finalDomains=[]
        collectors=self.getCollector()
        if len(collectors):
            for domain in domains:
                if domain.initialized=='true':
                    if hasattr(domain, 'collectors'):
                        domain.collectors=[]
                        for collector in collectors:
                            if domain.domainId==collector.attribute['custId']:
                                 domain.collectors.append(collector)
                    finalDomains.append(domain)
        else:
            finalDomains=domains
        self.customers=finalDomains

        return finalDomains

    def getCollector(self):
        self.appHandler.getData(COLLECTOR_QUERY)
        collectors=XMLHelper.unpickleXml(self.appHandler.xml, EVENT_COLLECTOR, objType=LIST)

        return collectors

    def getCustIdbyName(self, custName):
        custId=''
        if not hasattr(self, 'customers'):
            self.customers=self.getCustomer()
        for domain in self.customers:
            if domain.name.title()==custName.title():
                custId=domain.domainId

        return custId

    def getCustNamebyId(self, custId):
        custName=''
        if not hasattr(self, 'customers'):
            self.customers=self.getCustomer()
        for domain in self.customers:
            if domain.domainId==custId:
                custName=domain.name

        return custName

    def getCustIdbyIp(self, ipAddr, dataCollector):
        #check for collectors
        noCollect=True
        custId=[]
        if not hasattr(self, 'customers'):
            self.customers=self.getCustomer()
        for domain in self.customers:
            if hasattr(domain, 'collectors'):
                collectorList=domain.collectors
                if len(collectorList):
                    for col in collectorList:
                        if col.ipAddr==dataCollector:
                            custId.append(col.name)
                            noCollect=False
        if noCollect:
            for domain in self.customers:
                #check exclude
                if domain.excludeRange=='':
                    #check include
                    if domain.includeRange!='':
                        result=self.check(ipAddr, domain.includeRange)
                        if result:
                            custId.append(domain.domainId)
                else:
                    result=self.check(ipAddr, domain.excludeRange)
                    if not result:
                        if domain.includeRange!='':
                            result=self.check(ipAddr, domain.includeRange)
                            if result:
                                custId.append(domain.domainId)
                    else:
                        break

        if len(custId)==1:
            value=custId[0]
        else:
            value="1"

        return value

    def check(self, ipAddr, data):
        result=False
        exStack=data.split(",")
        for single in exStack:
            if '-' not in single:
                if ipAddr==single:
                    result=True
                    break
            else:
                rangeLow, rangeHigh=single.split('-')
                myIp=IP(ipAddr).int()
                if myIp >= IP(rangeLow).int() and myIp <= IP(rangeHigh).int():
                    result=True
                    break
        return result

if __name__=='__main__':
    usage="""
        usage: %prog args [options]
        -o, --option=OPTION                          :   Customer, CustomerCollector
        -n, --name=CUSTOMER_NAME                     :   name of customer, default AutoCust
        -i, --include=INCLUDE_RANGE                  :   IP ranges included
        -e, --exclude=EXCLUDE_RANGE                  :   IP ranges excluded
        -m, --max=MAX_DEVICES                        :   maximum devices in customer
        -c, --collectorName=COLLECTOR_NAME           :   collector name, default AutoCollector
        -d, --day=COLLECTOR_LIFE                     :   collector will last from now in days, default 100 days
        -s, --eps=EPS                                :   collector maximum EPS number, default 100
        -a, --address=IP_ADDRESS                     :   collector IP address
        -r, --randomNumber=NUMBERS_CUSTOMERS         :   numbers of random customers created
        -f, --file=INCLUDE_EXCLUDE_RANGE             :   IP ranges for included and excluded from file source"""
    import optionHandler, sys

    opts, args = optionHandler.parse(usage)

    if not opts and args:
        optionHandler.exit()
    try:
        myHandler=custHandler(args[0])
        if opts.option:
            if opts.option in OPTIONS:
                option=opts.option
            else:
                print 'Option is not supported, change to default Customer.'
                option='Customer'
        else:
            print 'No option specified, change to default Customer'
            option='Customer'
        if opts.name:
            name=opts.name
        else:
            name=AUTO_CUST
        if opts.collectorName:
            myCollector=opts.collectorName
        else:
            myCollector=AUTO_COLLECTOR
        if opts.eps:
            myEPS=opts.eps
        else:
            myEPS=DEFAULT_EPS
        if opts.include:
            myInclude=opts.include
        else:
            myInclude=False
        if opts.exclude:
            myExclude=opts.exclude
        else:
            myExclude=False
        if opts.max:
            myDev=opts.max
        else:
            myDev=MAX_DEV
        if opts.day:
            myDay=int(opts.day)
        else:
            myDay=DEFAULT_DAY
        if opts.address:
            myIp=opts.address
        else:
            myIp=False
        if opts.randomNumber:
            random=int(opts.randomNumber)
        else:
            random=1
        if opts.file:
            rangeFile=opts.file
        else:
            rangeFile=False
    except Exception, e:
        print 'Invalid Argument'
        sys.exit(1)

    includeList=[]
    excludeList=[]
    if rangeFile:
        myFile=open(rangeFile, 'r')
        myLines=myFile.readlines()
        myFile.close()
        for line in myLines:
            myInc, myExc=myLines[i].split(',')
            includeList.append(myInc)
            excludeList.append(myExc)
    elif myInclude and myExclude:
        includeList.append(myInclude)
        excludeList.append(myExclude)

    if option=='Customer':
        names=myHandler.createCustomers(name, include=includeList, exclude=excludeList, collector=False, maxDev=myDev, number=random)
    elif option=='CustomerCollector':
        names=myHandler.createCustomers(name, include=includeList, exclude=excludeList, collector=myCollector, ip=myIp, maxDev=myDev, eps=myEPS, day=myDay, number=random)

    print 'Task finished.'




