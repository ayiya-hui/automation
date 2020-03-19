import socket

def getLocalhostIp():
    localIp=socket.gethostbyname(socket.gethostname())
    if localIp=='127.0.0.1':
        print 'System doesn\'t return a valid IP address. Need to setup correctly, or verification task cannot be run.'

    return localIp