import dbUpgradeHandler
import configDataHandler
import XMLHelper
import classUtility

FILE_NAME='../TestData/DbUpgrade/preData/notification.xml'
LIST_KEY={'actions':'type', 'conditions':'name'}


def testNotification(server, option):
    if option.lower()=='pre':
        myDb=dbUpgradeHandler.dbUpgradeHandler(server)
        data=myDb.getNotification()
        myDb.saveXML(data, 'notificationPolicies', FILE_NAME)
    elif option.lower()=='post':
        myConfig=configDataHandler.configDataHandler(server)
        retData=myConfig.getData('notificationPolicies')
        oriData=XMLHelper.unpickleFile(FILE_NAME, 'notificationPolicies', objType='list')
        indexData={}
        for ori in oriData:
            indexData[ori.attribute['naturalId']]=ori
        for key in indexData.keys():
            classUtility.compare(indexData[key], retData[key], LIST_KEY, skip=['displayOrder', 'id', 'policy'])
    else:
        print 'option %s is not supported. Exit.' % option

if __name__=='__main__':
    import sys
    server=sys.argv[1]
    option=sys.argv[2]
    testNotification(server, option)

    print 'task done.'
