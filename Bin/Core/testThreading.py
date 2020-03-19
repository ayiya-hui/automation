import threading

class testThread(threading.Thread):
    """This class is the thread class for automation test."""
    def __init__ (self, queue, return_queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.return_queue=return_queue

    def run (self):
        """This method starts the testing."""
        while True:
            testData=self.queue.get()
            testName=testData['name']
            testKey=testData['key']
            task=testData['task']
            print "Running Test %s Task %s with %s" % (testName, testKey, self.name)
            self.testObj=testData['obj']
            testRet=self.testObj.run(task, testKey)
            if testRet!=None:
                self.return_queue.put(testRet)
                self.queue.task_done()
                print "%s (%s) successd." % (testKey, self.name)
