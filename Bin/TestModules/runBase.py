import ConfigConstants.TestConstant as testConstant
import os

class baseTest:
    def __init__(self, task, testConfig):
        self.task=task
        self.testConfig=testConfig
        self.path=testConstant.test_path % task.taskName

    def getTestList(self, type):
        if type!='all':
            if ',' in type:
                tasks=type.split(',')
            else:
                tasks=[type]

        return tasks

    def getCommonData(self):
        pass

    def getGlobalData(self):
        pass




