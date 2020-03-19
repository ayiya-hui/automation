import logging
import SshHandler
import ScpHandler
import compareTestResult
import os

DEST_IP='[destIP]='
OBJECT='[object]='
PRECMDS=['cd /', 'ls MyFileMonitor']
CONDITION='No such file or directory'
POSTCMDS=['mkdir MyFileMonitor', 'mkdir MyFileMonitor/All', 'mkdir MyFileMonitor/Attrib', 'mkdir MyFileMonitor/Close', 'mkdir MyFileMonitor/Create', 'mkdir MyFileMonitor/Delete', 'mkdir MyFileMonitor/Modify', 'mkdir MyFileMonitor/Open']

def runLinuxFileMonitor(config, testSuite):
    option=config['option']
    param=[]
    mySSH=SshHandler.SshHandler(testSuite.linuxHost, testSuite.linuxUser, testSuite.linuxPassword)

    #check test folders
    preCmdList=PRECMDS
    cond=CONDITION
    postCmdList=POSTCMDS
    mySSH.runCmd(preCmdList, condition=cond, commandList=postCmdList)

    #create config file, copy then remove
    pathList=testSuite.monConfig.split('#')
    setupConfigFile(config['dataCollector'], pathList)
    mySCP=ScpHandler(testSuite.linuxHost, testSuite.linuxUser, testSuite.linuxPassword)
    removeConfigFile()
    for case in testSuite.testcases:
        mapping={}
        for task in case.tasks:
            cmdList=getTaskCmd(task)
        myPath=task.targetPath.split(',')
        commands=[]
        for path in myPath:
            commands.append('cd '+path)
            for cmd in cmdList:
                commands.append(cmd)

        output=mySSH.runCmd('/LinuxFileMonitor', './LinuxFileMon')

        if option!='SendOnly':
            if case.createEvent=='False':
                mapping['errorMsg']=output
                mapping['caseName']=case.name
                param.append(mapping)
            else:
                fileHandle=open('../DataFiles/'+config[testTask]+'/')

    mySSH.logout()
    finalResult=None
    if option!='SendOnly':
        finalResult=compareTestResult.runCompareResult(config, testSuite, param)

    return finalResult

def setupConfigFile(ipAddress, pathList):
    fileHandler=open('linuxFileMon.conf', 'w')
    fileHandler.writeline(DEST_IP+ipAddress)
    for path in pathList:
        fileHandler.writeline(OBJECT+path)
    fileHandler.close()

def removeConfigFile():
    os.system('rm -f linuxFileMon.conf')

def getTaskCmd(task):
    cmdList=[]
    targets=[]
    if task.recurse!='':
        for i in range(int(task.recurse)):
            targets.append(task.target+str(i))

    if task.taskName=='Create':
        if taskType=='File':
            cmd='touch'
        else:
            cmd='mkdir'
    elif task.taskName=='Delete':
        if taskType=='File':
            cmd='rm -f'
        else:
            cmd='rm -rf'
    elif task.taskName=='Open':
        if taskType=='File':
            cmd='more'
        else:
            cmd='ls'
    elif task.taskName=='Rename':
        cmd='mv'
    elif task.taskName=='Attribute':
        cmd='chmod 777'

    for target in targets:
        cmdList.append(cmd+' '+target)

    return cmdList


