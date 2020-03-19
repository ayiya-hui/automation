import ruleDataClass
import appHandler
import XMLHelper
import xml.dom.minidom as dom
from xml.parsers.expat import ExpatError
from xml.dom.minidom import parseString
from classUtility import *

GET_RULE='config/rule'

class ruleHandler:
    def __init__(self, appServer):
        self.appHandler=appHandler.appHandler(appServer)

    def getAllRulesfromREST(self):
        self.appHandler.getData(GET_RULE)
        #remove extra useless eventFilters entry as '<eventFilters>EventFilter@591783</eventFilters>
        doc=parseString(self.appHandler.xml)
        nodes=doc.getElementsByTagName('rules')
        if len(nodes):
            for name, element in XMLHelper._getElementChilds(nodes[0]):
                for subName, subElement in XMLHelper._getElementChilds(element):
                    if subName=='eventFilters':
                        lastChild=XMLHelper._getElementChilds(subElement)
                        if not len(lastChild):
                            subElement.parentNode.removeChild(subElement)
                            subElement.unlink()

            rules=XMLHelper.unpickle(XMLHelper._getElementChilds(nodes[0]), type='list')
            #index with naturalId
            self.rules={}
            for rule in rules:
                self.rules[rule.attribute['naturalId']]=rule

    def getAllRuleAnalysis(self):
        if not hasattr(self, 'rules'):
            self.getAllRulesfromREST()
        self.ruleAnalysis={}
        for key in self.rules.keys():
            rule=self.rules[key]
            ruleAnalyst=ruleDataClass.ruleAnalyst()
            ruleAnalyst.id=key
            ruleAnalyst.incidentType=rule.incidentType.split('$')[-1]
            ruleAnalyst.name=rule.name
            ruleAnalyst.singleConstraint=rule.eventFilters.singleConstraint
            ruleAnalyst.groupConstraint=rule.eventFilters.groupConstraint
            ruleAnalyst.groupBy=rule.eventFilters.groupBy.split(',')
            self.ruleAnalysis[ruleAnalyst.name]=ruleAnalyst

if __name__=='__main__':
    appServer='192.168.20.116'
    myRule=ruleHandler(appServer)
    myRule.getAllRulesfromREST()
    myRule.getAllRuleAnalysis()
    for key in myRule.ruleAnalysis.keys():
        for name in getAttrList(myRule.ruleAnalysis[key]):
            if name=='groupConstraint':
                print '%s: %s' % (name, getattr(myRule.ruleAnalysis[key], name))

    print 'done'



