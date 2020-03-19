from Libs.incidentHandler import incidentHandler

def queryIncident(server, id):
    """
    Usage: queryIncident.py <appServer> <incidentId>
    """
    myIncidentHandler=incidentHandler(server)
    data=myIncidentHandler.getByIncidentId(id)

    return data

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print queryIncident.__doc__
        sys.exit()
    server=sys.argv[1]
    id=sys.argv[2]
    data=queryIncident(server, id)
    print data
    print '\nTask is done.'
