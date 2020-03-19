import queryHandler, re
import ExpressionDataClass
import classUtility
import ExpressionUtility
import generalUtility
import timeUtility
import math

KEY_WORDS=['LAST','FIRST','Pctile95','PctChange','AVG','SUM', 'MIN', 'MAX', 'HourOfDay','DeviceToCMDBAttr']
KEY_EXPS='%s\(([^\)]+)\)'
DATE='(?P<Day>\S{3})\s+[\S]+\s+[\d]{2}\s+(?P<Hour>[\d]{2}):.*'
WEEKDAYS={'Mon':'1','Tue':'2','Wed':'3','Thu':'4','Fri':'5','Sat':'6','Sun':'7'}
NOKEY={'NoKey':''}
SEPERATOR='$SEPERATOR$'

class ExpressionHandler:
    def __init__(self, appServer):
        self.queryHandler=queryHandler.queryHandler()
        self.appServer=appServer

    def getOriginalQuery(self, line, buffer, absTimes=False, timeLow=False, timeHigh=False):
        expData, self.time, self.value=self.formatQuery(line)
        if absTimes:
            self.absTimes=True
            self.lowTime=timeLow
            self.highTime=timeHigh
        else:
            self.absTimes=False
        buffer.add('Regular Summary Query:')
        buffer.add('singleConstr: %s' % expData.singleConstr)
        buffer.add('groupby: %s' % expData.groupBy)
        buffer.add('attrList: %s' % expData.attr)
        if self.absTimes:
            self.queryHandler.getQuery(self.appServer, expData.singleConstr, groups=expData.groupBy, orders=expData.orderBy, outputs=expData.outConstr, filter=expData.attr, absTimes=self.absTimes, timeLow=self.lowTime, timeHigh=self.highTime)
        else:
            self.queryHandler.getQuery(self.appServer, expData.singleConstr, groups=expData.groupBy, orders=expData.orderBy, outputs=expData.outConstr, filter=expData.attr, timeUnit=self.time, timeValue=self.value)
        self.count=len(self.queryHandler.data)
        buffer.add(self.count)
        self.summary=self.queryHandler.data
        buffer.add('Regular Query Result:\n')
        for data in self.summary:
            buffer.add(data)
        #exit()
        if self.constrFilters:
            finalData=self.getFinalData(self.summary)
        else:
            finalData=self.summary
            if not hasattr(self, 'nameKey'):
                setattr(self, 'nameKey', self.displayFilter.exp)
            if not hasattr(self, 'valueKey'):
                setattr(self, 'valueKey', self.displayFilter.regular)
        buffer.add('Regular Query after processing:\n')
        for data in finalData:
            buffer.add(data)

        return finalData, buffer

    def formatQuery(self, line):
        expData=ExpressionDataClass.ExpressionData()
        expData.singleConstr, expData.groupBy, expData.attr, expData.orderBy, expData.outConstr, time, value=line.split(';')
        expData, self.constrFilters, self.groupbyFilter, self.displayFilter=ExpressionUtility.getConstrOperators(expData, self.appServer)

        return expData, time, value

    def getFinalData(self, summary):
        newList=[]
        exp=self.constrFilters[0].exp
        val=self.constrFilters[0].value
        if exp=='DeviceToCMDBAttr':
            for data in summary:
                map={}
                for key in data.keys():
                    map[key]=data[key]
                map[exp]=val.replace('"','')
                newList.append(map)
        elif exp in ['DayOfWeek', 'HourOfDay']:
            for constr in self.constrFilters:
                pattern=re.compile(DATE)
                if constr.attr in summary[0].keys():
                    myKey=constr.attr
                else:
                    print 'This test is NOT VALID. %s is NOT present in return data.' % constr.attr
                    print 'Using groupby param as replacement'
                    print 'Also replace it with display param'
                    newV=self.displayFilter.exp.split('##')[0]
                    self.displayFilter.exp=newV+'##'+self.groupbyFilter.regular
                    myKey=self.groupbyFilter.regular

                for data in summary:
                    map={}
                    value=pattern.search(data[myKey]).group(constr.exp.split('Of')[0])
                    if value in WEEKDAYS.keys():
                        value=WEEKDAYS[value]
                        if generalUtility.compareValues(constr.oper, value, constr.value): #apply condition
                            #use display list to construct
                            map[self.displayFilter.exp]=value
                            for attr in self.displayFilter.regular.split(','):
                                map[attr]=data[attr]
                            newList.append(map)
        elif exp in ['FIRST', 'LAST', 'Pctile95', 'PctChange', 'AVG', 'SUM', 'MIN', 'MAX']:
            newList=summary
        #group by
        finalList=[]
        keyList=[]
        if exp=='DeviceToCMDBAttr':
            finalList=newList
        elif exp in ['DayOfWeek', 'HourOfDay']:
            for data in newList:
                keyValue=data[self.groupbyFilter.exp]
                if keyValue not in keyList:
                    keyList.append(keyValue)
                    finalList.append(data)
                else:
                    for item in data.keys():
                        if 'COUNT' in item:
                            oldVal=''
                            for sub in finalList:
                                oldVal=int(sub[item])
                                sub[item]=str(oldVal+int(data[item]))

        elif exp in ['FIRST', 'LAST', 'Pctile95', 'AVG', 'SUM', 'MIN', 'MAX', 'PctChange']:
            myKeys=[]
            if self.groupbyFilter.regular:
                myRegKeys=self.groupbyFilter.regular.split(',')
                for data in newList:
                    map={}
                    for myReg in myRegKeys:
                        map[myReg]=data[myReg]
                    if map not in myKeys:
                        myKeys.append(map)
            else:
                myKeys.append(NOKEY)
            for newkey in myKeys:
                valueList=[]
                for data in newList:
                    matchList=[]
                    for item in newkey.keys():
                        if item=='NoKey':
                            matchList.append(True)
                        elif data[item]==newkey[item]:
                            matchList.append(True)
                        else:
                            matchList.append(False)
                    if not False in matchList:
                        if exp in ['LAST', 'FIRST', 'PctChange']:
                            map={}
                            if SEPERATOR in data['phRecvTime']:
                                myData=data['phRecvTime'].split(SEPERATOR)[0]
                            else:
                                myData=data['phRecvTime']
                            timeVal=timeUtility.getUTimeFromString(myData)
                            if data[self.groupbyFilter.value]:
                                dataVal=self.getDataVal(data[self.groupbyFilter.value])
                                map[timeVal]=dataVal
                                valueList.append(map)
                        else:
                            if data[self.groupbyFilter.value]:
                                dataVal=self.getDataVal(data[self.groupbyFilter.value])
                                valueList.append(float(data[self.groupbyFilter.value]))

                finalValue=self.getFinalValue(exp, valueList)
                map={}
                if newkey != NOKEY:
                    map=newkey
                map[self.displayFilter.exp]=finalValue
                finalList.append(map)

                setattr(self, 'valueKey', self.displayFilter.exp)
                setattr(self, 'nameKey', self.displayFilter.regular)

        if not hasattr(self, 'nameKey'):
            setattr(self, 'nameKey', self.displayFilter.exp)
        if not hasattr(self, 'valueKey'):
            setattr(self, 'valueKey', self.displayFilter.regular)

        return finalList

    def getDataVal(self, dataValue):
        myVal=''
        if '$SEPERATOR' in dataValue:
            dataValue=dataValue.split('$SEPERATOR$')[0]
        if ':' in dataValue:
            myVal=dataValue
        elif '.' in dataValue:
            myVal=float(dataValue)
        else:
            myVal=int(dataValue)

        return myVal

    def getFinalValue(self, exp, valueList):
        finalValue=''
        if exp=='MIN':
            valueList.sort()
            finalValue=valueList[0]
        elif exp=='MAX':
            valueList.sort()
            finalValue=valueList[-1]
        elif exp=='AVG':
            sum=0.00
            for val in valueList:
                sum+=val
            finalValue=sum/len(valueList)
        elif exp=='SUM':
            sum=0
            for val in valueList:
                sum+=val
            finalValue=sum
        elif exp=='Pctile95':
            valueList.sort()
            finalValue=round(generalUtility.percentile(valueList, 95), 2)
        elif exp in ['FIRST', 'LAST', 'PctChange']:
            keyList=[]
            for value in valueList:
                keyList.append(value.keys()[0])
            keyList.sort()
            firstKey=keyList[0]
            lastKey=keyList[-1]
            for value in valueList:
                if value.keys()[0]==firstKey:
                    firstValue=value[firstKey]
                if value.keys()[0]==lastKey:
                    lastValue=value[lastKey]
            if exp=='FIRST':
                finalValue=firstValue
            elif exp=='LAST':
                finalValue=lastValue
            elif exp=='PctChange':
                if firstValue==0:
                    finalValue=0
                else:
                    diff=math.fabs(lastValue-firstValue)
                    finalValue=round(100*diff/firstValue)

        return finalValue





