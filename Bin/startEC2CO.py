import threading, os, time, sys

target_file='/etc/opsd/.phoenix507332'
payload_file_base='/root/gang-ec2/co-licenses/phoenix507332.%s'
result_file='finalok.txt'
start_cmd="ec2-run-instances -k gsg-keypair --instance-type m1.large %s | awk '{print $2}' | grep \"i-*\""
dns_cmd="ec2-describe-instances %s | awk '{print $4}' | grep -v \"default\" | grep -v \"pending\""
copy_cmd='scp -o stricthostkeychecking=no -i "/root/ec2/id_rsa-gsg-keypair" "%s" "root@%s:%s"'
run_cmd='ssh -o stricthostkeychecking=no -i "/root/ec2/id_rsa-gsg-keypair" "root@%s" "ldconfig; touch /var/lock/subsys/phxctl; phxctl start; sleep 10; /root/ec2test/startDemo %s"'

class coStatus:
    def __init__(self):
        self.collector_id=None
        self.instance_id=None
        self.dns_id=None
        self.dns_status=False
        self.license_status=False
        self.run_status=False

class testThread(threading.Thread):
    vlock=threading.Lock()
    results=[]
    def __init__ (self, id, ami_id, co_id, demo_num):
        self.id=id
        self.ami_id=ami_id
        self.co_id=co_id
        self.demo_number=demo_num
        threading.Thread.__init__(self)

    def getResult(self):
        return self.results

    def run (self):
        print "Running startEC2CO collector %s with Thread %s" % (self.co_id, self.id)
        testRet=startCO(self.co_id, self.ami_id, self.demo_number)
        if testRet:
            self.vlock.acquire()
            self.results.append(testRet)
            self.vlock.release()

def startEC2CO(ami_id, co_start_id, co_number, demo_number):
    """Usage: startEC2CO.py ami_id start_co_id co_number demo_number
                ami_id -- Amazon EC2 image id
                start_co_id -- first collector id
                co_number -- numbers of collectors will start
                demo_number -- startDemo number for traffic generation
    """
    try:
        os.removedirs('/root/.ssh')
    except OSError:
        pass
    id=1
    threads=[]
    for i in range(co_number):
        thread=testThread(id, ami_id, start_co_id+i, demo_number)
        thread.start()
        threads.append(thread)
        id+=1
    for thread in threads:
        thread.join()
    fullResult=thread.results
    myFile=open(result_file, 'w')
    for item in fullResult:
        values=[]
        for at in ['collector_id', 'instance_id', 'dns_id', 'dns_status', 'license_status', 'run_status']:
            values.append(str(getattr(item, at)))
        myFile.write(','.join(values)+'\n')
    myFile.close()

    print "Main Test Thread Exiting"

def startCO(coid, amiid, demo_number):
    co_status=coStatus()
    payload_file=payload_file_base % coid
    co_status.collector_id=coid
    fin, fout=os.popen4(start_cmd % amiid)
    iid=fout.readline().strip()
    print iid
    co_status.instance_id=iid
    for i in range(100):
        fin, fout=os.popen4(dns_cmd % iid)
        dnsid=fout.readline().strip()
        print 'Pending %s' % i
        if dnsid:
            print dnsid
            co_status.dns_id=dnsid
            co_status.dns_status=True
            break
        i+=1
        time.sleep(10)
    if not co_status.dns_status:
        print 'Failed maximum attempts to get DNS Hostname'
        sys.exit()
    time.sleep(10)
    for i in range(50):
        print i
        ret=os.system(copy_cmd % (payload_file, co_status.dns_id, target_file))
        if ret==0:
            co_status.license_status=True
            break
        i+=1
        time.sleep(5)
    if not co_status.license_status:
        print 'Failed maximum attempts to drop license file'
        sys.exit()
    for i in range(10):
        print i
        ret1=os.system(run_cmd % (co_status.dns_id, demo_number))
        if ret1==0:
            co_status.run_status=True
            break
        i+=1
        time.sleep(5)
    if not co_status.run_status:
        print 'Failed maximum attempts to start Event Sending'
        sys.exit()

    return co_status

if __name__=='__main__':
    if len(sys.argv)!=5:
        print startEC2CO.__doc__
        sys.exit()

    ami_id=sys.argv[1]
    start_co_id=int(sys.argv[2])
    co_number=int(sys.argv[3])
    demo_number=sys.argv[4]
    startEC2CO(ami_id, start_co_id, co_number, demo_number)

