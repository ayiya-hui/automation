import types

def apiInfo(object, spacing=10, collapse=1):
    """Print methods and doc strings.

    Takes module, class, list, dictionary, or string."""
    methodList=__getAttr(object)
    processFunc=collapse and (lambda s: " ".join(s.split())) or (lambda s: s)
    print '\n'.join(["%s --%s" %
                     (method.ljust(spacing), processFunc(str(getattr(object, method).__doc__)))
                     for method in methodList])
    for method in methodList:
        subobj=getattr(object, method)
        if type(subobj)==types.ClassType:
            sublist=__getAttr(subobj)
            if sublist:
                print '\n'.join(["%s --%s" %
                     (sub.ljust(spacing), processFunc(str(getattr(subobj, sub).__doc__)))
                     for sub in sublist])

def __getAttr(object):
    methodList=[]
    for method in dir(object):
        subobj=getattr(object, method)
        if callable(subobj):
            docString=subobj.__doc__
            if docString:
                methodList.append(method)

    return methodList

if __name__=='__main__':
    print info.__doc__
