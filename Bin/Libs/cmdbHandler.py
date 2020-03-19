import psqlHandler
import Models.cmdbDataClass as cmdbDataClass
from Models.ClassLocator import getClassObj
import Util.classUtility as classUtility
import ConfigConstants.TestConstant as TestConstant



class cmdbHandler:
    """This class is for specific task of get CMDB data."""
    def __init__(self, dbServer):
        self.dbServer=dbServer
        self.dbHandler=psqlHandler.psqlHandler(self.dbServer)

    def getDomain(self, param=False):
        """This method gets all domains from CMDB."""
        cmd=self.__getCmd('domain', param=param)
        data=self.dbHandler.execute(cmd)
        indexData={}
        nameList=TestConstant.sql_values['domain']['TestConstant.sql_values']
        for item in data:
            map={}
            for i in range(len(nameList)):
                newName=self.__getTransName(nameList[i])
                map[newName]=item[i]
            myObj=locateClassInstance.getClassInstance((self.__getTransName('domain')))
            for name in map.keys():
                if 'Attribute-' in name:
                    myObj.attribute[name.split('-')[-1]]=map[name]
                else:
                    setattr(myObj, name, map[name])
            myParam=[myObj.attribute['custId'], 'admin']
            admin=self.getAdmin(param=myParam)
            myObj.adminUser=admin['login_id']
            myObj.adminPwd=admin['passcode']+'-'+admin['salt']+'-'+admin['alg']
            svcParam=['2', myObj.attribute['custId']]
            svc=self.getAdmin(param=svcParam)
            myObj.svcUser=myObj.attribute['custId']
            myObj.svcPwd=svc['passcode']+'-'+svc['salt']+'-'+svc['alg']
            indexData[map[TestConstant.sql_values['domain']['param']]]=myObj

        return indexData

    def getAdmin(self, param=False):
        """This method gets all admin users from CMDB."""
        cmd=self.__getCmd('ident', param=param)
        data=self.dbHandler.execute(cmd)
        indexData=[]
        nameList=TestConstant.sql_values['ident']['TestConstant.sql_values']
        for item in data:
            map={}
            for i in range(len(nameList)):
                newName=self.__getTransName(nameList[i])
                map[newName]=item[i]
            indexData.append(map)

        return indexData[0]

    def getGroupItem(self):
        """This method gets all group_items from CMDB."""
        cmd=self.__getCmd('group_item')
        data=self.dbHandler.execute(cmd)
        nameList=TestConstant.sql_values['group_item']['values']
        indexData={}
        for item in data:
           map={}
           for i in range(len(item)):
               map[nameList[i]]=item[i]
           indexKey=map['item_id']
           if indexKey not in indexData.keys():
               indexData[indexKey]=map['group_id']
           else:
               oldval=indexData[indexKey]
               oldval+=','+map['group_id']
               indexData[indexKey]=oldval

        return indexData

    def __getCmd(self, type, param=False):
        if param:
            myParam=TestConstant.sql_values[type]['param']
            if classUtility.getType(myParam)=='list':
                myStr=' where '
                for i in range(len(myParam)):
                    myStr+=myParam[i]+' = '+"'"+param[i]+"'"+' AND '
                myStr=myStr[0:-5]
            else:
                myStr=' where '+myParam+' = '+"'"+param+"'"
            cmd=TestConstant.sql_query % (', '.join(TestConstant.sql_values[type]['values']), TestConstant.sql_values[type]['tableName'])+myStr
        else:
            cmd=TestConstant.sql_query % (', '.join(TestConstant.sql_values[type]['values']), TestConstant.sql_values[type]['tableName'])

        return cmd

    def __getTransName(self, name):
        if name in TestConstant.sql_trans_names.keys():
            newName=TestConstant.sql_trans_names[name]
        else:
            newName=name

        return newName

