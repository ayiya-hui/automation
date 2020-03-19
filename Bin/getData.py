from dbAccess import dbUtility

def getData(config):
    db=dbUtility(config.dbServer)
    db.connect()
    retData=[]
    for table in config.tableList:
        map={}
        cmd='Select * from '+table+';'
        data=db.execute(cmd)
        map['tableName']=table
        map['tableValue']=data
        retData.append(map)

    return retData
