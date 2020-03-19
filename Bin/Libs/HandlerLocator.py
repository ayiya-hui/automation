from eventParsingHandler import eventParsingHandler
from incidentHandler import incidentHandler
from logDiscoverHandler import logDiscoverHandler

token={'EventParsing':eventParsingHandler,
       'Incident':incidentHandler,
       'LogDiscover':logDiscoverHandler,
       }

def getHandlerObj(type, server, module_name=False):
    obj=None
    """This method will return a handler instance object with name specified in type."""
    if type not in token.keys():
        print 'Handler Type %s is not supported.' % type
    else:
        obj=token[type](server, mod=module_name)

    return obj

