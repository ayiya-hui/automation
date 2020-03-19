from restApiDataHandler import restApiDataHandler
from AutoTestUtil.getSystemVersion import getSystemVersion
from XmlHandler import XmlHandler
import Util.generalUtility as generalUtility
import Util.classUtility as classUtility
import Util.testUtility as testUtility
from ConfigConstants.TestConstant import obj_name_trans, obj_xml_wrap
from string import Template
from ConfigConstants.compareTemplate import html_content, compare_desc, content_body, table_body, table_row


MODULES=['rule', 'report', 'eventType']
HTTP_ERROR='HTTP Status 401'
OUT_FILE='/AutoAccelops/Public/compareTest.html'
IGNORE_LIST=['lastModified', 'creationTime','id', 'activatedTime', 'xmlId', 'entityVersion', 'incidentFired']

class compareTestHandler:
    def __init__(self, server1, server2, my_user1=False, my_password1=False, my_user2=False, my_password2=False, modules=False):
        self.server1Version=''
        self.server2Version=''
        self.server1=server1
        self.server2=server2
        self.handler1=restApiDataHandler(self.server1, user=my_user1, password=my_password1)
        self.handler2=restApiDataHandler(self.server2, user=my_user2, password=my_password2)
        self.data={}
        if modules:
            self.modules=modules
        else:
            self.modules=MODULES

    def test(self):
        self.server1Version=getSystemVersion(self.server1)
        self.server2Version=getSystemVersion(self.server2)
        for module in self.modules:
            data1=self.handler1.getData(module)
            data2=self.handler2.getData(module)
            myMap={}
            myMap['module_data'], myMap['module_key']=self.compareData(data1, data2)
            self.data[module]=myMap
        self.geneateHtml()

    def compareData(self, data1, data2):
        missKey, extraKey, commonKey=testUtility.processList(data1.keys(), data2.keys())
        keyMap={'common':str(len(commonKey)), 'missing':str(len(missKey)), 'extra':str(len(extraKey))}
        myData=[]
        errorMsg=''
        for key in commonKey:
            errorMsg=classUtility.compare(data1[key], data2[key], 'name', errorMsg, IGNORE_LIST)
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
        myCompareTemp=Template(compare_desc)
        myContentTemp=Template(content_body)
        myTableTemp=Template(table_body)
        myRowTemp=Template(table_row)
        myHtmlMap={}
        myDescMap={'server1':self.server1, 'server2':self.server2, 'server1_version':self.server1Version, 'server2_version':self.server2Version}
        myDesc=myCompareTemp.substitute(myDescMap)
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
