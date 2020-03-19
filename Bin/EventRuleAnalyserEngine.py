from deviceHandler import deviceHandler

def checkDeviceApprove(appServer, devIp):
    myHandler=deviceHandler(appServer)
    devs=myHandler.getApplicableDevices()
    if devs.approvedDevicesOnly=='true':
        exist=False
        for dev in devs.approvedDevices:
            if devIp==dev.accessIp:
                exist=True
        if exist:
            msg='ApproveDeviceOnly on and device %s is in the list.' % devIp
        else:
            msg='ApproveDeviceOnly on and device %s is not in the list' % devIp
    else:
        msg='ApproveDeviceOnly off'
        exist=True

    return exist, msg

if __name__=='__main__':
    import sys
    appServer=sys.argv[1]
    devIp=sys.argv[2]
    exist, msg=checkDeviceApprove(appServer, devIp)
    print msg

