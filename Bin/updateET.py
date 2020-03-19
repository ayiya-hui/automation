import os, socket

PATH='/opt/phoenix/data-definition/eventType'

def updateET():
    localhost=socket.gethostbyname(socket.gethostname())
    fileList=os.listdir(PATH)
    if 'README' in fileList:
            fileList.remove("README")
    if 'phoenix-eventtype.csv.old' in fileList:
        fileList.remove("phoenix-eventtype.csv.old")

    for name in fileList:
         print "Import %s" % name
         cmd="/opt/phoenix/deployment/phoenixCLI.sh import -host "+localhost+" -port 8181 -cust system -user admin -pass 'Kd8@paL5Dcy' -type ET -file /opt/phoenix/data-definition/eventType/"+name
         os.system(cmd)
         print "%s is done" % name

    print "All import are done."

if __name__=='__main__':
    updateET()


