import queryHandler, sys, optparse
import ExpressionHandler
import listCompare
import timeUtility
import os
from stringBuilder import stringBuilder


EXP='%s\((\S+)\)'
DEFAULT='../%s/expressionTest'
DATA=DEFAULT % 'DataFiles'
RESULT=DEFAULT % 'Results'+'/'

parser=optparse.OptionParser()
parser.add_option("-o", "--option", dest="opt", metavar="OPTIONS", help="options")
parser.add_option("-f", "--file", dest="file", metavar="FILE", help="files")
(opts, args)=parser.parse_args()

if opts.opt:
    myOpt=opts.opt
else:
    myOpt=False

if opts.file:
    myFile=opts.file
else:
    myFile=False
    myStr.add('No data file to run test. Exit.')
    exit()

appServer=args[0]
folders=[]
if myFile.lower()=='all':
    folders=os.listdir(DATA)
else:
    folders.append(myFile)

myQuery=queryHandler.queryHandler()
endTime, uEndTime=timeUtility.getTimeNow(second=True)
for fileName in folders:
    myReader=open(DATA+'/'+fileName, 'r')
    myLines=myReader.readlines()
    myReader.close()
    myStr=stringBuilder()
    for line in myLines:
        myStr.add('Expression Query:')
        singleConstr, groupby, attr, orderby, outConstr, time, value=line.split(';')
        myStr.add('singleConstr: %s' % singleConstr)
        myStr.add('groupby: %s' % groupby)
        myStr.add('attrList: %s' % attr)
        startTime, uStartTime=timeUtility.getPastTime(endTime, time, value)
        myStr.add('Query duration is %s %s\nstart at %s(%s)\nend at %s(%s)' % (value.strip(), time.strip(), startTime, uStartTime, endTime, uEndTime))

        myQuery.getQuery(appServer, singleConstr, groups=groupby, orders=orderby, outputs=outConstr, filter=attr, absTimes=True, timeLow=uStartTime, timeHigh=uEndTime)
        expResult=myQuery.data
        myStr.add('Expression Query Result:')
        for data in expResult:
            myStr.add(data)

        missKey=[]
        if expResult:
            dataKeys=expResult[0].keys()
            for key in attr.split(','):
                if key not in dataKeys:
                    missKey.append(key)
        if missKey:
            myStr.add('Missing key: %s' % ','.join(missKey))
        if not myOpt:
            myExpress=ExpressionHandler.ExpressionHandler(appServer)
            oriResult, myStr=myExpress.getOriginalQuery(line, myStr, absTimes=True, timeLow=uStartTime, timeHigh=uEndTime)
            if expResult and oriResult:
                myCompare=listCompare.listCompare(expResult, oriResult)
                myStr=myCompare.compare(myExpress.nameKey, myExpress.valueKey, missKey, myStr)

                if myCompare.listCountMatch:
                    myStr.add('total counts: %s' % myCompare.totalCount)
                else:
                    myStr.add('matched data counts: %s' % len(myCompare.matchedData))
                    myStr.add('not matched data counts: %s' % len(myCompare.notMatchedData))

                if myCompare.match:
                    myStr.add('matched details:')
                    for data in myCompare.matchedData:
                        myStr.add(data)
                else:
                    myStr.add('Total %s NOT MACTHED' % len(myCompare.notMatchedData))
                    myStr.add('not matched details:')
                    for data in myCompare.notMatchedData:
                        myStr.add(data)
            else:
                myStr.add('Expresion query has no data. Skip the compare.')
        else:
            for data in expResult:
                myStr.add(data)

        myWriter=open(RESULT+'Result_'+fileName, 'w')
        myWriter.write(myStr.output())
        myWriter.close()
        print 'test for %s is done.' % fileName

print 'All tasks are done.'

