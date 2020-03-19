import time

def getRemoteTimeZone():
    #find out your location
    localZone=time.altzone/3600
    if localZone>0:
        #System is in CA
        value=-8
    else:
        #System is in Shanghai
        value=7



if __name__=='__main__':
    getRemoteTimeZone()
