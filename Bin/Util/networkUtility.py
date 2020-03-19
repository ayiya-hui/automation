import sys, os

def getMacAddress():
    if sys.platform=='win32':
        for line in os.popen('ipconfig/all'):
            if line.lstrip().startswith('Physical Address'):
                mac=line.split(':')[1].strip().replace('-', ':')
                break
    else:
        for line in os.popen('/sbin/ifconfig'):
            if line.find('Ether')> -1:
                mac=line.split()[4]

    return mac

def getArpMac(ip):
    ping_cmd='ping '+ip+' -c 1'
    ping_cmd='ping '+ip+' -c 1'
    os.popen(ping_cmd)
    arp_cmd='arp '+ip
    data=os.popen(arp_cmd).readlines()
    for line in data:
        if line.startswith(ip):
            mac=line.split()[2]
            break

    return mac
