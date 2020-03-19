from Libs.incidentHandler import incidentHandler
from Util.IPUtility import combineIP
import time, copy

default_timer=1

def incidentSender(app_server, types, differ=False, timer=default_timer, number=1):
    """Usage: incidentSender.py <app_server> -n <rule_type> -f <file_path> -t <sleep_time_in_minutes> -d True -c <total_number>"""
    myHandler=incidentHandler(app_server)
    paramMap={}
    rawMap={}
    print 'count: %i' % number
    for i in range(number):
        for incident_type in types:
            if incident_type not in paramMap.keys():
                param=myHandler.getTestRuleParameter(incident_type)
                if not param:
                    print 'incident type %s not implemented.' % incident_type
                    break
                paramMap[incident_type]=param
            myParam=''
            if differ:
                myParam=copy.deepcopy(paramMap[incident_type])
                myParam.reptDevIpAddr=combineIP(paramMap[incident_type].reptDevIpAddr, i)
            else:
                myParam=paramMap[incident_type]
            if myParam:
                if incident_type not in rawMap.keys():
                    rawData=myHandler.getRawData(incident_type)
                    rawMap[incident_type]=rawData
                myData=rawMap[incident_type]
                myHandler.trigger(myParam, myData.dataMap['default'].eventMsg)
                time.sleep(timer)

if __name__=='__main__':
    from optparse import OptionParser
    import os, sys
    parser=OptionParser()
    parser.add_option('-t', '--wait_time', dest='wait_time', help='time to wait for next send')
    parser.add_option('-d', '--differ', dest='differ', help='change the Reporting IP to create different incidents.')
    parser.add_option('-f', '--filename', dest='filename', help='incident types are in file.')
    parser.add_option('-n', '--name', dest='name', help='incident types are in name.')
    parser.add_option('-c', '--count', dest='count', help='count of incidents created.')
    options, args=parser.parse_args()
    if len(args)!=1:
        print incidentSender.__doc__
        sys.exit()
    app_server=args[0]
    types=[]
    if options.name:
        types=options.name.split(',')
    elif options.filename:
        file_path=options.filename
        if not os.path.exists(file_path):
            print 'File %s is not exist.' % file_path
            sys.exit()
        else:
            myR=open(file_path)
            myD=myR.readlines()
            myR.close()
            for line in myD:
                if line.strip():
                    types.append(line.strip())
    if not types:
        print 'No rule types to test.'
        sys.exit()
    differ_flag=False
    time_wait_flag=default_timer
    count=1
    if options.differ:
        differ_flag=True
    if options.wait_time:
        time_wait_flag=int(options.wait_time)
    if options.count:
        count=int(options.count)
    incidentSender(app_server, types, differ=differ_flag, timer=time_wait_flag, number=count)

