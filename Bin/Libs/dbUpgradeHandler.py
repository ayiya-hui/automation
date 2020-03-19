import psqlHandler
import dbUpgradeDataClass
import re
import classUtility
import notificationDataClass
import XMLHelper
from ConfigConstants.dbUpgradeConfig import *


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
            id=item[0]
            custId=item[1]
            event_src_id=item[2]
            name=item[3]
            if custId=='0':
                custId='3'
            myNotiPolicy.attribute['custId']=custId
            myNotiPolicy.name=name
            if event_src_id>0 and name!='Default for all rules':
                naturalId=self.dbHandler.execute(RULE_NATURAL_ID % event_src_id)[0][0]
                myNotiPolicy.attribute['naturalId']=naturalId
                myCond=notificationDataClass.notificationCondition()
                myCond.attribute['custId']=custId
                myCond.name=naturalId
                myCond.type='RULE'
                myNotiPolicy.conditions.append(myCond)
            deliver=self.dbHandler.execute(DELIVER % id)
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













