import httplib2
from urllib import urlencode
import ssl
import time, os
import re
import logging

DEFAULT_URL="http://sj-dev-s-rh-vmw-01/bugzilla-3.0.4/"

def AddBugInfo(caseName, failedParam, username, password):
    #get back the bug ID if exist
    bugId=bugQuery(caseName, username, password)
    if (bugId==""):
        #if bug ID is not exist, fill new bug and get the ID
        bugId=bugFiling(caseName, failedParam, username, password)
    return bugId

def bugQuery(caseName, username, password):
    url=DEFAULT_URL+"buglist.cgi?query_format=advanced&short_desc_type=substring&short_desc=AutomateCase-"+caseName
    h=httplib2.Http()
    h.add_credentials(username, password)
    body=""
    m=[]
    resp, content=h.request(url, 'GET', body)
    if(resp['status']=="200"):
        p=re.compile('id=\d+')
        m=p.findall(content)
    bugId=""
    if(len(m)>0):
        if(len(m)==1):
            bugId=m[0].split("=")[1]
            logging.debug("Exist bug ID: %s", bugId)
        else:
            logging.debug("Multiple bugs: %s found", m)
            for item in m:
                bugNum=item.split("=")[1]
                bugId=bugId+" "+bugNum
                logging.debug("Exist bug ID: %s", bugId)
    return bugId

def bugFiling(caseName, failedParam, username, password):
    url=DEFAULT_URL+"post_bug.cgi"
    h=httplib2.Http()
    h.add_credentials(username, password)
    summary="AutomateCase-"+caseName
    comment=""
    for item in failedParam:
        comment+="Failed Attribute Name: "+item['param']+" Expected Value: "+item['Expect Value']+" Actual Returned Value: "+item['Actual Value']

    data={}
    data['Bugzilla_login']="sha.zhou@accelops.net"
    data['Bugzilla_password']="310FZr4f"
    data['product']="Phoenix"
    data['rep_platform']="All"
    data['op_sys']="All"
    data['bug_Severity']="major"
    data['priority']="P3"
    data['bug_status']="NEW"
    data['short_desc']=summary
    data['version']="unspecified"
    data['component']="Parser"
    data['comment']= comment
    resp, content=h.request(url, 'POST', urlencode(data))
    output=open("myResult.html","w")
    output.write(content)
    output.close()

    time.sleep(30)
    bugId=bugQuery(caseName)
    logging.debug("New bug ID: %s", bugId)
    return bugId

