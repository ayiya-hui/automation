#!/usr/local/bin/python

import httplib2
import ssl
import re

def SendQuery(appServer, user, password, method, inputString=False, inputXML=False):
	top_url="https://"+appServer+"/phoenix/rest/"
	h=httplib2.Http()
	h.add_credentials(user, password)
	outXML=[]

	if method == "POST" and inputXML==False:
		print "Missing input XML for PUT and POST methods. Exit."
		exit()

	if inputString:
		input=inputString
	else:
		input="query/eventQuery"

	if method=="GET":
		url1=top_url+input
		resp, content=h.request(url1, "GET")
		outXML.append(content.decode("utf-8"))
	elif method=="PUT":
		url1=top_url+input
		resp, content=h.request(url1, "PUT", inputXML)
		outXML.append(content.decode("utf-8"))
	elif method=="POST":
		header={'Content-Type': 'text/xml'}
		url1=top_url+input
		resp, content1=h.request(url1, "POST", inputXML, header)
		queryId=content1.decode("utf-8")
		if 'error code="255"' in queryId:
			print "Query Error, check sending XML file."
			exit()

		url2=top_url+"query/progress/"+queryId

		if(resp['status']=="200"):
			response1, content2=h.request(url2)
		else:
			print("DataCollector doesn't return query. Test failed. Error code is %s" % resp['status'])
			exit()

		while (content2.decode("utf-8")!="100"):
			response1, content2=h.request(url2)

		content3=''
		if (content2.decode("utf-8")=="100"):
			url3=top_url+"query/events/"+queryId+"/0/1000"
			response2, content3=h.request(url3)

		if content3!='':
			outXML.append(content3.decode("utf-8"))
			p=re.compile('totalCount="\d+"')
			mlist=p.findall(content3)
			if mlist[0]!='':
				mm=mlist[0].replace('"', '')
				m=mm.split("=")[-1]
				num=0
				if int(m)>1000:
					num=int(m)/1000
					if int(m)%1000>0:
						num+=1
				if num>0:
					for i in range(num):
						url3=top_url+'query/events/'+queryId+'/'+str(i*1000+1)+'/1000'
						resp4, content4=h.request(url3)
						if content4!='':
							outXML.append(content4.decode("utf-8"))

	return outXML
