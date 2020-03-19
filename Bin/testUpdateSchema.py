import dbUpgradeHandler
import sys

dbServer=sys.argv[1]
version=sys.argv[2]
myDb=dbUpgradeHandler.dbUpgradeHandler(dbServer)
myDb.getUpgradeDatafromSQL(version)
print 'verify the version:'
dbVer=myDb.getDbVersion()
if version==dbVer:
    print 'version is %s as expected.' % dbVer
else:
    print 'version is NOT correct. Expect %s, Actual %s, Exit.' % (version, dbVer)
    exit()

print 'verify new tables:'
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

print 'Task finished.'

