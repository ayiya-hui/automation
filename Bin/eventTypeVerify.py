from processCSV import getOriData

def eventTypeVerify(fileName=False):
    if fileName:
        oriData=getOriData(files=fileName)
    else:
        oriData=getOriData()


