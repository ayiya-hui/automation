from string import Template
from udpSendHandler import udpSendHandler
from appHandler import appHandler
from ConfigConstants.queryTemplate import query_xml
from Models.geoLocationDataClass import geoLocationData
import Util.classUtility as classUtility
from XmlHandler import XmlHandler
import time
from httplib2 import Http

AO_test_event='Fri Oct 30 18:19:58 2009 $ip_address AccelOps-WinLog-WMI  [Category]="12548" [CategoryString]="Special Logon" [ComputerName]="sf1dc03.jha.local" [Data]="NULL" [EventCode]="4672" [EventIdentifier]="4672" [EventType]="4" [Logfile]="Security" [RecordNumber]="184035301" [SourceName]="Microsoft-Windows-Security-Auditing" [TimeGenerated]="20100505222910.681375-000" [TimeWritten]="20100505222910.681375-000" [Type]="Audit Success" [User]="(null)" [[Subject]][Security ID]="S-1-5-21-2090294290-982477196-2044928816-8675" [Account Name]="riverbedAdmin" [Account Domain]="JHA" [Logon ID]="0x550baff" [Privileges]="SeSecurityPrivilege,SeBackupPrivilege,SeRestorePrivilege,SeTakeOwnershipPrivilege,SeDebugPrivilege,SeSystemEnvironmentPrivilege,SeLoadDriverPrivilege,SeImpersonatePrivilege,SeEnableDelegationPrivilege,SeAssignPrimaryTokenPrivilege"'
event_query_constr='reptDevIpAddr IN (%s) AND eventType IN ("Win-Security-4672")'
web_address='http://freegeoip.net/csv/%s'
attr_orders=['reptDevIpAddr', 'reptGeoOrg', 'reptGeoCity', 'reptGeoState', 'reptGeoCountry', 'reptGeoLatitude', 'reptGeoLongitude']

class geoLocationHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.udphandler=udpSendHandler(self.appServer)
        self.apphandler=appHandler(self.appServer)
        self.event_template=Template(AO_test_event)
        self.query_template=Template(query_xml)
        self.http=Http()

    def getGeoInfo(self, ip_address):
        myAOData=self.getAOInfo(ip_address)
        myWebData=self.getWebInfo(ip_address)
        myGeoData=geoLocationData()
        for attr in attr_orders:
            ao=getattr(myAOData, attr)
            web=getattr(myWebData, attr)
            newValue='AO: '+str(ao)+' WEB: '+str(web)
            setattr(myGeoData, attr, newValue)

        return myGeoData

    def getAOInfo(self, ip_address):
        myMap={'ip_address':ip_address}
        event=self.event_template.substitute(myMap)
        #self.udphandler.sendEvent(event, 'syslog')
        #time.sleep(120)
        AOData=self.get(ip_address)


        return AOData

    def getWebInfo(self, ip_address):
        resp, content=self.http.request(web_address % ip_address, 'GET')
        WebInfo=''
        if resp['status']=='200':
            WebInfo=geoLocationData()
            WebInfo.reptDevIpAddr, h1, WebInfo.reptGeoCountry, h2, WebInfo.reptGeoState, WebInfo.reptGeoCity, h3, WebInfo.reptGeoLatitude, WebInfo.reptGeoLongitude, h4=content.split('","')
            WebInfo.reptDevIpAddr=WebInfo.reptDevIpAddr.replace('"', '')
        return WebInfo

    def get(self, ip_address):
        myMap={'constr':event_query_constr % ip_address}
        inXml=self.query_template.substitute(myMap)
        self.apphandler.getQuery(inXml)
        outRet=self.apphandler.queryXml
        data=''
        if outRet:
            outXml=outRet[0]
            data=self.processsXml(outXml)

        return data

    def processsXml(self, xml):
        myData=''
        obj=XmlHandler().XmlStringToObj(xml, keyword='events')
        if obj:
            myData=geoLocationData()
            attrs=classUtility.getAttrList(myData)
            for attr in obj[0].attributes:
                if attr.name in attrs:
                    setattr(myData, attr.name, attr.value)

        return myData
