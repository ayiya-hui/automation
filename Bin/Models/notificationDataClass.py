class notificationPolicy:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.attribute['custId']=''
        self.attribute['naturalId']=''
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

class notificationCondition:
    def __init__(self):
        self.attribute={}
        self.attribute['custId']=''
        self.policy=''
        self.name=''
        self.type=''
        self.included=True

class notificationAction:
    def __init__(self):
        self.policy=''
        self.type=''
        self.definition=''

