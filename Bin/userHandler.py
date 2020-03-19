from userDataClass import user, contact, RbacProfile, domain, orgRoleMapping
import xml.dom.minidom as dom
import XMLHelper
import time
from custHandler import custHandler
from appHandler import appHandler

ADD_USER='user/import'
USER_QUERY='config/user'
USER='users'
LIST='list'

class userHandler:
    def __init__(self, appServer):
        self.appServer=appServer
        self.appHandler=appHandler(appServer)
        self.myCust=custHandler(appServer)
        self.customers=self.myCust.getCustomer()

    def isUserExist(self, username):
        if not hasattr(self, 'users'):
            self.getAllUsers()
        exist=False
        for user in self.users:
            if username==user.name:
                exist=True

        return exist

    def getAllUsers(self):
        self.appHandler.getData(USER_QUERY)
        self.users=XMLHelper.unpickleXml(self.appHandler.xml, USER, objType=LIST)

    def createUsers(self, name, custName, userType, number=1):
        if self.myCust.isCustomerExist(custName):
            custId=self.myCust.getCustIdbyName(custName)
        else:
            self.myCust.createCustomer(custName)
            time.sleep(60)
            self.customers=self.myCust.getCustomer()
            custId=self.myCust.getCustomerIdbyName(custName)

        myUserList=[]
        if number==1:
            theName=name
        else:
            theName=custName+'-'+name
        for i in range(number):
           if i==0:
               myName=theName
           else:
               myName=theName+str(i)
           if not self.isUserExist(myName):
               myUser=self._createUserObj(myName, custId, userType)
               myUserList.append(myUser)
           else:
               print 'User %s already exist. Skip creating this user.' % myName
        self.uploadUser(myUserList, custName, custId)

    def _createUserObj(self, name, custId, userType):
        myUser=user()
        myUser.name=name
        myUser.naturalId=myUser.name
        myUser.fullName=myUser.name
        myUser.effectiveCustId=custId
        contacts=[]
        myContact=contact()
        myContact.name=myUser.name
        contacts.append(myContact)
        myUser.contacts=contacts
        myRbac=RbacProfile()
        myRbac.name=userType
        myUser.primaryProfile=myRbac
        myOrg=domain()
        myOrg.id=custId
        orgs=[]
        orgs.append(myOrg)
        myUser.orgs=orgs
        mapList=[]
        map=orgRoleMapping()
        map.domain=myOrg
        map.RbacProfile=myRbac
        mapList.append(map)
        myUser.orgRoleMappings=mapList

        return myUser

    def uploadUser(self, objList, custName, custId):
        if len(objList):
            inXml=self.createXml(objList, custId)
            print inXml
            myApp=appHandler(self.appServer, user=custName+'/admin')
            myApp.putData(ADD_USER, inXml)

    def createXml(self, objList, custId):
        myDoc=dom.Document()
        node=XMLHelper.pickle(root=objList, fabric=dom.Document(), elementName='users')
        node.setAttribute("custId", custId)

        return node.toxml()



if __name__=='__main__':
    myUser=userHandler('192.168.20.116')
    #myUser.createRandomUsers('O-eng', 'Full Admin', 10)
    myUser.createUsers('GooGTestUser1', 'GOOG', 'Full Admin')

    print "Done"
