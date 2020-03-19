from Libs.restApiDataHandler import restApiDataHandler
from Util.timeUtility import convertTime

def getSystemVersion(server, my_user=False, my_password=False):
    systemInfo=restApiDataHandler(server, user=my_user, password=my_password).getData('health', module='cloudStatus')
    buildVersion=systemInfo.version+' (build on '+convertTime(int(systemInfo.buildDate))+')'

    return buildVersion
