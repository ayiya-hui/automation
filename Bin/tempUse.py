total=100
myFile=open('orgIncludeFile.txt', 'w')
for i in range(total):
    myFile.write('192.168.1.'+str(i+1)+'\n')
myFile.close()


