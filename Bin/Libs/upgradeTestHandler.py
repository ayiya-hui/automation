from restApiDataHandler import restApiDataHandler
from AutoTestUtil.getSystemVersion import getSystemVersion
from XmlHandler import XmlHandler
import Util.generalUtility as generalUtility
import Util.classUtility as classUtility
import Util.testUtility as testUtility
from ConfigConstants.TestConstant import obj_name_trans, obj_xml_wrap
from string import Template
from ConfigConstants.upgradeTemplate import html_content, upgrade_desc, content_body, table_body, table_row


MODULES=['rule', 'report', 'eventType']
#MODULES=['report']
HTTP_ERROR='HTTP Status 401'
upgrade_path='../TestData/DbUpgrade/preData/%s'
pre_version='../TestData/DbUpgrade/preData/preVersion'
OUT_FILE='/AutoAccelops/Public/upgradeTest.html'
IGNORE_LIST=['lastModified', 'creationTime','id', 'activatedTime', 'xmlId', 'entityVersion', 'incidentFired']

class upgradeTestHandler:
    def __init__(self, server, my_user=False, my_password=False, modules=False):
        self.preVersion=''
        self.postVersion=''
        self.server=server
        self.handler=restApiDataHandler(self.server, user=my_user, password=my_password)
        self.data={}
        if modules:
            self.modules=modules
        else:
            self.modules=MODULES

    def preTest(self):
        myVer=getSystemVersion(self.server)
        for module in self.modules:
            data=self.handler.getData(module, pickle=False)
            if HTTP_ERROR in data:
                print 'Data error, check authentication'
                import sys
                sys.exit()
            else:
                myPath=upgrade_path % (module+'-'+self.server.replace('.', '_')+'.xml')
                myFile=open(myPath, 'w')
                myFile.write(data.encode("utf-8"))
                myFile.close()
        self.writePreVersion(myVer)

    def postTest(self):
        self.getPreVersion()
        self.postVersion=getSystemVersion(self.server)
        for module in MODULES:
            postData=self.handler.getData(module)
            preData=self.getModulePreData(module)
            myMap={}
            myMap['module_data'], myMap['module_key']=self.compareData(preData, postData)
            self.data[module]=myMap
        self.geneateHtml()

    def getPreVersion(self):
        myR=open(pre_version)
        self.preVersion=myR.read().strip()
        myR.close()

    def writePreVersion(self, version):
        myFile=open(pre_version, 'w')
        myFile.write(version)
        myFile.close()

    def getModulePreData(self, module):
        myPath=upgrade_path % (module+'-'+self.server.replace('.', '_')+'.xml')
        if module in obj_name_trans.keys():
            fiMod=obj_name_trans[module]
        else:
            fiMod=module
        if fiMod in obj_xml_wrap.keys():
            fiKey=obj_xml_wrap[fiMod]
        else:
            fiKey=generalUtility.getPlural(fiMod)
        oriData=XmlHandler().XmlFileToObj(myPath, keyword=fiKey)
        indexData={}
        for ori in oriData:
            if classUtility.getType(ori)!='NoneType':
                indexData[ori.attribute['naturalId']]=ori

        return indexData

    def compareData(self, preData, postData):
        missKey, extraKey, commonKey=testUtility.processList(preData.keys(), postData.keys())
        keyMap={'common':str(len(commonKey)), 'missing':str(len(missKey)), 'extra':str(len(extraKey))}
        myData=[]
        errorMsg=''
        for key in commonKey:
            errorMsg=classUtility.compare(preData[key], postData[key], 'name', errorMsg, IGNORE_LIST)
            myMap={}
            myMap['name']=key
            if errorMsg:
                myMap['status']='Mismatch'
                myMap['reason']=errorMsg
            else:
                myMap['status']='Match'
                myMap['reason']='No Error'
            myData.append(myMap)
        if len(missKey):
            for key in missKey:
                myMap={}
                myMap['name']=key
                myMap['status']='Missing'
                myMap['reason']='Not in compare system'
                myData.append(myMap)
        if len(extraKey):
            for key in extraKey:
                myMap={}
                myMap['name']=key
                myMap['status']='Extra'
                myMap['reason']='Not in base system'
                myData.append(myMap)

        return myData, keyMap

    def geneateHtml(self):
        myHtmlTemp=Template(html_content)
        myUpgradeTemp=Template(upgrade_desc)
        myContentTemp=Template(content_body)
        myTableTemp=Template(table_body)
        myRowTemp=Template(table_row)
        myHtmlMap={}
        myDescMap={'server':self.server, 'pre_version':self.preVersion, 'post_version':self.postVersion}
        myDesc=myUpgradeTemp.substitute(myDescMap)
        myHtmlMap={'description':myDesc}
        myContents=[]
        for key in self.data.keys():
            key_data=self.data[key]
            my_rows=[]
            for item in key_data['module_data']:
                my_rows.append(myRowTemp.substitute(item))
            myTBodyMap={'tableBody':''.join(my_rows)}
            myTBody=myTableTemp.substitute(myTBodyMap)
            myContentMap={'module_name':key, 'common': key_data['module_key']['common'], 'missing':key_data['module_key']['missing'], 'extra':key_data['module_key']['extra'], 'table':myTBody}
            myContents.append(myContentTemp.substitute(myContentMap))
        myHtmlMap['content']=''.join(myContents)
        myHtml=myHtmlTemp.substitute(myHtmlMap)
        myW=open(OUT_FILE, 'w')
        myW.write(myHtml)
        myW.close()

