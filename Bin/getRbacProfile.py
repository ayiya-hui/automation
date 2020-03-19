from xml.dom.minidom import parse
import configModel
import XMLHelper

PROFILE_PATH='../TestData/RBAC/'

def getUser(user):
    myUser=autoTestClass.user()


def getDomain(name):
    myDom=configModel.domain()
    if name=="Super":
        myDom.name="Super"
        myDom.domainId="1"
        myDom.custKey='AES$F2789A415FF07939E3259D29A34113C974DAA4634A7C3EE8F647C9691B609212073EF57A136BC44A8EA694D95352A134'

    return myDom

def getRBACProfile(type):
    doc=parse(PROFILE_PATH+type+'Admin.xml')
    profile=XMLHelper.unpickle(doc.childNodes[0])
    myProfile=configModel.RbacProfile()
    myProfile.name=profile.name
    myProfile.description=profile.description
    myProfile.config=profile.config
    myFilter=configModel.eventFilter()
    myFilter.singleConstraint=profile.eventFilter.singleConstraint
    myProfile.eventFilter=myFilter

    return myProfile

if __name__=='__main__':
    type='Network'
    profile=getRBACProfile(type)






