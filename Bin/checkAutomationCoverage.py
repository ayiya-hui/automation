from Libs.parserHandler import parserHandler
from Libs.ruleHandler import ruleHandler

categories={'EventParsing':parserHandler, 'Incident':ruleHandler}

def checkAutomationCoverage(server, cat):
    """Usage: checkAutomationCoverage.py <ao_server> <category>
    ao_server - AO Server IP address
    category - one of EventParsing, Incident, Report, etc.
    """
    myHandler=categories[cat](server)
    myHandler.checkNew(sysdefine=True)

if __name__=="__main__":
    import sys
    if len(sys.argv)!=3:
        print checkAutomationCoverage.__doc__
        sys.exit()
    server=sys.argv[1]
    cat=sys.argv[2]
    if cat not in categories.keys():
        print 'Category %s is not supported this. Only support: %s' % (cat, ','.join(categories.keys()))
        sys.exit()
    checkAutomationCoverage(server, cat)
    print '\nTask is done.'
