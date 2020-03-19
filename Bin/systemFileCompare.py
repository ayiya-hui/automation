import os, re
import Libs.sshHandler as sshHand


path='/opt/phoenix'
cmd='ls -l '
charset_exp='\\x1b\[00;[\d]{2}m(?P<name>\S+)\\x1b\[00m'
ignores=['cache']

exp=re.compile(charset_exp)


def systemFileCompare(ip1, ip2):
    """This function will compare two systems for files difference."""
    files=getFolder(ip1, path)
    another_files=getFolder(ip2, path)
    miss_files=[]
    extra_files=[]
    for file in files:
        if file not in another_files:
            miss_files.append(file)
    for file in another_files:
        if file not in files:
            extra_files.append(file)

    if miss_files:
        print 'Files in %s, but not in %s:' % (ip1, ip2)
        for file in miss_files:
            print file

    if extra_files:
        print 'Files not in %s, but in %s:' % (ip2, ip2)
        for file in extra_files:
            print file


def getFolder(ip, folder_path):
    files=[]
    mySsh=sshHand.SshHandler(ip)
    value=mySsh.runCmd([cmd+folder_path]).split('\n')
    fvalue=value[2:-1]
    if fvalue:
        for item in fvalue:
            name=item.strip().split()[-1]
            if item.startswith('dr'):
                new_name=''
                ret=exp.search(item)
                if ret:
                    new_name=ret.group('name')
                if new_name and new_name not in ignores:
                    new_path=folder_path+'/'+new_name
                    sub_files=getFolder(ip, new_path)
                    for sub in sub_files:
                        if sub not in files:
                            files.append(sub)
                        else:
                            print 'duplicate file: %s' % sub
            else:
                new_path=folder_path+'/'+name
                if new_path not in files:
                    files.append(new_path)
                else:
                    print 'duplicate file: %s' % new_path


    return files

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print systemFileCompare.__doc__
        sys.exit()

    systemFileCompare(sys.argv[1], sys.argv[2])
