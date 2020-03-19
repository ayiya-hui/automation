import os

PERL_CMD='perl sendRawIp.pl %s %s %s'

def sendRawIp(src_ip, remote_ip, fileName):
    myFile=open(fileName)
    myData=myFile.readlines()
    myFile.close()
    for data in myData:
        if data.strip():
            cmd=PERL_CMD % (src_ip, remote_ip, data.strip())
            print cmd
            os.system(cmd)

if __name__=='__main__':
    import sys
    src=sys.argv[1]
    dst=sys.argv[2]
    file=sys.argv[3]
    sendRawIp(src, dst, file)
