import Libs.dbUpgradeHandler as dbHandler

def dbSchemaChange(dbServer, version):
    """Usage: dbSchemaChange.py <dbServer> <version>"""
    myDb=dbHandler.dbUpgradeHandler(dbServer)
    data=myDb.getUpgradeDatafromSQL(version)
    for table in myDb.newTables.keys():
        print 'new table: %s' % table
        if myDb.isTableExist(table):
            myData=myDb.getTableAttr(table)
            myDb.compareAttr(table, myData)
    print 'verify new columns in existing tables:'
    for table in myDb.alterTables.keys():
        print 'existing table: %s' % table
        myData=myDb.getTableAttr(table)
        myDb.compareAttr(table, myData)


if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print dbSchemaChange.__doc__
        sys.exit()
    dbServer=sys.argv[1]
    version=sys.argv[2]
    dbSchemaChange(dbServer, version)

    print 'Task Finished.'
