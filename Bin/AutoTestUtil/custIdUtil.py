from IPy import IP
import types

def getCustIdbyName(customers, custName):
    """This method gets customer id by name."""
    custId=''
    for domain in customers:
        if domain.name.title()==custName.title():
            custId=domain.domainId

    return custId

def getCustNamebyId(customers, custId):
    """This method gets customer name by id."""
    custName=''
    for domain in customers:
        if domain.domainId==custId:
            custName=domain.name

    return custName

def getCustIdbyIp(customers, ipAddr, dataCollector):
    """This method gets customer id by IP addresss."""
    #check for collectors
    noCollect=True
    custId=[]
    for key in customers.keys():
        if hasattr(customers[key], 'collectors'):
            collectorList=customers[key].collectors
            if len(collectorList):
                for col in collectorList:
                    if col.ipAddr==dataCollector:
                        custId.append(col.name)
                        noCollect=False
    if noCollect:
        for key in customers.keys():
            #check exclude
            if not hasattr(customers[key], 'excludeRange'):
                #check include
                if type(customers[key].includeRange)!=types.NoneType:
                    result=__check(ipAddr, customers[key].includeRange)
                    if result:
                        custId.append(customers[key].domainId)
            else:
                if type(getattr(customers[key], 'excludeRange'))==types.NoneType:
                    #check include
                    if type(customers[key].includeRange)!=types.NoneType:
                        result=__check(ipAddr, customers[key].includeRange)
                        if result:
                            custId.append(customers[key].domainId)
                else:
                    result=__check(ipAddr, customers[key].excludeRange)
                    if not result:
                        if customers[key].includeRange!='':
                            result=__check(ipAddr, customers[key].includeRange)
                            if result:
                                custId.append(customers[key].domainId)
                    else:
                        break

    if len(custId)==1:
        value=custId[0]
    else:
        value="1"

    return value

def __check(ipAddr, data):
        result=False
        exStack=data.split(",")
        for single in exStack:
            if '-' not in single:
                if ipAddr==single:
                    result=True
                    break
            else:
                rangeLow, rangeHigh=single.split('-')
                myIp=IP(ipAddr).int()
                if myIp >= IP(rangeLow).int() and myIp <= IP(rangeHigh).int():
                    result=True
                    break
        return result
