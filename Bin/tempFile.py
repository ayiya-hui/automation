import Libs.XmlHandler as XmlHandler
from Models.autoTestResultClass import TestSuiteResult, TestCaseResult

MyObj=TestSuiteResult()
MyObj.name='haha'
MyObj.fileName='some file'
MyObj.totalRun=100
MyObj.totalPass=50
MyObj.totalNoReturn=0
MyObj.totalFail=50
MyObj.totalMissing=0
MyObj.totalExtra=0
caseList=[]
for i in range(10):
    MyCase=TestCaseResult()
    MyCase.name='Name'+str(i)
    MyCase.status='Pass'
    MyCase.Pass=[]
    MyCase.Fail=[]
    MyCase.Missing=[]
    MyCase.Extra=[]
    caseList.append(MyCase)

MyObj.caseList=caseList

myXml=XmlHandler.XmlHandler()
myNode=myXml.XmlObjToString(MyObj)

print myNode.toxml()
