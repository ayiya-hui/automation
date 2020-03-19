from pickClass import pickleClass

TITLE='tester'
COMPANY='test company'
DESC='tester in test company'
DOMAIN='test domain'
DN='cn=test,cn=users,dc=testcompany,dc=com'
PWD='admin*1'
ADDR='tester address item'
ADDR2='Suite Number 1000'
CITY='Santa Clara'
STATE='CA'
COUNTRY='USA'
CONTACT_DESC='contact for user'
ZIP='95054'
EMAIL='tester@tester.com'
PHONE='408-xxx-xxxx'
SMS='666666'
SMS_PROV='att'

class user(pickleClass):
    def __init__(self):
        self.name=''
        self.naturalId=''
        self.fullName=''
        self.company=COMPANY
        self.jobTitle=TITLE
        self.domain=DOMAIN
        self.dn=DN
        self.password=PWD
        self.privileged='true'
        self.primaryProfile=''
        self.orgs=[]
        self.orgRoleMappings={}
        self.active='true'
        self.contacts=[]
        self.description=DESC
        self.effectiveCustId=''

class domain(pickleClass):
    def __int__(self):
        self.id=''

class orgRoleMapping(pickleClass):
    def __init__(self):
        self.domain=''
        self.RbacProfile=''

class contact(pickleClass):
    def __init__(self):
        self.primary='false'
        self.name=''
        self.address=ADDR
        self.address2=ADDR2
        self.city=CITY
        self.state=STATE
        self.country=COUNTRY
        self.zip=ZIP
        self.homePhone=PHONE
        self.workPhone=PHONE
        self.mobilePhone=PHONE
        self.email=EMAIL
        self.smsProvider=SMS_PROV
        self.smsNumber=SMS
        self.description=CONTACT_DESC

class RbacProfile(pickleClass):
    def __init__(self):
        self.name=''
