import os, csv
import Libs.CSVHandler as CSVHandler
import Libs.datFileHandler as datFileHandler
from ConfigConstants.TestConstant import event_data_keys, event_replace_symbol
from Models.testConfigs import testDataItem, testData, eventParsingData


titles={'EventParsing':'eventType,name,module,reptDevIpAddr,key,method'}
eventParsing_key='[reptDevIpAddr(key)]'
msg='[eventMsg]'
params='[params]'

token={'EventParsing':eventParsingData}

class caseDbHandler:
    def __init__(self, type):
        self.type=type
        self.dbPath='../TestData/'+type
        if type=='Incident':
            self.dbPath+='/IncidentMsgs'
        self.modules=[]
        self.index={}
        self.module_event_map={}

    def getAllModules(self):
        folders=os.listdir(self.dbPath)
        if '.svn' in folders:
            folders.remove('.svn')
        for file in folders:
            if '.dat' in file:
                file=file.replace('.dat', '')
            self.modules.append(file)

        return self.modules

    def getEventTypesInModule(self, module):
        indexPath=self.dbPath+'/'+str(module)+'/Index'
        indexData={}
        if os.path.exists(indexPath):
            self.index=CSVHandler.getDataFromFile('eventParsingData', indexPath, None, None, asCsv=False)
            map={}
            maxId=1
            for key in self.index:
                eventType=self.index[key].eventType
                id=int(self.index[key].name.split('_')[-1])
                if id>maxId:
                    maxId=id
                if eventType not in indexData.keys():
                    indexData[eventType]=[self.index[key]]
                else:
                    exist_cases=indexData[eventType]
                    exist_cases.append(self.index[key])
                    indexData[eventType]=exist_cases
            map['indexPath']=indexPath
            map['indexData']=indexData
            map['maxId']=maxId
            self.module_event_map[module]=map

    def createNewCases(self, data, method):
        if not self.modules:
            self.modules=self.getAllModules()
        for dat in data:
            isAdd=True
            change_case=[]
            if dat.module not in self.modules and not os.path.exists(self.dbPath+'/'+str(dat.module)):
                print 'Create new module: %s' % dat.module
                os.makedirs(self.dbPath+'/'+str(dat.module))
            caseData=token[self.type]()
            caseData.eventType=dat.eventType
            caseData.key=''
            caseData.method='syslog'
            caseData.module=dat.module
            caseData.reptDevIpAddr=dat.reptDevIpAddr
            self.getEventTypesInModule(caseData.module)
            exist_cases=[]
            indexPath=''
            if self.module_event_map:
                maxId=self.module_event_map[caseData.module]['maxId']
                exist_cases=self.module_event_map[caseData.module]['indexData']
                indexPath=self.module_event_map[caseData.module]['indexPath']
            else:
                maxId=0
                indexPath=self.dbPath+'/'+str(dat.module)+'/Index'
            if maxId:
                caseData.name=str(dat.module)+'_'+str(maxId+1)
            else:
                caseData.name=str(dat.module)+'_1'
            if exist_cases:
                if caseData.eventType in exist_cases.keys():
                    exist_case_list=exist_cases[caseData.eventType]
                    fileName=caseData.eventType+'.dat'
                    for rep in event_replace_symbol:
                        if rep in fileName:
                            fileName=fileName.replace(rep, '$')
                    myData=datFileHandler.getData(self.dbPath+'/'+str(caseData.module)+'/'+fileName, event_data_keys)
                    raw_match=False
                    for key in myData.dataMap.keys():
                        if dat.eventMsg==myData.dataMap[key].eventMsg:
                            raw_match=True
                    if not raw_match:
                        pass
                    else:
                        print 'duplicate case: %s' % caseData.eventType
                        isAdd=False
            if isAdd:
                if change_case:
                    print 'need to add codes to handle change cases'
                else:
                    print 'add new cases.'
                    self.writeCaseData(dat)
                    self.writeIndex(caseData, indexPath)

    def getDiffKey(self, exist_param, new_param):
        exist_map={}
        exist_keyValue=''
        new_keyValue=''
        for item in exist_param:
            name, value=item.split('=')
            if not name in exist_map.keys():
                exist_map[name]=value
        for key in exist_map.keys():
            if exist_map[key]!=new_param[key]:
                exist_keyValue=key+':'+exist_map[key]
                new_keyValue=key+':'+new_param[key]

        return exist_keyValue, new_keyValue

    def isEventParsingModuleExist(self, module):
        status=''
        if not self.modules:
            self.modules=self.getAllModules()
        if not module in self.modules:
            print 'Module %s is a new module.' % module
            status=False
        else:
            status=True

        return status

    def getCaseData(self, module):
        files=os.listdir(self.dbPath+'/'+str(module))
        if 'Index' in files:
            files.remove('Index')
        myIndexData={}
        if files:
            for file in files:
                myData=datFileHandler.getData(self.dbPath+'/'+str(module)+'/'+file, event_data_keys)
                myIndexData[file.split('.')[0]]=myData

        return myIndexData

    def getIndexPath(self, module):
        indexPath=''
        if module in self.auto_event_map.keys() and self.auto_event_map[module]['index']:
            indexPath=self.auto_event_map[module]['index']
        else:
            indexPath=self.dbPath+'/'+str(module)+'/Index'

        return indexPath

    def writeEventParsing(self, obj):
        new_name=obj.eventType
        for i in event_replace_symbol:
            if i in new_name:
                new_name=new_name.replace(i, '$')
        myWrite=open(self.dbPath+'/'+str(obj.module)+'/'+new_name+'.dat', 'a')
        myWrite.write(eventParsing_key+'\n')
        myWrite.write(obj.reptDevIpAddr+'\n')
        myWrite.write('[eventMsg]\n')
        myWrite.write(obj.eventMsg+'\n')
        myWrite.write('[params]\n')
        for item in obj.params.keys():
            if ('Geo' in item) or ('name' in item and 'HOST-' in obj.params[item]):
                myWrite.write(item + '=' + 'any\n')
            else:
                myWrite.write(item+'='+obj.params[item]+'\n')
        myWrite.close()

    token_write={'EventParsing':writeEventParsing,}

    def writeCaseData(self, obj):
        return self.token_write[self.type](self, obj)

    def writeIndex(self, obj, indexPath):
        exist=os.path.exists(indexPath)
        myWrite=open(indexPath, 'a')
        if not exist:
            myWrite.write(titles[self.type]+'\n')
        data_list=[obj.eventType, obj.name, obj.module, obj.reptDevIpAddr, obj.key, obj.method]
        data_string=','.join([str(x) for x in data_list])
        myWrite.write('\n'+data_string)
        myWrite.close()



