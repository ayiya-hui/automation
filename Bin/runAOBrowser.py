#! /usr/bin/python

import getCmdsSelenium
from AOBrowser import AOBrowser

def runAOBrowser(filename, outXml, debug_flag, timeout_flag):
    """Usage: runAOBrowser.py <html_file> <output_file> [-o]
    html_file - it is the html file crearted by Selenium recorder.
    output_file - xml file created by test.
    -o -- option to turn on debug
    -t -- timeout to add timeout (seconds) for each step."""
    status, err_msg, cmd_list=getCmdsSelenium.getCmdsSelenium(filename)
    if status:
        browser=AOBrowser(debug=debug_flag, timeout=timeout_flag)
        result=browser.replay(cmd_list, outXml)
        browser.exit()
    else:
        myW=open(outXml, 'w')
        myW.write(err_msg)
        myW.close()

if __name__ == "__main__":
    import getpass
    import sys
    if getpass.getuser() not in ['admin', 'sha']:
        print 'Current user is %s. Only admin can run this program.' % getpass.getuser()
        sys.exit()
    from optparse import OptionParser
    parser=OptionParser()
    parser.add_option('-t', '--timeout', dest='timeout', help='timeout for each step')
    parser.add_option('-d', '--debug', dest='debug', help='enable debug mode')
    options, args=parser.parse_args()
    if len(args)!=2:
        print runAOBrowser.__doc__
        sys.exit()
    filename=args[0]
    outXml=args[1]
    debug_flag=False
    if options.debug:
        debug_flag=True
    timeout_flag=''
    if options.timeout:
        timeout_flag=int(options.timeout)
    runAOBrowser(filename, outXml, debug_flag, timeout_flag)
    print '\ntask is done'

