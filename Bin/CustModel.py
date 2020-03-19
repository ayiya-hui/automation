from XMLHelper import pickleToXML

class config(pickleToXML):
    def __init__(self, customers=[]):
        self.customers=customers

class customer(pickleToXML):
    def __init__(self,name,fullName,description,adminUser,adminPwd,adminEmail,includeRange,excludeRange=False):
        self.name=name
        self.fullName=fullName
        self.description=description
        self.adminUser=adminUser
        self.adminPwd=adminPwd
        self.adminEmail=adminEmail
        self.includeRange=includeRange

        if excludeRange:
            self.excludeRange=excludeRange

