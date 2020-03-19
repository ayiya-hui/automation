import os

path='../TestData/EventParsing'
folders=os.listdir(path)
for folder in folders:
    files=os.listdir(path+'/'+folder)
    for file in files:
        myFile=open(path+'/'+folder+'/'+file)
        data=myFile.read()
        myFile.close()
        data=data.replace('$Comma',',')
        myWrite=open(path+'/'+folder+'/'+file, 'w')
        myWrite.write(data)
        myWrite.close()

print 'done'
