# model Rules from data-definition
class Rule:
    def __init__(self):
        self.attribute={}
        self.attribute['phIncidentCategory']=None
        self.attribute['group']=None
        self.attribute['id']=None
        self.Name=None
        self.active=None
        self.Description=None
        self.GlobalConstr=None
        self.CustomerScope=CustomerScope()
        self.IncidentDef=IncidentDef()
        self.PatternClause=PatternClause()
        self.TriggerEventDisplay=TriggerEventDisplay()
        self.ClearCondition=ClearCondition()

class CustomerScope:
    def __init__(self):
        self.attribute={}
        self.attribute['groupByEachCustomer']=None
        self.Include=Include()
        self.Exclude=Exclude()

class Include:
    def __init__(self):
        self.attribute={}
        self.attribute['all']=None

class Exclude:
    def __init__(self):
        pass

class IncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['eventType']=None
        self.attribute['severity']=None
        self.ArgList=None

class PatternClause:
    def __init__(self):
        self.attribute={}
        self.attribute['window']=None
        self.GlobalConstr=None
        self.SubPattern=[]
        self.Operator=Operator()

class SubPattern:
    def __init__(self):
        self.attribute={}
        self.attribute['displayName']=None
        self.attribute['name']=None
        self.Description=None
        self.SingleEvtConstr=None
        self.GroupEvtConstr=None
        self.GroupByAttr=None

class Operator:
    def __init__(self):
        self.attribute={}
        self.attribute['rank']=None
        self.attribute['type']=None

class TriggerEventDisplay:
    def __init__(self):
        self.AttrList=None

class ClearCondition:
    def __init__(self):
        self.attribute={}
        self.attribute['method']=None
        self.attribute['type']=None
        self.ClearIncidentDef=ClearIncidentDef()
        self.ClearConstr=None
        self.PatternClause=None
        self.QuietPeriod=None

class ClearIncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['name']=None
        self.ArgList=None

#ruleAnalyst class for auto debug
class ruleAnalyst:
    def __init__(self):
        self.id=None
        self.incidentType=None
        self.name=None
        self.groupBy=None
        self.singleConstraint=None
        self.groupConstraint=None

class Reports:
    def __init__(self):
        pass

class Report:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=None
        self.attribute['id']=None
        self.Name=None
        self.CustomerScope=CustomerScope()
        self.Description=None
        self.SelectClause=SelectClause()
        self.OrderByClause=OrderByClause()
        self.ReportInterval=ReportInterval()
        self.PatternClause=PatternClause()
        self.inline=None
        self.active=None
        self.RelevantFilterAttr=None

class SelectClause:
    def __init__(self):
        self.attribute={}
        self.attribute['numEntries']=None
        self.AttrList=None

class OrderByClause:
    def __init__(self):
        self.AttrList=None

class ReportInterval:
    def __init__(self):
        self.Window=Window()

class Window:
    def __init__(self):
        self.attribute={}
        self.attribute['unit']=None
        self.attribute['val']=None

class Role:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.Name=None
        self.Description=None
        self.Config=Config()
        self.SingleEvtConstr=None

class Config:
    def __init__(self):
        self.profile=profile()

class profile:
    def __init__(self):
        self.groupNodes=[]
        self.leafNodes=None

class groupNode:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.actions=[]

class action:
    def __init__(self):
        self.attribute={}
        self.attribute['action']=None
        self.attribute['target']=None
        self.attribute['value']=None

class Config:
    def __init__(self):
        self.profile=profile()

class profile:
    def __init__(self):
        self.groupNodes=[]
        self.leafNodes=None

class groupNode:
    def __init__(self):
        self.attribute={}
        self.attribute['id']=None
        self.actions=[]

class action:
    def __init__(self):
        self.attribute={}
        self.attribute['action']=None
        self.attribute['target']=None
        self.attribute['value']=None

class eventAttrDesc:
    def __init__(self):
        self.code=None
        self.description=None

class eventAttribByDevice:
    def __init__(self):
        self.eventType=None
        self.attrNameList=None




