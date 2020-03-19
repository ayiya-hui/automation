from Libs.deviceHandler import deviceHandler
from Util.randomGen import getRandomIPAddr, getRandomNum
from ConfigConstants.deviceTemplate import create_device_info

def createDevice(appServer, opt='cmdline', num=1, file='', device_ip='', device_name='', device_type=''):
    """
    This program will create device by simulation of discovery.
    """
    deviceTypes=create_device_info.keys()
    data=[]
    if opt=='random':
        for i in range(num):
            map={}
            map['device_ip']=getRandomIPAddr()
            map['device_name']='host-'+map['device_ip']
            map['device_type']=deviceTypes[int(getRandomNum(0,len(deviceTypes)-1))]
            data.append(map)
    elif opt=='file':
        myFile=open(file)
        myData=myFile.readlines()
        myFile.close()
        for item in myData:
            if item:
                map={}
                map['device_ip'], map['device_name'], map['device_type']=item.strip().splilt(',')
                if not map['device_name']:
                    map['device_name']='host-'+map['device_ip']
                data.append(map)
    elif opt=='cmdline':
        map={}
        map['device_ip']=device_ip
        if device_name:
            map['device_name']=device_name
        else:
            map['device_name']='host-'+map['device_ip']
        map['device_type']=device_type
        data.append(map)
    myDevHandler=deviceHandler(appServer)
    for item in data:
        print item
        myDevHandler.createDevice(item['device_ip'], item['device_name'], item['device_type'])

if __name__=='__main__':
    import sys
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-r', '--random', dest='random', help='numbers of devices randomly created')
    parser.add_option('-f', '--file', dest='filename', help='full path of file that contains device info.')
    parser.add_option('-a', '--address', dest='ipaddress', help='IP address of creating device')
    parser.add_option('-n', '--name', dest='device_name', help='name of creating device')
    parser.add_option('-t', '--type', dest='device_type', help='device type of creating device.')
    options, args=parser.parse_args()
    if not sys.argv:
        print createDevice.parser_help()
        sys.exit()
    appServer=sys.argv[1]
    if options.random:
        createDevice(appServer, opt='random', num=int(options.random))
    elif options.file:
        import os
        if not os.path.exists(options.file):
            print '%s is not exist.' % options.file
        else:
            createDevice(appServer, opt='file', file=options.file)
    else:
        deviceIp=''
        if options.address:
            deviceIp=options.address
        deviceName=''
        if options.name:
            deviceName=options.name
        elif deviceIp:
            deviceName='host-'+deviceIp
        deviceType='linux'
        if options.type:
            deviceType=options.type
        createDevice(appServer, opt='cmdline', device_ip=deviceIp, device_name=deviceName, device_type=deviceType)
    print 'Done'


