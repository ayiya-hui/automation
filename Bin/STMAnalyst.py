import optparse
import re
import sys
import time


"""
    usage: %prog args [options]
    -o, --object=OBJECT                          :   name of Objects (CustomerOnly, UserOnly, CustomerUser, CustomerCollector, CustomerCollectorUser)
    -n, --number=NUMBER_CUSTOMER, NUMBER_USER    :   numbers of cutomers and numbers of user in a customer, default as 1 (only 1 collector in a customer as default)
    -c, --customerName=CUSTOMER_NAME             :   name of customer, default as AutoCust, if more than one customer, then all others will have name+number format
    -u, --userName=USER_NAME                     :   name of user, default as AutoUser, if more than one user, then all others will have user_name+number format
    -t, --userType=USRE_TYPE                     :   type of user, default as Full Admin
    -l, --collectorName=COLLECTOR_NAME           :   name of collector, default as AutoCollector
    -a, --collectorIp=COLLECTOR_IPADDR           :   IP address of collector
"""


OBJECTS=['CustomerOnly', 'UserOnly', 'CustomerUser', 'CustomerCollector', 'CustomerCollectorUser']
USER_TYPE=['DB Admin', 'Executive', 'Full Admin', 'Help Desk', 'Network Admin', 'Read-Only Admin', 'Security Admin', 'Server Admin', 'Storage Admin', 'System Admin', 'Unix Server Admin', 'Windows Server Admin']

opt, args = parse(__doc__)


USAGE = re.compile(r'(?s)\s*usage: (.*?)(\n[ \t]*\n|$)')

def nonzero(self): # will become the nonzero method of optparse.Values
    # True if options were given
    for v in self.__dict__.itervalues():
        if v is not None:
            return True
    return False

optparse.Values.__nonzero__ = nonzero # dynamically fix optparse.Values

class ParsingError(Exception):
    pass

optionstring = ''

def exit(msg=''):
    raise SystemExit(msg or optionstring.replace('%prog', sys.argv[0]))

def parse(docstring, arglist=None):
    global optionstring
    optionstring = docstring
    match = USAGE.search(optionstring)
    if not match: raise ParsingError('ERROR: Can not find the option string')
    optlines = match.group(1).splitlines()
    try:
        p = optparse.OptionParser(optlines[0])
        for line in optlines[1:]:
            opt, help=line.split(':')[:2]
            short,long=opt.split(',')[:2]
            if '=' in opt:
                action = 'store'
                long = long.split('=')[0]
            else:
                action = 'store_true'
            p.add_option(short.strip(), long.strip(),
                action = action, help = help.strip())
    except (IndexError, ValueError):
        raise ParsingError('ERROR: Can not parse the option string correctly')
    return p.parse_args(arglist)
