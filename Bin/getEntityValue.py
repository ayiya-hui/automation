from Libs.restApiDataHandler import restApiDataHandler

type='PH_SYS_EVENT_NetIntfRestart'

myRest=restApiDataHandler('192.168.20.116')
data=myRest.getData(type, module='namedValue')

print 'done'