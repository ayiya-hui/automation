import Libs.upgradeTestHandler as upgradeTestHandler

def testUpgrade(server, option, user=False, password=False, mod=False):
    myUpgrade=upgradeTestHandler.upgradeTestHandler(server, my_user=user, my_password=password, modules=mod)
    if option=='pre':
        myUpgrade.preTest()
    elif option=='post':
        myUpgrade.postTest()

if __name__=='__main__':
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-m', '--modules', dest='modules', help='Modules', metavar='MODULES')
    parser.add_option('-o', '--option', dest='opt', help='Option', metavar='OPT')
    parser.add_option('-u', '--user', dest='user', help='User Name', metavar='USER')
    parser.add_option('-p', '--password', dest='password', help='Password', metavar='PASSWORD')
    options, args=parser.parse_args()
    server=args[0]
    option=False
    if options.opt:
        option=options.opt
    my_modules=False
    if options.modules:
        my_modules=options.modules
    my_user=False
    if options.user:
        my_user=options.user
    my_pass=False
    if options.password:
        my_pass=options.password
    testUpgrade(server, option, user=my_user, password=my_pass, mod=my_modules)

    print 'task done.'
