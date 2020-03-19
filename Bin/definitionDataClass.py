# model Rules from data-definition
class Rule:
    def __init__(self):
        self.attribute={}
        self.attribute['phIncidentCategory']=''
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

class Report:
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
        self.inline=''
        self.active=''
        self.RelevantFilterAttr=''

class SelectClause:
    def __init__(self):
        self.attribute={}
        self.attribute['numEntries']=''
        self.AttrList=''

class OrderByClause:
    def __init__(self):
        self.AttrList=''

class ReportInterval:
    def __init__(self):
        self.Window=''

class Window:
    def __init__(self):
        self.attribute={}
        self.attribute['unit']=''
        self.attribute['val']=''
