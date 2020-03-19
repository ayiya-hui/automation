import HandlerLocator
import time

class caseHandler:
    """This class to handle test cases."""
    def __init__(self, appServer, category='EventParsing', module=False):
        self.appServer=appServer
        self.category=category
        self.module=module
        self.moduleHandler=HandlerLocator.getHandlerObj(self.category, self.appServer, module_name=self.module)

    def send(self, event, name=False):
        self.moduleHandler.send(event, name=name)
        time.sleep(120)

    def query(self, event, tag):
        myCase=self.moduleHandler.get(event, tag)

        return myCase

    def queryAll(self, keyword):
        myCases=self.moduleHandler.getAll(keyword)

        return myCases

    def addNew(self, cases):
        self.moduleHandler.addNew(cases)



