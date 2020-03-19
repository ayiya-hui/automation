import threading, os, time, sys

dns_cmd="ec2-describe-instances | awk '{print $4}' | grep -v \"default\" | grep -v \"pending\""
run_cmd='ssh -o stricthostkeychecking=no -i "/root/ec2/id_rsa-gsg-keypair" "root@%s" "phxctl start; sleep 10; /root/ec2test/startDemo %s"'

class testThread(threading.Thread):
    vlock=threading.Lock()
    results=[]
    def __init__ (self, id, dns, demo_num):
        self.id=id
        self.demo_number=demo_num
        self.dns=dns
        threading.Thread.__init__(self)

    def getResult(self):
        return self.results

    def run (self):
        print "Running startDemoRate collector %s rate %s with Thread %s" % (self.dns, self.demo_number, self.id)
        testRet=startDemo(self.dns, self.demo_number)
        if testRet:
            self.vlock.acquire()
            self.results.append(testRet)
            self.vlock.release()

def startDemoRate(demo_number):
    """Usage: startDemoRate.py demo_number
                demo_number -- startDemo number for traffic generation
    """
    fin, fout=os.popen4(dns_cmd)
    dnsids=fout.readlines()
    id=1
    threads=[]
    for i in range(len(dnsids)):
        thread=testThread(id, dnsids[i].strip(), demo_number)
        thread.start()
        threads.append(thread)
        id+=1
    for thread in threads:
        thread.join()
    fullResult=thread.results
    print "Main Test Thread Exiting"

def startDemo(dns, demo_number):
    ret1=os.system(run_cmd % (dns, demo_number))

    return 1

if __name__=='__main__':
    if len(sys.argv)!=2:
        print startDemoRate.__doc__
        sys.exit()
    demo_number=sys.argv[1]
    startDemoRate(demo_number)

