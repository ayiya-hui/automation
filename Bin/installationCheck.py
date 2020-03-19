import dbAccess
import CSVHandler


class installationCheck:
    def __init__(self, dbServer):
        self.dbAccess=dbAccess.dbUtility(dbServer)

    def connect(self):
        self.dbAccess.connect()

    def close(self):
        self.dbAccess.close()

    def getCVSData(self):
        param=CSVHandler.getData()
        self.csvEventType=param


    def getEventType(self):
        typeData=self.dbAccess.execute('Select id, name, description, severity, device_type_id from ph_event_type')
        param=[]
        for type in typeData:
            map={}
            map['eventType']=type[1]
            map['eventName']=type[2]
            map['severity']=type[3]
            map['model'],map['vendor'],map['version']=self.getDeviceType(type[4])
            map['group']=self.getGroup(type[0])
            param.append(map)
        self.dbEventType=param

    def getDeviceType(self, id):
        model=''
        vendor=''
        version=''
        if id>0:
            devicetypeData=self.dbAccess.execute('Select model, vendor, version from ph_device_type where id = '+str(id))
            model=devicetypeData[0][0]
            vendor=devicetypeData[0][1]
            version=devicetypeData[0][2]

        return model,vendor,version

    def getGroup(self, id):
        name=''
        itemData=self.dbAccess.execute('Select group_id from ph_group_item where item_id = '+str(id))
        if len(itemData)!=0:
            groupId=itemData[0][0]
            groupData=self.dbAccess.execute('Select name from ph_group where id = '+str(groupId))
            name=groupData[0][0]

        return name

    def getEventTypeDiff(self):
        csvCount=len(self.csvEventType)
        dbCount=len(self.dbEventType)
        diff1=[]
        diff2=[]
        good=[]
        if csvCount != dbCount:
            csvNames=[]
            for item in self.csvEventType:
                if 'eventType' in item:
                    csvNames.append(item['eventType'])

            dbNames=[]
            for item in self.dbEventType:
                dbNames.append(item['eventType'])

            for item in dbNames:
                if item not in csvNames:
                   diff1.append(item)
                else:
                    good.append(item)

            for item in csvNames:
                if item not in dbNames:
                   diff2.append(item)

        self.good=good

        return diff1,diff2

    def compareGoodEntry(self):
        passed=[]
        failed=[]
        for item in self.csvEventType:
            if item['eventType'] in self.good:
                for entry in self.dbEventType:
                    if entry['eventType']==item['eventType']:
                        finalData={}
                        finalData['eventType']=item['eventType']
                        finalData['eventName']=item['eventName']+' vs '+entry['eventName']
                        finalData['severity']=item['severity']+' vs '+str(entry['severity'])
                        if 'group' not in item:
                            item['group']=''
                        finalData['group']=item['group']+' vs '+entry['group']
                        if 'model' not in item:
                            item['model']=''
                        finalData['model']=item['model']+' vs '+entry['model']
                        if 'vendor' not in item:
                            item['vendor']=''
                        finalData['vendor']=item['vendor']+' vs '+entry['vendor']
                        if 'version' not in item:
                            item['version']=''
                        finalData['version']=item['version']+' vs '+entry['version']
                        if entry['eventName']==item['eventName'] and entry['severity']==item['severity'] and entry['group']==item['group'] and entry['vendor']==item['vendor'] and entry['model']==item['model'] and entry['version']==item['version']:

                            passed.append(finalData)
                        else:

                            failed.append(finalData)

        return passed, failed





if __name__=='__main__':
    import sys
    myCheck=installationCheck(sys.argv[1])
    myCheck.getCVSData()
    myCheck.connect()
    myCheck.getEventType()
    myCheck.close()

    print 'Total numbers of eventType from CVS files: %s\n' % len(myCheck.csvEventType)
    print 'Total numbers of eventType from database: %s' % len(myCheck.dbEventType)

    diff1,diff2=myCheck.getEventTypeDiff()
    if len(diff1):
        print '%s Extra in DB:\n' % len(diff1)
        for item in diff1:
            print item

    if len(diff2):
        print '%s Missing from CSV:\n' % len(diff2)
        for item in diff2:
            print item

    #passed,failed=myCheck.compareGoodEntry()

    #if len(passed):
     #   print 'Passed eventTypes fileds:\n'
      #  for key in passed:
       #     print key

    #if len(failed):
     #   print 'Failed eventTypes fields:\n'
      #  for fail in failed:
       #     print fail



