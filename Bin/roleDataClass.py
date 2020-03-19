class Role:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.Name=''
        self.Description=''
        self.Config=''
        self.SingleEvtConstr=''

class Config:
    def __init__(self):
        self.profile=''

class profile:
    def __init__(self):
        self.groupNodes=[]
        self.leafNodes=''

class groupNode:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=''
        self.actions=[]

class action:
    def __init__(self):
        self.attribute={}
        self.attribute['action']=''
        self.attribute['target']=''
        self.attribute['value']=''
