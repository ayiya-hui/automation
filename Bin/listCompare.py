import generalUtility

class listCompare:
    def __init__(self, list1, list2):
        self.list1=list1
        self.list2=list2
        self.matchedData=[]
        self.notMatchedData=[]
        self.notMatchedDetail=''

    def floatHandling(self, value):
        newValue=generalUtility.floatStrip(float(value))
        if '.' in newValue:
            finalValue=generalUtility.roundNumber(newValue, 2)
        else:
            finalValue=newValue

        return finalValue

    def compare(self, keyword, valueWord, missKey, buffer):
        buffer.add('expressionQuery: %s' % self.list1)
        buffer.add('total: %s' % len(self.list1))
        buffer.add('regularQuery: %s' % self.list2)
        buffer.add('total: %s' % len(self.list1))
        count1=len(self.list1)
        count2=len(self.list2)
        if count1==count2:
            self.listCountMatch=True
            self.totalCount=count1
        else:
            self.listCountMatch=False
            self.notMatchDetail='list1 count %s list2 count %s' % (count1, count2)
        for item1 in self.list1:
            for item2 in self.list2:
                if keyword and keyword not in missKey and keyword!='None':
                    keywordList=keyword.split(',')
                else:
                    keywordList=['NoKey']
                for keyitem in keywordList:
                    if keyitem=='NoKey':
                        match=True
                    elif item1[keyitem]==item2[keyitem]:
                        match=True
                    else:
                        match=False
                if match:
                    map={}
                    valueList=[]
                    for myKey in keywordList:
                        if myKey!='NoKey':
                            valueList.append(item1[myKey])
                    map['key']=','.join(valueList)
                    map['expressionQuery']=item1[valueWord]
                    map['regularQuery']=str(item2[valueWord])
                    buffer.add(map)
                    if '.' in map['expressionQuery']:
                        newVal1=self.floatHandling(map['expressionQuery'])
                    else:
                        newVal1=map['expressionQuery']
                    if '.' in map['regularQuery']:
                        newVal2=self.floatHandling(map['regularQuery'])
                    else:
                        newVal2=map['regularQuery']
                    if newVal1==newVal2:
                        self.matchedData.append(map)
                    else:
                        self.notMatchedData.append(map)
        if len(self.notMatchedData):
            self.match=False
        else:
            self.match=True

        return buffer




