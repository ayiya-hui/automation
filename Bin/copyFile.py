import pexpect
import time

def copyFile(destHost, sourcePath, destPath, user, password, type):
    if type=="File":
        cmd='scp '+sourcePath+' '+user+'@'+destHost+':'+destPath
    else:
        cmd='scp -r '+path+' '+user+'@'+line.strip()+':/'
    child=pexpect.spawn(cmd)
    child.expect('password:')
    child.sendline(password)
    child.expect(pexpect.EOF)
    child.close()

if __name__=='__main__':
    import sys
    copyFile(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
