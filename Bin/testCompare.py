import Libs.compareTestHandler as compareTestHandler

def testCompare(servers, user1=False, password1=False, user2=False, password2=False, mod=False):
    myCompare=compareTestHandler.compareTestHandler(servers[0], servers[1], my_user1=user1, my_password1=password1, my_user2=user2, my_password2=password2, modules=mod)
    myCompare.test()

if __name__=='__main__':
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-m', '--modules', dest='modules', help='Modules', metavar='MODULES')
    parser.add_option('-u', '--user1', dest='user1', help='User1 Name', metavar='USER1')
    parser.add_option('-p', '--password1', dest='password1', help='Password1', metavar='PASSWORD1')
    parser.add_option('-v', '--user2', dest='user2', help='User2 Name', metavar='USER2')
    parser.add_option('-w', '--password2', dest='password2', help='Password2', metavar='PASSWORD2')
    options, args=parser.parse_args()
    servers=args[0].split(',')
    my_modules=False
    if options.modules:
        my_modules=options.modules
    my_user1=False
    if options.user1:
        my_user1=options.user1
    my_pass1=False
    if options.password1:
        my_pass1=options.password1
    my_user2=False
    if options.user2:
        my_user2=options.user
    my_pass2=False
    if options.password2:
        my_pass2=options.password2
    testCompare(servers, user1=my_user1, password1=my_pass1, user2=my_user2, password2=my_pass2, mod=my_modules)

    print 'task done.'
