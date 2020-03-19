import os

path='../TestData/EventParsing/Snort'
addline='devEventTypeGrp=Misc activity'
files=os.listdir(path)
for file in files:
    if file.startswith('Snort-'):
        myF=open(path+'/'+file, 'a')
        myF.write(addline)
        myF.close()