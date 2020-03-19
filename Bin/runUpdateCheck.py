import getUpdateInfo
import CSVHandler

def runUpdateCheck(option, server, type, scope=None, path=None):
    myPath=''
    if path:
        if option in ['csv2csv','xml2xml']:
            myPath=[]
            for item in path.split(','):
                myPath.append(item+'\\'+type)
        else:
            myPath=path+'\\'+type

    if type=='report':
        report=True
    else:
        report=False

    if option=='csv2csv':
        keyWord='upgrade'
        myData1=CSVHandler.getData(myPath[0])
        myData2=CSVHandler.getData(myPath[1])
    elif option=='csv2db':
        keyWord='install'
        db=server
        myData1=CSVHandler.getData(myPath)
        myrawData=getUpdateInfo.getData(db, type)
        myData2=myrawData[type]
    elif option=='xml2xml':
        keyWord='upgrade'
        myData1=getUpdateInfo.getXML(path=myPath[0], report=report)
        myData2=getUpdateInfo.getXML(path=myPath[1], report=report)
    elif option=='xml2db':
        keyWord='install'
        db=server
        myData1=getUpdateInfo.getXML(path=myPath, report=report)
        myrawData=getUpdateInfo.getData(db, type)
        myData2=myData[type]
    elif option=='db2db':
        keyWord='upgrade'
        db=server.split(',')
        myrawData1=getUpdateInfo.getData(db[0], type)
        myrawData2=getUpdateInfo.getData(db[1], type)
        myData1=myrawData1[type]
        myData2=myrawData2[type]

    getUpdateInfo.output(myData1, myData2, type, keyWord)
    print '\nDone'

if __name__=='__main__':
    import sys
    if not len(sys.argv)in [4,5,6] :
        usage='Usage: runUpdateCheck.py option server type scope [path=]\
                option -- xml2db, xml2xml, db2db \
                server -- xml2db one db server is required; xml2xml no db server is required; db2db two db servers are require with , separating \
                type -- eventType, rule, report, role and all \
                scope -- if not specified, check all. Using Natural_Id will check only specified \
                path -- where xml files located that as parent folders for folder rule/report/eventtype/role'

    option=sys.argv[1]
    servers=sys.argv[2]
    type=sys.argv[3]

    val4=None
    val5=None
    scope=None
    path=None

    if len(sys.argv)==5:
        val4=sys.argv[4]

    if len(sys.argv)==6:
        val5=sys.argv[5]

    if val4!=None:
        if 'scope=' in val4:
            scope=val4.split('=')[-1]
        elif 'path=' in val4:
            path=val4.split('=')[-1]

    if val5!=None:
        if 'scope=' in val5:
            scope=val5.split('=')[-1]
        elif 'path=' in val5:
            path=val5.split('=')[-1]

    runUpdateCheck(option, servers, type, scope=scope, path=path)





