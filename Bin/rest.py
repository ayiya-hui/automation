import Libs.restApiDataHandler as restApiDataHandler

ip='192.168.20.30:8181'
myRest=restApiDataHandler.restApiDataHandler(ip)
data=myRest.getData('rbacProfile')

for key in data.keys():
    print data[key]

print 'done'
