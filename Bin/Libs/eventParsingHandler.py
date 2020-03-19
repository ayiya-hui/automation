from Libs.udpSendHandler import udpSendHandler
from Libs.appHandler import appHandler
from ConfigConstants.queryTemplate import query_xml, xml_escapes, str_escapes
from string import Template
import Util.classUtility as classUtility
from Libs.XmlHandler import XmlHandler
from Models.caseDataModel import eventParsingCase
import caseDbHandler
from Util.localhostIp import getLocalhostIp

constr_params={'rawmsg':'rawEventMsg = "%s"',
               'eventtype':'eventType = "%s"'}
ignore_attrs=set((
   'eventRuleTrigger',
   'hostGeoCity',
   'hostGeoCountry',
   'hostGeoLatitude',
   'hostGeoLongitude',
   'hostGeoOrg',
   'hostGeoState',
   'logoffTime',
   'logonTime',
   'reptGeoCountry',
   'reptGeoLatitude',
   'reptGeoLongitude',
   'reptGeoOrg',
   'scanEnd',
   'srcGeoCity',
   'srcGeoCountry',
   'srcGeoLatitude',
   'srcGeoLongitude',
   'srcGeoOrg',
   'srcGeoState',
   'timeSkewSec',
   'updateTime'
))
any_attrs=set((
   'destGeoCity',
   'destGeoCountry',
   'destGeoCountryCode',
   'destGeoLatitude',
   'destGeoLongitude',
   'destGeoOrg',
   'destGeoState',
   'deviceTime',
   'eventId',
   'hostGeoCity',
   'hostGeoCountry',
   'hostGeoLatitude',
   'hostGeoLongitude',
   'hostGeoOrg',
   'hostGeoState',
   'phRecvTime',
   'postNATSrcGeoCity',
   'postNATSrcGeoCountry',
   'postNATSrcGeoLatitude',
   'postNATSrcGeoLongitude',
   'postNATSrcGeoOrg',
   'postNATSrcGeoState',
   'rawEventMsg',
   'reptGeoCity',
   'reptGeoCountry',
   'reptGeoLatitude',
   'reptGeoLongitude',
   'reptGeoOrg',
   'reptGeoState',
   'srcGeoCity',
   'srcGeoCountry',
   'srcGeoCountryCode',
   'srcGeoLatitude',
   'srcGeoLongitude',
   'srcGeoOrg',
   'srcGeoState'
))
address_attrs=['destIpAddr', 'relayDevIpAddr', 'srcIpAddr', 'reptDevIpAddr']

class eventParsingHandler:
    def __init__(self, server, mod=False):
        self.udphandler=udpSendHandler(server)
        self.appHandler=appHandler(server)
        self.module_name=mod
        self.localhost=getLocalhostIp()

    def send(self, event, name=False):
        self.udphandler.sendEvent(event, 'syslog')

    def get(self, event, tag):
        newCase=''
        myTemp=Template(query_xml)
        new_event=self.handleXmlEscape(event)
	new_event=self.handleStrEscape(new_event)
        if tag not in constr_params.keys():
            print '%s tag is not supported.' % tag
            import sys
            sys.exit()
        myMap={}
        myMap['constr']=constr_params[tag] % new_event
        myMap['minute']=60*24
        inXml=myTemp.substitute(myMap)
        self.appHandler.getQuery(inXml)
        outRet=self.appHandler.queryXml
        if outRet:
            outXml=outRet[0]
            newCase=self.processsXml(outXml)
            if newCase:
                print 'New case eventType: %s' % newCase.eventType
        final_case=[]
        if newCase:
            final_case=self.processCase(newCase)

        return final_case

    def processsXml(self, xml):
        myCase=''
        objlist=XmlHandler().XmlStringToObj(xml, keyword='events')
        if objlist:
            obj=objlist[-1]
            myCase=eventParsingCase()
            myCase.eventType=obj.eventType
            for attr in obj.attributes:
                if not attr.name in myCase.params.keys() and not attr.name in ignore_attrs:
                    if attr.name in any_attrs:
                        myCase.params[attr.name]='any'
                        if attr.name=='rawEventMsg':
                            myCase.eventMsg=attr.value
                    elif attr.name in address_attrs:
                        if attr.value==self.localhost:
                            myCase.params[attr.name]='$localhost'
                        else:
                            myCase.params[attr.name]=attr.value
                    elif attr.name=='phCustId':
                            myCase.params[attr.name]='$sender'
                    else:
                            myCase.params[attr.name]=attr.value
                else:
                    if not attr.name in ignore_attrs and not attr.value==myCase.params[attr.name]:
                        if len(attr.value)>len(myCase.params[attr.name]):
                            myCase.params[attr.name]=attr.value
            if 'parser' in myCase.params.keys():
                myCase.module=myCase.params['parser']
            else:
                myCase.module=self.module_name
        else:
            print 'No case returned'

        return myCase

    def handleXmlEscape(self, event):
        for i in xml_escapes:
            event=event.replace(i[0],i[1])
        return event
	
    def handleStrEscape(self, event):
	for i in str_escapes:
	    event=event.replace(i[0],i[1])
	return event

    def addNew(self, newCases):
        myCaseDb=caseDbHandler.caseDbHandler('EventParsing')
        myCaseDb.createNewCases(newCases, 'syslog')

    def processCase(self, case):
        for item in ['reptDevIpAddr', 'hostIpAddr']:
            if item in case.params.keys() and case.params[item] not in case.eventMsg:
                case.params[item]='$localhost'
        case.reptDevIpAddr=case.params['reptDevIpAddr']
        if 'relayDevIpAddr' in case.params.keys() and case.params['relayDevIpAddr'] not in case.eventMsg:
            case.params['relayDevIpAddr']=case.reptDevIpAddr
        if 'reptDevName' in case.params.keys() and case.params['reptDevName'].startswith('HOST-'):
            case.params['reptDevName']='any'
        if 'collectorId' in case.params.keys():
            case.params['collectorId']='any'
        if 'rawEventMsg' in case.params.keys():
            case.params['rawEventMsg']='any'
        for key in case.params.keys():
            if case.params[key] is None:
                case.params.pop(key)

        return case

    def close(self):
        self.udphandler.close()

