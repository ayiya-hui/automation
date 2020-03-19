from pickClass import pickleClass

class Report(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['group']=''
        self.attribute['id']=''
        self.Name=''
        self.CustomerScope=''
        self.Description=''
        self.SelectClause=''
        self.OrderByClause=''
        self.ReportInterval=''
        self.PatternClause=''
        self.RelevantFilterAttr=''

class CustomerScope(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['groupByEachCustomer']=''
        self.Include=''
        self.Exclude=''

class Include(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['all']=''

class Exclude(pickleClass):
    def __init__(self):
        pass

class PatternClause(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['window']=''
        self.SubPattern=[]

class SubPattern(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['displayName']=''
        self.attribute['name']=''
        self.SingleEvtConstr=''
        self.GroupEvtConstr=''
        self.GroupByAttr=''

class SelectClause(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['numEntries']=''
        self.AttrList=''

class OrderByClause(pickleClass):
    def __init__(self):
        self.AttrList=''

class ReportInterval(pickleClass):
    def __init__(self):
        self.Window=''
        self.Low=''
        self.High=''

class Window(pickleClass):
    def __init__(self):
        self.attribute={}
        self.attribute['unit']=''
        self.attribute['val']=''





