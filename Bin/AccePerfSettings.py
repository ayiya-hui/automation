#config
AGENTS=1
USER='super/admin'
PASSWORD='admin*1'
DURATION=60 #sec
RAMPUP=0 #sec
INTERVAL=0 #millisec
TEST_FILENAME='testcases.xml'
OUTPUT_DIR=None
TEST_NAME=None
LOG_MSG=False

#default
GENERATE_RESULTS=True
SHUFFLE_TESTCASES=False
WAITFOR_AGENT_FINISH=True
SMOOTH_TP_GRAPH=3 #sec
SOCKET_TIMEOUT=300 #sec
COOKIES_ENABLED=True
HTTP_DEBUG=False
BLOCKING=False
GUI=False
PORT=9999

class config:
    def __init__(self):
        self.agents=AGENTS
        self.user=USER
        self.password=PASSWORD
        self.duration=DURATION
        self.rampup=RAMPUP
        self.interval=INTERVAL
        self.filename=TEST_FILENAME
        self.outdir=OUTPUT_DIR
        self.name=TEST_NAME
        self.logmsg=LOG_MSG



