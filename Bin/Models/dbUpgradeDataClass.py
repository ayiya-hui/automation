class table:
    def __init__(self):
        self.attribute={}
        self.attribute['Name']=''
        self.attribute['Owner']=''
        self.attribute['Primary key']=''
        self.Columns=[]
        self.Constraints=[]

class Column:
    def __init__(self):
        self.Name=''
        self.DataType=''
        self.NotNull=False
        self.Default=''
        self.primaryKey=False
        self.foreignKey=False

class primaryConstraint:
    def __init__(self):
        self.Name=''
        self.Columns=''
        self.Primary=True

class foreignConstraint:
    def __init__(self):
        self.Name=''
        self.ChildColumns=''
        self.References=''
        self.MatchType='SIMPLE'
        self.onUpdate='NO ACTION'
        self.onDelete='NO ACTION'
        self.foreignKey=False




