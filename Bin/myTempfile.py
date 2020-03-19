import os

title='[eventMsg]'
path='../TestData/LogDiscover/logDiscoverMsgs'

folders=os.listdir(path)
for file in folders:
    myFile=open(path+'/'+file)
    myData=myFile.read()
    myFile.close()
    myWrite=open(path+'/'+file, 'w')
    myWrite.write(title+'\n')
    myWrite.write(myData)
    myWrite.close()

print 'Done'
