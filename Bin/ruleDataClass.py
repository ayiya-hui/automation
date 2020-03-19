# model Rules from data-definition
class Rules:
    def __init__(self):
        self.rules=[]

class Rule:
    def __init__(self):
        self.attribute={}
        self.attribute['group']=''
        self.attribute['id']=''
        self.Name=''
        self.active=''
        self.Description=''
        self.CustomerScope=''
        self.IncidentDef=''
        self.PatternClause=''
        self.TriggerEventDisplay=''
        self.ClearCondition=''

class CustomerScope:
    def __init__(self):
        self.attribute={}
        self.attribute['groupByEachCustomer']=''
        self.Include=''
        self.Exclude=''

class Include:
    def __init__(self):
        self.attribute={}
        self.attribute['all']=''

class IncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['eventType']=''
        self.attribute['severity']=''
        self.ArgList=''

class PatternClause:
    def __init__(self):
        self.attribute={}
        self.attribute['window']=''
        self.SubPattern=[]
        self.Operator=''
        self.GlobalConstr=''


class SubPattern:
    def __init__(self):
        self.attribute={}
        self.attribute['displayName']=''
        self.attribute['name']=''
        self.SingleEvtConstr=''
        self.GroupEvtConstr=''
        self.GroupByAttr=''

class Operator:
    def __init__(self):
        self.attribute={}
        self.attribute['rank']=''
        self.attribute['type']=''

class TriggerEventDisplay:
    def __init__(self):
        self.AttrList=''

class ClearCondition:
    def __init__(self):
        self.attribute={}
        self.attribute['method']=''
        self.attribute['type']=''
        self.ClearIncidentDef=''
        self.ClearConstr=''
        self.PatternClause=''
        self.QuietPeriod=''

class ClearIncidentDef:
    def __init__(self):
        self.attribute={}
        self.attribute['name']=''
        self.ArgList=''

#ruleAnalyst class for auto debug
class ruleAnalyst:
    def __init__(self):
        self.id=''
        self.incidentType=''
        self.name=''
        self.groupBy=''
        self.singleConstraint=''
        self.groupConstraint=''

