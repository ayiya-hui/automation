from custHandler import custHandler
from collectorHandler import collectorHandler
import time

class collectorSim:
    def __init__(self, appServer):
        self.custHand=custHandler(appServer)
        self.collectHand=collectorHandler(appServer)

    def createRandomCustCollector(self, number, name, myDev, collectName, myDay, myEPS):
        self.custHand.createRandomCustomers(number, name, myDev, collector=collectName, day=myDay, eps=myEPS)
        self.custHand.uploadCustomer()

    def updateCollector(self):
        self.collectHand.autoWork('update')

if __name__=='__main__':
    appServer='192.168.20.37:8181'
    custNum=20
    custName='AutotestCust'
    maxDev=500
    collectName='AutoCollector'
    Day=20
    Eps=50
    createCollector=False

    myColSim=collectorSim(appServer)
    if createCollector:
        myColSim.createRandomCustCollector(custNum, custName, maxDev, collectName, Day, Eps)

    while True:
        myColSim.updateCollector()
        time.sleep(180)

