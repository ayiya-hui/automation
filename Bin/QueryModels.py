from XMLHelper import pickleToXML

class Reports(pickleToXML):
    def __init__(self, reportList):
        self.Report=reportList

class Report(pickleToXML):
    def __init__(self, id, group, name, custScope, desc, select, interval, pattern, filter, order=False):
        self.__attributes__=dict(id=id, group=group)
        self.Name=name
        self.CustomerScope=custScope
        self.Description=desc
        self.SelectClause=select
        self.ReportInterval=interval
        self.PatternClause=pattern
        self.ReleventFilterAttr=filter
        if order:
            self.OrderByClause=order

class CustomerScope(pickleToXML):
    def __init__(self, include, exclude):
        self.__attributes__=dict(groupByEachCustomer="true")
        self.Include=include
        self.Exclude=exclude

class Include(pickleToXML):
    def __init__(self):
        self.__attributes__=dict(all="true")

class Exclude(pickleToXML):
    def __init__(self):
        self.__attribute__=dict()

class SelectClause(pickleToXML):
    def __init__(self, attrilist):
        self.__attributes__=dict(numEntries="All")
        self.AttrList=attrilist

class OrderByClause(pickleToXML):
    def __init__(self, attriList):
        self.AttrList=attriList

class ReportInterval(pickleToXML):
    def __init__(self, window):
        self.Window=window

class Window(pickleToXML):
    def __init__(self):
        self.__attributes__=dict(unit="Hourly", val="1")

class PatternClause(pickleToXML):
    def __init__(self, subPattern):
        self.__attributes__=dict(window="3600")
        self.SubPattern=subPattern

class SubPattern(pickleToXML):
    def __init__(self, display, name, singleConstr, groupBy=False):
        self.__attributes__=dict(displayName=display, name=name)
        self.SingleEvtConstr=singleConstr
        if groupBy:
            self.GroupByAttr=groupBy

