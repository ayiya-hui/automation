import dbAccess
from xml.dom.minidom import Node, Document, parse
import time

def dbIntegrityCheck(dbServer, schemaVersion, newTable):
    myDb=dbAccess.dbUtility(dbServer)
    myDb.connect()

    #check db version
    print 'Check 1: DB Schema Version'
    cmd="Select value from ph_sys_conf where property = 'DB_Schema_Version'"
    data=myDb.execute(cmd)
    while not data:
        data=myDb.execute(cmd)
        print 'data is %s' % data
        time.sleep(3)
    print 'data is %s' % data
    if data[0][0]==schemaVersion:
        print 'DB has correct schema version %s' % data[0][0]
    else:
        print 'DB has wrong schema version %s, expect %s' % (data[0][0], schemaVersion)

    #check total numbers of tables
    print 'Check 2: total numbers of tables'
    cmd="Select * from information_schema.TABLES where table_name like 'ph_%'"
    data=myDb.execute(cmd)
    count=0
    mytable=[]
    for item in data:
        if item[2]!='ph_ec_auth_view':
            count+=1
            mytable.append(item[2])

    print 'Total table is %s' % count

    #check if new tables are there
    for new in newTable:
        if new['name'] in mytable:
            myData=[]
            if new['isNew']=='Yes':
                print '\nNew table %s is created.' % new['name']
            else:
                print '\nOld table %s is altered.' % new['name']

            cmd="Select * from information_schema.COLUMNS where table_name = '"+new['name']+"'"
            data=myDb.execute(cmd)
            for item in data:
                mapping={}
                mapping['name']=item[3]
                mapping['default']=item[5]
                mapping['isNull']=item[6]
                mapping['type']=item[7]
                mapping['length']=str(item[8])
                myData.append(mapping)
            myParams=new['params']
            for param in myParams:
                for key in param.keys():
                    for map in myData:
                        if param['name']==map['name']:
                            if param[key]==map[key]:
                                if key!='name':
                                    print 'column name %s param %s correct value %s' % (param['name'], key, param[key])
                            else:
                                print 'BIG ERROR!!! column name %s incorrect value %s' % (key, param[key])

    #check ph_user with three default values
    print 'Check 2: ph_user have default users: 500150, 500151, 500152 are present.'
    cmd='Select * from ph_user where id = 500150 or id=500151 or id=500152'
    data=myDb.execute(cmd)
    check1=[500150, 500151, 500152]
    for item in data:
        if item[0] in check1:
            print 'User %s is exist: %s' % (item[0], item)
            check1.remove(item[0])
        else:
            print 'Sanity check fail. Default user is not present.'

    if len(check1)>0:
        for i in range(len(check1)):
            print 'User %s is not present in ph_user table.' % (check1[i])

    #check ph_sys_conf for scheme version, etc.
    print 'Check 3: ph_sys_config for scheme version, system key, system name, svn rul, svn user name and svn password.'
    cmd="Select * from ph_sys_conf where property='DB_Schema_Version' or property='System_Key' or property='System_Name' or property='svn_url' or property='svn_username' or property='svn_password'"
    data=myDb.execute(cmd)
    check2=['DB_Schema_Version', 'System_Key', 'System_Name', 'svn_url', 'svn_username', 'svn_password']
    for item in data:
        if item[6]=='DB_Schema_Version':
            if item[8]==schemaVersion:
                print 'Schema version is %s: %s' % (schemaVersion, item)
            else:
                print 'Sanity check fail. Schema version is not correct.'
            check2.remove(item[6])
        elif item[6]=='System_Key':
            print 'System Key is unique: %s' % item[8]
            check2.remove(item[6])
        elif item[6]=='System_Name':
            print 'System Name %s is matching with your install system: %s' % (item[8], item)
            check2.remove(item[6])
        elif item[6]=='svn_url':
            if '127.0.0.1' in item[8]:
                print 'VN URL is loopback with single VA: %s' % item[8]
            else:
                print 'VN URL is Super IP Address: %s' % item[8]
            check2.remove(item[6])
        elif item[6]=='svn_username':
            print 'SVN User Name is present: %s' % item[8]
            check2.remove(item[6])
        elif item[6]=='svn_password':
            print 'SVN User Password is present: %s' % item[8]
            check2.remove(item[6])
        else:
            print "This value is not correct."

    if len(check2)>0:
        for i in range(len(check2)):
            print '%s is not present in ph_user table' % check2[i]

    #check ph_sys_domain for 3 admins
    print 'Check 4: ph_sys_domain for System, Service and Super Customer values'
    cmd="Select * from ph_sys_domain where id=500050 or id=500051 or id=500052"
    data=myDb.execute(cmd)
    check3=[500050, 500051, 500052]
    for item in data:
        if item[0] in check3:
            print '%s with name %s is exist: %s' % (item[0], item[9], item)
            check3.remove(item[0])
        else:
            print 'Sanity check fail. Default user is not present.'

    if len(check3)>0:
        for i in range(len(check3)):
            print '%s is not present in ph_sys_domain table' % check3[i]



    #print data

    myDb.close()

def parsingUpgrade(fileName):
    newParam=[]
    doc=parse(fileName)
    for node in doc.getElementsByTagName("tables"):
        for node1 in node.getElementsByTagName("table"):
            tableParam={}
            tableParam['name']=node1.getAttribute("name")
            tableParam['isNew']=node1.getAttribute("isNew")
            params=[]
            for node2 in node1.getElementsByTagName("column"):
                mapping={}
                myKeys=node2.attributes.keys()
                for key in myKeys:
                    value=node2.getAttribute(key)
                    mapping[key]=value
                params.append(mapping)
            tableParam['params']=params
            newParam.append(tableParam)

    return newParam

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print "Usage: dbIntegrityCheck.py dbServerIP dbSchemaVersion"
        exit()
    #fileName='C:\eclipse-galileo-pydev\workspace\AutoAccelops\Bin\dbSchema.xml'
    #newTable=parsingUpgrade(fileName)
    newTable=''
    dbIntegrityCheck(sys.argv[1], sys.argv[2], newTable)

