class simpleConstriant:
    def __init__(self):
        self.name=None
        self.desc=None
        self.operator=None
        self.value=None

class complexConstriant:
    def __init__(self):
        self.operator=None
        self.subConstriants=[]

class groupConstriant:
    def __init__(self):
        self.name=None
        self.desc=None
        self.func=None
        self.operator=None
        self.value=None

class complexGroupConstriant:
    def __init__(self):
        self.name1=None
        self.func1=None
        self.name2=None
        self.func2=None
        self.param_operator=None
        self.desc=None
        self.operator=None
        self.value=None

class accelopsConstriant:
    def __init__(self):
        self.accelops_name=None
        self.desc=None
        self.name=None
        self.func=None
        self.accelops_value=None
        self.operator=None
        self.value=None


