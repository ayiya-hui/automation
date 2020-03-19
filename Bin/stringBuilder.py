class stringBuilder:
    def __init__(self):
        self.context=''

    def add(self, line):
        self.context+=str(line)+'\n'

    def addFront(self, line):
        self.context=line+'\n'+self.context

    def output(self):
        return self.context
