import ConfigParser

def getConfig(path):
    """This method is for handling config file."""
    myConf=ConfigParser.ConfigParser()
    myConf.read(path)
    data={}
    for key in myConf._sections.keys():
        options=myConf.options(key)
        data[key]=myConf.get(key)

    return data
