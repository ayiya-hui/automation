import dbAccess

def clearActiveIncident(dbServer):
    myDb=dbAccess.dbUtility(dbServer)
    myDb.connect()
    cmd1="update ph_incident set incident_status = 2 where incident_status = 0;"
    re1=myDb.execute(cmd1)

    myDb.close()

if __name__=='__main__':
    import sys
    clearActiveIncident(sys.argv[1])
    print "Done"
