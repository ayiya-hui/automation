from configModel import user, contact, RbacProfile, domain
from randomGen import getRandomNum
import xml.dom.minidom as dom
import XMLHelper
import callRest
from getRbacProfile import getRBACProfile, getDomain
import time
from getCust import getCust

USER_NAME='autoUser'

def addUser(id, type, totalUsers, postFix=False):
    userlist=[]
    if postFix:
        name=USER_NAME+postFix
    else:
        name=USER_NAME

    for i in range(totalUsers):
        myUser=user()
        myUser.name=name+type.replace(" ", "")+str(i+1)
        myUser.naturalId='autoUserId'+type.replace(" ", "")+str(i+1)
        myUser.fullName='autoUser autoTester'+type.replace(" ", "")+str(i+1)
        myUser.jobTitle='autoUser job-tester'+type.replace(" ", "")+str(i+1)
        myUser.company='auto testing company'
        myUser.description='auto tester description item'+str(i+1)
        myUser.domain='autotesting'
        myUser.dn='cn=test,cn=users,dc=autotest,dc=com'
        myUser.privileged="true"
        myUser.password='admin*1'
        myUser.active="true"
        myUser.effectiveCustId=id

        contacts=[]
        myContact=contact()
        myContact.primary="false"
        myContact.name='autoTester'+type.replace(" ", "")+str(i+1)
        myContact.address='autoTest address item'+str(i+1)
        myContact.address2='Suite Number 1000'+str(i+1)
        myContact.city='Santa Clara'
        myContact.state='CA'
        myContact.country='USA'
        myContact.description='contact item'+str(i+1)
        myContact.zip='97654'
        myContact.email=myUser.name+'@tester.com'
        myContact.homePhone=getRandomNum(500, 900)+'-'+getRandomNum(1000, 9999)
        myContact.workPhone=getRandomNum(500, 900)+'-'+getRandomNum(1000, 9999)
        myContact.mobilePhone=getRandomNum(500, 900)+'-'+getRandomNum(1000, 9999)
        myContact.smsNumber=getRandomNum(600000, 700000)
        myContact.smsProvider='att'
        contacts.append(myContact)
        myUser.contacts=contacts

        myRbac=RbacProfile()
        myRbac.name=type
        myUser.primaryProfile=myRbac

        myOrg=domain()
        myOrg.id=id
        orgs=[]
        orgs.append(myOrg)
        myUser.orgs=orgs

        mapping=[]
        mapping.append(myOrg)
        mapping.append(myRbac)
        myUser.orgRoleMappings=mapping

        userlist.append(myUser)

    myDoc=dom.Document()
    attribute=dict(custId=id)
    node=XMLHelper.pickle(userlist, myDoc, 'users')
    node.setAttribute("custId", id)

    #myObj=config(userlist)
   # node=XMLHelper.pickle(root=userlist, fabric=dom.Document(), elementName='users')
    myXml=node.toxml()
    #myId='<users custId="'+org+'">'
    myXml=myXml.replace('key', 'domain')
    myXml=myXml.replace('value', 'RbacProfile')
    print myXml

    return myXml

if __name__=='__main__':
    #import appHandler
    #import orgHandler

    #DEFAULT_ADMIN="/admin"
    #DEFAULT_PASSWORD="admin*1"
   # appServer='localhost:8181'
    #org='super'
    #myOrgHandler=orgHandler.orgHandler(appServer)
    #myOrgHandler.getOrgs()
    #orgId=myOrgHandler.getOrgIDfromName(org)
    #admin=org+DEFAULT_ADMIN
    #if admin=='super/admin':
     #   myHandler=appHandler.appHandler(appServer)
    #else:
     #   myHandler=appHandler.appHandler(appServer, user=admin)
    type='Full Admin'
    #queryString="user/import"
    totalUsers=2
    round=1
    myFix=False
    if totalUsers>500:
        round=totalUsers/500
        myFix='Round'
    for i in range(0, round):
        newFix=myFix
        if newFix:
            newFix+=str(i)
        inXml=addUser('1', type, 1, postFix=newFix)
        #myHandler.getEvent("PUT", urlString=queryString, xml=inXml)
        time.sleep(10)

    print "Done"


