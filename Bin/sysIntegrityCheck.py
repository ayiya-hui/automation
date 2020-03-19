import os
import socket

DATA="/data"
LOCAL_MOUNT="/dev/sdb"
REMOTE_MOUNT="/eventdb/"
ARCHIVE="archive"
CACHE="cache"
CMDB="cmdb"
EVENTDB="eventdb"
SVN="svn"
ADMIN="admin"
ROOT_USER="root"
POSTGRES="postgres"
APACHE="apache"
OPT="/opt"
PHOENIX_DIR="/opt/phoenix"
GLASSFISH="glassfish"
JAVA="Java"
Java="java"
JDK="jdk1.6.0"
PHOENIX="phoenix"
VM="vmware"
BIN="bin"
CONFIG="config"
DATA_DEFINITION="data-definition"
DEPLOY="deployment"
LIB32="lib32"
LIB64="lib64"
LOG="log"
XML_DIR="/opt/phoenix/config/xml"
PBIN="/pbin"
PH_DOWNLOAD_IMAGE="phdownloadimage"
PH_DOWNLOAD_LICENSE="phdownloadlicense"
PH_INSTALL_LICENSE="phinstalllicense"
PH_UPGRADE_IMAGE="phupgradeimage"
ROOT="/root"
TMP="/tmp"
ANACONDA="anaconda-ks.cfg"
INSTALL_LOG="install.log"
INSTALL_SYS="install.log.syslog"
INITDB="initdb.log"
INITPHDB="initphdb.log"
POPDB="populatedb.log"
DBSCHEMA="dbschema.log"
DOWNLOADIMG="downloadimage.log"
UPGRADEIMG="upgradeimage.log"
UPGRADEPOP="upgrade-populatedb.log"


def sysIntegrityCheck(type, mount):
    localhost=socket.gethostname()
    localaddress=socket.gethostbyname(localhost)
    print 'This check is performed in host name %s IP address %s' % (localhost, localaddress)
    #check mount
    cmd="mount"
    mountLines=cmdReturn(cmd)
    if mount=="local":
        verifyFile(LOCAL_MOUNT, mountLines, '/data')
    else:
        verifyFile(REMOTE_MOUNT, mountLines, '/data')



    prefix='ls -al '
    #check /data
    cmd=prefix+DATA
    dataLines=cmdReturn(cmd)
    verifyFile(ARCHIVE, dataLines, DATA, ROOT_USER)
    verifyFile(CACHE, dataLines, DATA, ADMIN)
    verifyFile(CMDB, dataLines, DATA, POSTGRES)
    verifyFile(EVENTDB, dataLines, DATA, ADMIN)
    verifyFile(SVN, dataLines, DATA, APACHE)

    #check version
    cmd="cat /opt/phoenix/bin/VERSION"
    version=cmdReturn(cmd)
    print version[0]
    print version[1]

    #check directory structure
    cmd=prefix+OPT
    optLines=cmdReturn(cmd)
    verifyFile(GLASSFISH, optLines, OPT, ADMIN)
    verifyFile(JAVA, optLines, OPT, ROOT_USER)
    verifyFile(JDK, optLines, OPT, ROOT_USER)
    verifyFile(PHOENIX, optLines, OPT, ADMIN)
    verifyFile(VM, optLines, OPT, ROOT_USER)

    cmd=prefix+PHOENIX_DIR
    phoenixLines=cmdReturn(cmd)
    verifyFile(BIN, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(CACHE, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(CONFIG, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(DATA_DEFINITION, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(DEPLOY, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(Java, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(LIB32, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(LIB64, phoenixLines, PHOENIX_DIR, ADMIN)
    verifyFile(LOG, phoenixLines, PHOENIX_DIR, ADMIN)

    #check total of XML parsers
    cmd=prefix+XML_DIR
    xmlLines=cmdReturn(cmd)
    print 'XML parser files: %s' % xmlLines[0]

    prefix='ls -l '
    #check /pbin for upgrade script
    cmd=prefix+PBIN
    pbinLines=cmdReturn(cmd)
    verifyFile(PH_DOWNLOAD_IMAGE, pbinLines, PBIN)
    verifyFile(PH_UPGRADE_IMAGE, pbinLines, PBIN)
    verifyFile(PH_INSTALL_LICENSE, pbinLines, PBIN)
    verifyFile(PH_DOWNLOAD_LICENSE, pbinLines, PBIN)
    #check /root and tmp
    if type=='install':
        cmd=prefix+ROOT
        rootLines=cmdReturn(cmd)
        verifyLog(ANACONDA, rootLines, ROOT)
        verifyLog(INSTALL_LOG, rootLines, ROOT)
        verifyLog(INSTALL_SYS, rootLines, ROOT)

        cmd=prefix+TMP
        tmpLines=cmdReturn(cmd)
        verifyLog(INITDB, tmpLines, TMP)
        verifyLog(INITPHDB, tmpLines, TMP)
        verifyLog(POPDB, tmpLines, TMP)
    else:
        cmd=prefix+TMP
        tmpLines=cmdReturn(cmd)
        verifyLog(DBSCHEMA, tmpLines, TMP)
        verifyLog(DOWNLOADIMG, tmpLines, TMP)
        verifyLog(UPGRADEIMG, tmpLines, TMP)
        verifyLog(UPGRADEPOP, tmpLines, TMP)

def cmdReturn(cmd):
    fin, fout=os.popen4(cmd)
    lines=fout.readlines()

    return lines

def verifyFile(filename, lines, folder, word=None):
    exist="no"
    for line in lines:
        if filename in line:
            print '%s is in %s folder.' % (filename, folder)
            if word!=None:
                if word in line:
                    print '%s has owner %s' % (filename, word)
            print line
            exist="yes"
    if exist!="yes":
        print "%s is missing." % filename

def verifyLog(logName, lines, folder):
     exist="no"
     for line in lines:
         if logName in line:
            print '%s is in %s folder.' % (logName, folder)
            print line
            File=open('/'+folder+'/'+logName, 'r')
            data=File.readlines()
            File.close()
            if 'ERROR' in data or 'error' in data:
                print 'There are ERROR in %s' % logName
            else:
                print 'No ERROR in %s' % logName
            exist="yes"
     if exist!="yes":
         print '%s is missing.' % logName

if __name__=='__main__':
    import sys
    if len(sys.argv)!=3:
        print "Usage: sysIntegrityCheck type local|nfs"
    sysIntegrityCheck(sys.argv[1], sys.argv[2])
