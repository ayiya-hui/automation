import psqlHandler
import dbUpgradeDataClass
import re
import classUtility
import notificationDataClass
import XMLHelper

CREATE_KEY='CREATE TABLE'
ALTER_KEY='ALTER TABLE'
REFERENCE_KEY='REFERENCE'
PATTERN_ADD_COLUMN='alter table\s+(?P<tableName>\S+)\s+add column\s+(?P<columnName>\S+)\s+(?P<dataType>[\s\S\(\)]+);'
PATTERN_CONSTR_OWEER='ALTER TABLE\s+(?P<tableName>\S+)\s+OWNER TO\s+(?P<tableOwner>\S+)'
PATTERN_CONSTR_PRIMARY='CONSTRAINT\s+(?P<constrName>\S+)\s+PRIMARY\s+KEY\s+\((?P<constrValue>\S+)\)'
PATTERN_CONSTR_FOREIGN='ALTER TABLE\s+(?P<tableName>\S+)\s+ADD CONSTRAINT\s+(?P<keyName>[\S\d]+)\s+FOREIGN KEY\s+\((?P<columnName>\S+)\)'
PATTERN_REFERENCE='REFERENCES\s+(?P<refTableName>\S+)\s+(?P<refColumnName>[\(\)\S]+)\s+MATCH SIMPLE'
PATH='../TestData/DbUpgrade/Schema/upgrade/'
VERSIONS={'3.5.1':'phoenix_db_up_3.1.2_to_3.5.1.sql', '3.1.2':'phoenix_db_up_3.1.0_to_3.1.2.sql'}
TABLES="Select table_name from information_schema.TABLES where table_name like 'ph_%'"
TABLE_ATTR="Select column_name, is_nullable, data_type, character_maximum_length, column_default from information_schema.COLUMNS where table_name = '%s'"
NOTIFICATION="Select id, cust_org_id, event_source_id, name from ph_notification where event_source_type = 'Rule'"
DELIVER="Select receipt, receipt_type, type from ph_delivery where notification_id = %s"
RULE_NATURAL_ID="Select natural_id from ph_drq_rule where id = %s"
DB_VERSION="Select value from ph_sys_conf where property = 'DB_Schema_Version'"

class dbUpgradeHandler:
    def __init__(self, dbServer):
        self.dbServer=dbServer
        self.dbHandler=psqlHandler.psqlHandler(self.dbServer)

    def getDbVersion(self):
        data=self.dbHandler.execute(DB_VERSION)

        return data[0][0]

    def getDbTableList(self):
        data=self.dbHandler.execute(TABLES)
        self.dbTables=[]
        for item in data:
            if item[0]!='ph_ec_auth_view':
                self.dbTables.append(item[0])

    def isTableExist(self, tableName):
        exist=False
        if not hasattr(self, 'dbTables'):
            self.getDbTableList()
        if tableName in self.dbTables:
            exist=True

        return exist

    def getTableAttr(self, tableName):
        data=self.dbHandler.execute(TABLE_ATTR % tableName)

        return data

    def compareAttr(self, tableName, data):
        indexData={}
        for item in data:
            map={}
            map['Name']=item[0]
            if item[1]=='YES':
                map['NotNull']=False
            elif item[1]=='NO':
                map['NoNull']=True
            if item[3]:
                map['DataType']=item[2].strip()+'('+item[3].strip()+')'
            else:
                map['DataType']=item[2].strip()
            if item[4]:
                map['Default']=item[4].strip()
            indexData[map['Name']]=map
        if tableName in self.newTableIndex:
            if len(data)!=len(self.newTables[tableName].Columns):
                print 'new table %s' % tableName
                print 'columns number not match. Expect %s Actual %s' % (len(self.newTables[tableName].Columns), len(data))
                print 'expect columns:'
                for col in self.newTables[tableName].Columns:
                    print col.Name
                print 'actual columns:'
                for key in indexData.keys():
                    print key

            expTable=self.newTables[tableName]
        else:
            expTable=self.alterTables[tableName]

        for column in expTable.Columns:
            actualColumn=indexData[column.Name]
            for attr in classUtility.getAttrList(column):
                if attr in actualColumn.keys():
                    value=getattr(column, attr)
                    if str(value).strip()!=str(actualColumn[attr]).strip():
                        print 'attr %s in column %s has value mismatch: expect %s actual %s' % (attr, column.Name, value, actualColumn[attr])

    def getUpgradeDatafromSQL(self, version):
        sqlFile=PATH+VERSIONS[version]
        self.newTableIndex=[]
        self.alterTableIndex=[]
        self.newTables={}
        self.alterTables={}
        myFile=open(sqlFile)
        datas=myFile.readlines()
        myFile.close()
        blockMode=False
        alterMode=False
        foreignKey=''
        tableName=''
        for line in datas:
            if CREATE_KEY in line:
                myTable=dbUpgradeDataClass.table()
                myTable.attribute['Name']=line.split(CREATE_KEY)[-1].strip()
                self.newTableIndex.append(myTable.attribute['Name'])
                self.newTables[myTable.attribute['Name']]=myTable
                tableName=myTable.attribute['Name']
                blockMode=True
            elif blockMode:
                if line.strip()=='(':
                   pass
                elif line.strip()==')':
                    blockMode=False
                    tableName=''
                elif 'CONSTRAINT' in line and 'PRIMARY KEY' in line:
                        primaryKey=dbUpgradeDataClass.primaryConstraint()
                        ret=self.__getRegExp(PATTERN_CONSTR_PRIMARY, line)
                        primaryKey.Name=ret.group('constrName')
                        primaryKey.Columns=ret.group('constrValue')
                        self.newTables[tableName].Constraints.append(primaryKey)
                        self.newTables[tableName].attribute['Primary key']=primaryKey.Columns
                        for column in self.newTables[tableName].Columns:
                            if column.Name==primaryKey.Columns:
                                column.primaryKey=True
                else:
                    column=dbUpgradeDataClass.Column()
                    if 'NOT NULL' in line:
                        column.NotNull=True
                        line=line.replace('NOT NULL', '')
                    if 'DEFAULT' in line:
                        myStack=line.split('DEFAULT')
                        line=myStack[0].strip()
                        column.Default=myStack[-1].replace(',', '').strip()
                    values=line.strip().split(' ')
                    column.Name=values[0].replace('"','').strip()
                    if len(values)==2:
                        column.DataType=values[1].replace(',', '')
                    elif len(values)==3:
                        column.DataType=values[1]+' '+values[2].replace(',', '')
                    self.newTables[tableName].Columns.append(column)
            elif ALTER_KEY in line and 'OWNER TO' in line:
                ret=self.__getRegExp(PATTERN_CONSTR_OWEER, line)
                myTable=ret.group('tableName')
                if myTable in self.newTableIndex:
                    self.newTables[myTable].attribute['Owner']=ret.group('tableOwner')
            elif ALTER_KEY in line and 'ADD CONSTRAINT' in line and 'FOREIGN KEY' in line:
                alterMode=True
                ret=self.__getRegExp(PATTERN_CONSTR_FOREIGN, line)
                tableName=ret.group('tableName')
                foreignKey=dbUpgradeDataClass.foreignConstraint()
                foreignKey.Name=ret.group('keyName')
                foreignKey.ChildColumns=ret.group('columnName')
            elif REFERENCE_KEY in line:
                if alterMode and foreignKey:
                    ret=self.__getRegExp(PATTERN_REFERENCE, line)
                    foreignKey.References=ret.group('refTableName')+ret.group('refColumnName')
                    if tableName in self.newTableIndex:
                        self.newTables[tableName].Constraints.append(foreignKey)
                alterMode=False
                foreignKey=''
            elif ALTER_KEY.lower() in line:
                myAlt=dbUpgradeDataClass.table()
                ret=self.__getRegExp(PATTERN_ADD_COLUMN, line)
                myAltName=ret.group('tableName')
                myAlt.attribute['Name']=myAltName
                column=dbUpgradeDataClass.Column()
                column.Name=ret.group('columnName').replace('"','')
                column.DataType=ret.group('dataType')
                myAlt.Columns.append(column)
                if myAltName not in self.alterTableIndex:
                    self.alterTableIndex.append(myAlt.attribute['Name'])
                    self.alterTables[myAlt.attribute['Name']]=myAlt
                else:
                    self.alterTables[myAltName].Columns.append(column)

    def __getRegExp(self, reg, value):
        pattern=re.compile(reg)
        ret=pattern.search(value)

        return ret

    def getNotification(self):
        data=self.dbHandler.execute(NOTIFICATION)
        finalList=[]
        for item in data:
            myNotiPolicy=notificationDataClass.notificationPolicy()
            deliver=self.dbHandler.execute(DELIVER % item[0])
            naturalId=self.dbHandler.execute(RULE_NATURAL_ID % item[2])[0][0]
            myNotiPolicy.attribute['naturalId']=naturalId
            myNotiPolicy.name=item[3]
            myCond=notificationDataClass.notificationCondition()
            myCond.name=naturalId
            myCond.type='RULE'
            myNotiPolicy.conditions.append(myCond)
            for de in deliver:
                myAct=notificationDataClass.notificationAction()
                if de[1]=='VALUE':
                    if de[2]=='EMAIL':
                        myAct.type=de[2].title()
                        myAct.definition=de[0]
                    elif de[2]=='SMS':
                        myAct.type=de[2]
                        myAct.definition=de[0]
                    elif de[2]=='ALERT':
                        myAct.type=de[2].title()
                elif de[1]=='SNMP':
                    myAct.type=de[1]+'Trap'
                else:
                    myAct.type=de[1]
                myNotiPolicy.actions.append(myAct)
            finalList.append(myNotiPolicy)

        return finalList

    def saveXML(self, finalData, type, fileName):
        myNode=XMLHelper.classListToXml(finalData, type)
        if not '.xml' in fileName:
            fileName+='.xml'
        myFile=open(fileName, 'w')
        myNode.writexml(myFile)
        myFile.close()







if __name__=='__main__':
    import sys
    dbServer=sys.argv[1]
    path=VERSIONS[sys.argv[2]]
    myDb=dbUpgradeHandler(dbServer)
    #myDb.getUpgradeDatafromSQL(path)
    #print 'verify new tables:'
    #for table in myDb.newTables.keys():
     #   print 'new table: %s' % table
      #  if myDb.isTableExist(table):
       #     myData=myDb.getTableAttr(table)
        #    myDb.compareAttr(table, myData)
    #print 'verify new columns in existing tables:'
    #for table in myDb.alterTables.keys():
      #  print 'existing table: %s' % table
      #  myData=myDb.getTableAttr(table)
     #   myDb.compareAttr(table, myData)

    data=myDb.getNotification()
    myDb.saveXML(data, 'notificationPolicies', 'noti')




    print 'Task Finished.'





