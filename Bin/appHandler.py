import httplib2, ssl, re

DEFAULT_USER='super/admin'
DEFAULT_PASSWORD='admin*1'
PATH='/phoenix/rest'
QUERY='query/eventQuery'
EVENT='query/events'
PROGRESS='query/progress'
HEADER={'Content-Type': 'text/xml'}
LIST='list'
PAGE=1000

class appHandler:
	def __init__(self, appServer, user=False, password=False):
		self.appServer=appServer
		if user:
			self.user=user
		else:
			self.user=DEFAULT_USER
		if password:
			self.password=password
		else:
			self.password=DEFAULT_PASSWORD
		self.http=httplib2.Http()
		self.http.add_credentials(self.user, self.password)

	def setSecure(self):
		self.appServer+=':443'

	def __urljoin(self, param, arg=False):
		base='https://'+self.appServer+PATH
		if arg:
			return base+'/'+param+'/'+arg
		else:
			return base+'/'+param

	def getData(self, param, arg=False):
		if arg:
			url=self.__urljoin(param, arg=arg)
		else:
			url=self.__urljoin(param)
		resp, content=self.http.request(url, "GET")
		self.xml=content.decode("utf-8")

	def putData(self, param, inputXml):
		url=self.__urljoin(param)
		resp, content=self.http.request(url, "PUT", inputXml)

	def deleteData(self, param):
		url=self.__urljoin(parm)
		resp, content=self.http.request(url, "DELETE")

	def postData(self, param, inputXml):
		url=self.__urljoin(param)
		resp, content1=self.http.request(url, "POST", inputXml, HEADER)

	def getQuery(self, inputXml):
		self.queryXml=[]
		url1=self.__urljoin(QUERY)
		resp, content1=self.http.request(url1, "POST", inputXml, HEADER)
		queryId=content1.decode("utf-8")
		if 'error code="255"' in queryId:
			print "Query Error, check sending XML file."
			return None

		url2=self.__urljoin(PROGRESS, arg=queryId)
		if(resp['status']=="200"):
			response1, content2=self.http.request(url2)
		else:
			print("DataCollector doesn't return query. Test failed. Error code is %s" % resp['status'])
			exit()

		while (content2.decode("utf-8")!="100"):
			response1, content2=self.http.request(url2)

		content3=''
		if (content2.decode("utf-8")=="100"):
			url3=self.__urljoin(EVENT, arg=queryId+"/0/"+str(PAGE))
			response2, content3=self.http.request(url3)

		if content3!='':
			self.queryXml.append(content3.decode("utf-8"))
			p=re.compile('totalCount="\d+"')
			mlist=p.findall(content3)
			if mlist[0]!='':
				mm=mlist[0].replace('"', '')
				m=mm.split("=")[-1]
				num=0
				if int(m)>PAGE:
					num=int(m)/PAGE
				if int(m)%PAGE>0:
					num+=1
				if num>0:
					for i in range(num):
						if i:
							url3=self.__urljoin(EVENT, arg=queryId+'/'+str(i*PAGE)+'/'+str(PAGE))
							resp4, content4=self.http.request(url3)
							if content4!='':
								self.queryXml.append(content4.decode("utf-8"))



