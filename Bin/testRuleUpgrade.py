import configDataHandler
import XMLHelper
import classUtility
import hashUtility

FILE_NAME='../TestData/DbUpgrade/preData/rule.xml'

def testRuleUpgrade(server, option):
    myHandler=configDataHandler.configDataHandler(server)
    if option.lower()=='pre':
        data=myHandler.getData('rule', pickle=False)
        myFile=open(FILE_NAME, 'w')
        myFile.write(data)
        myFile.close()
    elif option.lower()=='post':
        retData=myHandler.getData('rule')
        oriData=XMLHelper.unpickleFile(FILE_NAME, 'rules', objType='list')
        indexData={}
        for ori in oriData:
            indexData[ori.attribute['naturalId']]=ori
        missKey, extraKey, commonKey=hashUtility.getHashKeys(indexData, retData)
        if len(missKey):
            print 'Missing rules: %s' % len(missKey)
            print '\nMissing rules detail:'
            for key in missKey:
                print '%s: %s' % (key, indexData[key].name)
        if len(extraKey):
            print 'Extra rules: %s' % len(extraKey)
            print '\nExtra rules detail:'
            for key in extraKey:
                print '%s: %s' % (key, retData[key].name)
        for key in commonKey:
            classUtility.compare(indexData[key], retData[key], None)
    else:
        print 'option %s is not supported. Exit.' % option

if __name__=='__main__':
    import sys
    server=sys.argv[1]
    option=sys.argv[2]
    testRuleUpgrade(server, option)

    print 'task done.'
