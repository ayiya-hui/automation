import Libs.userHandler as userHandler

default_user_name='QAtester'

def createNewUsers(appServer, org, role, total, page=False):
    """This program is to create new users in the Accelops system.
       Usage: python createNewUsers.py <app_server_address> <org> <admin_role> <numbers_of_users> [True]
       option: True for sending users in chunk of 100 users a bunch.
               omit is for sending users all in one by using pagenating of server.
       """
    myUser=userHandler.userHandler(appServer)
    if page:
        myUser.createUsers(default_user_name+'-R'+str(i), org, role, number=total)
    else:
        if total>100:
            count=int(total/100)
        for i in range(count):
            myUser.createUsers(default_user_name+'-R'+str(i), org, role, number=100)

        remain=total-count*100
        myUser.createUsers(default_user_name+'-R'+str(count), org, role, number=remain)


if __name__=='__main__':
    import sys
    if len(sys.argv) not in [5, 6]:
        print createNewUsers.__doc__
        exit()
    appServer=sys.argv[1]
    org=sys.argv[2]
    role=sys.argv[3]
    count=int(sys.argv[4])
    no_page=False
    if len(sys.argv)==6:
        no_page=True
    createNewUsers(appServer, org, role, count, page=no_page)

    print "Done"
