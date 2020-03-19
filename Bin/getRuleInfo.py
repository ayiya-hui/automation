from Libs.restApiDataHandler import restApiDataHandler
import Util.constraintUtility as constraintUtility
import Util.classUtility as classUtility
import expressionReader

correct_grammer_cases={'PH_RULE_ESX_DISKIO_CRIT':'(AVG(guestDiskRdLatency) >= 50 OR AVG(guestDiskWrLatency)) >= 50 AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_WARN':'((AVG(inIntfPktErrPct) >= 1 AND AVG(inIntfPktErrPct) <= 5) OR (AVG(outIntfPktErrPct) >= 1 AND AVG(outIntfPktErrPct) <= 5)) AND COUNT(*) >= 2',
                       'PH_RULE_NET_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',
                       'PH_RULE_SERVER_INTF_ERR_CRIT':'(AVG(inIntfPktErrPct) > 5 OR AVG(outIntfPktErrPct) > 5) AND COUNT(*) >= 2',}

def getRules(server):
    restApiHandler=restApiDataHandler(server)
    rawtestMap=restApiHandler.getData('rule')
    testMap={}
    for mapKey in rawtestMap.keys():
        if rawtestMap[mapKey].active=='true':
            if 'dataCreationType' in rawtestMap[mapKey].attribute.keys() and rawtestMap[mapKey].attribute['dataCreationType']=="SYSTEM" :
                testMap[mapKey]=rawtestMap[mapKey]

    indexMap={}
    for key in testMap.keys():
        incidentType=testMap[key].incidentType.split('$')[-1]
        indexMap[incidentType]=testMap[key]
    myFile=open('ruleInfo.txt', 'w')
    for key in indexMap.keys():

        myFile.write(key+'\n')
        print key
        groupCon=None
        groupby=None
        if classUtility.getType(indexMap[key].eventFilters[0].groupConstraint)!='NoneType':
            if type in correct_grammer_cases.keys():
                groupCon=correct_grammer_cases[type]
            else:
                groupCon=indexMap[key].eventFilters[0].groupConstraint

        """if classUtility.getType(indexMap[key].eventFilters[0].groupBy)!='NoneType':
            groupby=indexMap[key].eventFilters[0].groupBy
        else:
            groupby=None"""
        #single=indexMap[key].eventFilters[0].singleConstraint
        #valueMap=constraintUtility.processConstraint(single, groupBy=groupby, groupConstr=groupCon)
        #valueMap=expressionReader.expressionReader(groupCon, server)
        if groupCon:
            print groupCon
            myFile.write(groupCon+'\n')
        #myFile.write(str(valueMap['SingleConstriant'])+'\n')
        #print valueMap['SingleConstriant']
        """if groupCon:
            print groupCon
            print valueMap['GroupConstriant']
            myFile.write(groupCon+'\n')
            myFile.write(str(valueMap['GroupConstriant'])+'\n')   """
    myFile.close()

if __name__=='__main__':
    server='192.168.20.116'
    getRules(server)

