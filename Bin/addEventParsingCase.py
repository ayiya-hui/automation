from Libs.CaseHandler import caseHandler
from Libs.parserHandler import parserHandler
from Libs.udpSendHandler import udpSendHandler
import time
import sys

def addEventParsingCase(server, key=False, data=False, raw_msg=True, module=False):
    """Usage: addEventParsingCase.py <server_ip> [-k <keyword> -f <file> -r True]
    server_ip -- AO server IP address
    -k -- eventType with keyword such as Cisco-
    -f -- file path. if option r is not added, it contains raw event message. If option r is added, it contains event type.
    -r --if added, it means file containing event type.
    -m --module name for test case.
    """
    #if raw_msg is true, then we need to send out the message and query using rawmsg; otherwise, we query using eventtype
    myCase=caseHandler(server, module=module)
    new_event=[line.strip() for line in data]
    new_cases=[]
    if raw_msg:
        mySend=udpSendHandler(server)
        for d in data:
            mySend.sendEvent(d.strip(), 'syslog')
        mySend.close()
        print 'It will take five minutes to parse the events, please wait.'
        for i in xrange(300,0,-1):
            sys.stdout.write('Parsing remaining: %d seconds \r' % (i))
            sys.stdout.flush()
            time.sleep(1)
        for e in new_event:
            new_case=myCase.query(e, 'rawmsg')
            if new_case:
                new_cases.append(new_case)
    else:
        if key:
            new_cases=myCase.queryAll(key)
        else:
            for e in new_event:
                new_case=myCase.query(e, 'eventtype')
                if new_case:
                    new_cases.append(new_case)
    if new_cases:
        myCase.addNew(new_cases)
    else:
        print 'Not add new cases.'

if __name__=='__main__':
    from optparse import OptionParser
    import sys, os
    parser=OptionParser()
    parser.add_option('-k', '--keyword', dest='keyword', help='keyword')
    parser.add_option('-f', '--filename', dest='filename', help='filename either contain raw message or event type')
    parser.add_option('-r', '--rawmsg', action="store_false", dest='rawmsg', help='whether raw event message or event type')
    parser.add_option('-m', '--module', dest='module', help='module name')
    options, args=parser.parse_args()
    if len(args)!=1:
        print addEventParsingCase.__doc__
        sys.exit()
    server=args[0]
    keyword=''
    if options.keyword:
        keyword=options.keyword
    filename=''
    file_data=''
    if options.filename:
        filename=options.filename
        if not os.path.exists(filename):
            print '%s is not exist.' % filename
            sys.exit()
        myF=open(filename)
        file_data=myF.readlines()
        myF.close()
    rawmsg=False if options.rawmsg is False else True
    module_name=False
    if options.module:
        module_name=options.module
    addEventParsingCase(server, key=keyword, data=file_data, raw_msg=rawmsg, module=module_name)
    print '\ntask is done'
