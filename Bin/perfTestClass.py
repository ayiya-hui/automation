HEADER={'Content-Type': 'text/xml'}

class perfTestSuite:
    def __init__(self):
        self.testcases=[]

class perfTestCase:
    def __init__(self):
        self.url=''
        self.httpMethod='GET'
        self.header=HEADER
        self.xml=''
        self.repeat=1
        self.verify=''
        self.verify_negative=''
        self.msg=''
        self.timer_group='default_timer'
