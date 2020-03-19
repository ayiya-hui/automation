from Libs.parserHandler import parserHandler

def checkEventParseCoverage(server):
    myParser=parserHandler(server)
    myParser.checkNewParsers()

if __name__=="__main__":
    server='192.168.20.116'
    checkEventParseCoverage(server)
    print '\nTask is done.'
