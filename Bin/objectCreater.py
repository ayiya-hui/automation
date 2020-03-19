"""
    usage: %prog args [options]
    -o, --object=OBJECT                          :   name of Objects (CustomerOnly, UserOnly, CustomerUser, CustomerCollector, CustomerCollectorUser)
    -n, --number=NUMBER_CUSTOMER, NUMBER_USER    :   numbers of cutomers and numbers of user in a customer, default as 1 (only 1 collector in a customer as default)
    -c, --customerName=CUSTOMER_NAME             :   name of customer, default as AutoCust, if more than one customer, then all others will have name+number format
    -u, --userName=USER_NAME                     :   name of user, default as AutoUser, if more than one user, then all others will have user_name+number format
    -t, --userType=USRE_TYPE                     :   type of user, default as Full Admin
    -l, --collectorName=COLLECTOR_NAME           :   name of collector, default as AutoCollector
    -a, --collectorIp=COLLECTOR_IPADDR           :   IP address of collector
"""

import optionHandler, sys, time
import userHandler, custHandler

OBJECTS=['CustomerOnly', 'UserOnly', 'CustomerUser', 'CustomerCollector', 'CustomerCollectorUser']
USER_TYPE=['DB Admin', 'Executive', 'Full Admin', 'Help Desk', 'Network Admin', 'Read-Only Admin', 'Security Admin', 'Server Admin', 'Storage Admin', 'System Admin', 'Unix Server Admin', 'Windows Server Admin']

opt, args = optionHandler.parse(__doc__)

if not opt and args:
    optionHandler.exit()
try:
    appServer=args[0]
    if opt.object:
        if opt.object in OBJECTS:
            myObj=opt.object
        else:
            print 'Object is not support. Supported Objects are %s' % ','.join(OBJECTS)
            optionHandler.exit()
    else:
        print 'No Object specified.'
        optionHandler.exit()
    if opt.number:
        if ',' in opt.number:
            n1, n2=opt.number.split(',')
            custNum=int(n1)
            userNum=int(n2)
        else:
            custNum=userNum=int(opt.number)
    else:
        custNum=userNum=1
    if opt.customerName:
        custName=opt.customerName
    else:
        custName='AutoCust'
    if opt.userName:
        myUserName=opt.userName
    else:
        myUserName='AutoUser'
    if opt.userType:
        if opt.userType in USER_TYPE:
            myUserType=opt.userType
        else:
            print 'User type is not supported. Change to default Full Admin'
            myUserType='Full Admin'
    else:
        myUserType='Full Admin'
    if opt.collectorName:
        myCollectorName=opt.collectorName
    else:
        myCollectorName='AutoCollector'
    if opt.collectorIp:
        myIp=opt.collectorIp
    else:
        myIp=False
except Exception, e:
    print 'Invalid Argument'
    sys.exit(1)


if myObj=='UserOnly':
    myUser=userHandler.userHandler(appServer)
    myUser.createUsers(myUserName, custName, myUserType, number=userNum)
elif myObj=='CustomerOnly':
    myCust=custHandler.custHandler(appServer)
    names=myCust.createCustomers(custName, number=custNum)
elif myObj=='CustomerCollector':
    myCust=custHandler.custHandler(appServer)
    names=myCust.createCustomers(custName, collector=myCollectorName, ip=myIp, number=custNum)
elif myObj=='CustomerUser':
    myCust=custHandler.custHandler(appServer)
    names=myCust.createCustomers(custName, number=custNum)
    time.sleep(120)
    for name in names:
        myUser.createUsers(myUserName, name, myUserType, number=userNum)
elif myObj=='CustomerCollectorUser':
    myCust=custHandler.custHandler(appServer)
    names=myCust.createCustomers(custName, collector=myCollectorName, ip=myIp, number=custNum)
    myUser=userHandler.userHandler(appServer)
    time.sleep(120)
    for name in names:
        while not myCust.isCustomerExist(name):
            time.sleep(10)
        myUser.createUsers(myUserName, name, myUserType, number=userNum)

print 'Task finished.'

