import ConfigConstants.userTemplate as userTemp
import time
from appHandler import appHandler
from restApiDataHandler import restApiDataHandler
from string import Template

ADD_USER='user/import'

class userHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.restApiHandler=restApiDataHandler(self.appServer)
        self.customers=self.restApiHandler.getData('domain')

    def isUserExist(self, username):
        if not hasattr(self, 'users'):
            self.getAllUsers()
        exist=False
        for user in self.users.keys():
            if not hasattr(user, 'name'):
                continue
            if username==user.name:
                exist=True
                break

        return exist

    def isOrgExist(self, orgName):
        if orgName in self.customers.keys():
            return True
        else:
            return False

    def getAllUsers(self):
        self.users=self.restApiHandler.getData('user')

    def createUsers(self, name, orgName, userType, number=1):
        custId=''
        if self.isOrgExist(orgName):
            custId=self.customers[orgName].domainId
        else:
            print 'Customer name %s is not exist.'

        if custId:
            myUserList=[]
            if number==1:
                theName=name
            else:
                theName=orgName+'-'+name
            for i in range(number):
               if i==0:
                   myName=theName
               else:
                   myName=theName+str(i)
               if not self.isUserExist(myName):
                   myUser=Template(userTemp.user)
                   map={'name':myName, 'custId':custId, 'RbacName':userType}
                   myUserList.append(myUser.substitute(map))
               else:
                   print 'User %s already exist. Skip creating this user.' % myName
            myFinal=Template(userTemp.wrap)
            finalMap={'user':''.join(myUserList), 'custId':custId}
            inXml=myFinal.substitute(finalMap)
            myApp=appHandler(self.appServer, user=orgName+'/admin')
            myApp.putData(ADD_USER, inXml)
