import os

path='IncidentMsgs'

def removeSpace():
    folders=os.listdir(path)
    folders.remove('.svn')
    for item in folders:
        file=path+'/'+item
        myR=open(file)
        myD=myR.read()
        myR.close()
        if '[PH_DEV_' in myD:
	    new=myD.replace(', [', ',[')
	    myW=open(file, 'w')
            myW.write(new)
            myW.close()

if __name__=='__main__':
    removeSpace()
    print 'task done'
