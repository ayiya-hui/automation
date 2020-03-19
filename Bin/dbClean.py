import dbAccess

def DbClean(config):
    if config['testTask'] in ['incident', 'incidentPatternBased', 'incidentTimeBased']:
        if 'dbServer' in config.keys():
            dbServer=config['dbServer']
        else:
            dbServer=config['appServer']

        myDb=dbAccess.dbUtility(dbServer)
        myDb.connect()
        cmd1="DELETE FROM ph_incident;"
        cmd2="DELETE FROM ph_incident_detail;"
        re1=myDb.execute(cmd1)
        re2=myDb.execute(cmd2)

        myDb.close()


