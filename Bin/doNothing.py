import os, sys, time
def doNothing():
    while 1:
        time.sleep(10)
        print 'I am alive.'

if __name__=='__main__':
    # do double-fork magic
    try:
        pid=os.fork()
        if pid>0:
            sys.exit(0)    #exit first parent
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    #decouple from parent enviornment
    os.setsid()
    os.umask(0)

    #second fork
    try:
        pid=os.fork()
        if pid>0:    #exit out second parent, print out eventual PID
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)

    doNothing()






