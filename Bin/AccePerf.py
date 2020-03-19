import AccePerfSettings
import sys, optparse

VERSION='1.0'

parser=optparse.OptionParser()
parser.add_option("-a", "--agents", dest="agents", metavar="NUM_AGENTS", help="number of agents")
parser.add_option("-u", "--user", dest="user", metavar="USERNAME", help="user name")
parser.add_option("-w", "--password", dest="password", metavar="PASSWORD", help="user password")
parser.add_option("-d", "--duration", dest="duration", metavar="DURATION", help="test duration in seconds")
parser.add_option("-r", "--rampup", dest="rampup", metavar="RAMPUP", help="rampup in seconds")
parser.add_option("-i", "--interval", dest="interval", metavar="INTERVAL", help="interval in milliseconds")
parser.add_option("-f", "--filename", dest="filename", metavar="FILENAME", help="test file name")
parser.add_option("-o", "--output_dir", dest="outdir", metavar="PATH", help="output directory")
parser.add_option("-n", "--name", dest="name", metavar="TESTNAME", help="name of test")
parser.add_option("-l", "--log_msg", dest="logmsg", help="log messages")
parser.add_option("-b", "--blocking", dest="block", help="blocking mode")
parser.add_option("-g", "--gui", dest="gui", help="start GUI")
parser.add_option("-p", "--port", dest="port", metavar="PORT", help="xml-rpc listening port")
(opts, args)=parser.parse_args()

myConfig=AccePerfSettings.config()
if not opts and not args:
    print 'version: %s' % VERSION
try:
    if opts.agents:
        myConfig.agents=int(opts.agents)
    if opts.user:
        myConfig.user=opts.users
    if opts.password:
        myConfig.password=opts.password
    if opts.duration:
        myConfig.duration=int(opts.duration)
    if opts.rampup:
        myConfig.rampup=int(opts.rampup)
    if opts.interval:
        myConfig.interval=int(opts.interval)
    if opts.filename:
        myConfig.filename=opts.filename
    if opts.outdir:
        myConfig.outdir=opts.outdir
    if opts.name:
        myConfig.name=opts.name
    if opts.logmsg:
        myConfig.logmsg=opts.logmsg
    if opts.block:
        myblock=opts.block
    if opts.gui:
        if opts.gui.lower()=='true':
            myGui=True
        else:
            myGui=False
    if opts.port:
        myPort=int(opts.port)
except Exception, e:
    print 'Invalid Argument'
    sys.exit(1)

if myGui:
    import AccePerfGui
    AccePerfGui.main(myConfig, VERSION)
