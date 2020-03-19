import pickClass

class notificationPolicy(pickClass.pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['naturalId']=''
        self.attribute['id']=''
        self.name=''
        self.description=''
        self.displayOrder=''
        self.enabled=True
        self.conditions=[]
        self.attectedItems=''
        self.timeExpr=''
        self.severity=''
        self.targetOrgs=''
        self.exculdeTargetOrgs=''
        self.actions=[]
        self.affectedItemNames=''
        self.excludedItemNames=''

class notificationCondition(pickClass.pickleClass):
    def __init__(self):
        self.policy=''
        self.name=''
        self.type=''
        self.included=True

class notificationAction(pickClass.pickleClass):
    def __init__(self):
        self.policy=''
        self.type=''
        self.definition=''

