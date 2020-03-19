import XMLHelper
import configModel
import xml.dom.minidom as dom
import randomGen
import getAdd


def createRules():
    pass

    return 1

def getInactiveRules(appServer):
    ruleDbParam,reptDbParam=getAdd.getAddFromDB(appServer)
    inActive=[]
    for rule in ruleDbParam.keys():
        if ruleDbParam[rule]['Active']==False:
            inActive.append(ruleDbParam[rule]['Id'])

    return inActive



if __name__=='__main__':
    import sys
    import ComHandler

    DEFAULT_ADMIN="super/admin"
    DEFAULT_PASSWORD="admin*1"
    appServer=sys.argv[1]

    dbServer='192.168.20.118'
    param=getInactiveRules(dbServer)
    if len(param):
        myString=','.join(param)
        inXml='<id>'+myString+'</id>'
        #inXml='<rules><rule id="4544388"><incidentFireFreq>30</incidentFireFreq></rule></rules>'
        myHandler=ComHandler.comHandler(appServer, appServer, DEFAULT_ADMIN, DEFAULT_PASSWORD)
        queryString="rule/activateAll"
        myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
    else:
        print 'No inactive rules in system.'

    print "Done"


