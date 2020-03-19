import httplib2, ssl, re, cookielib
from ConfigConstants.TestConstant import restApi_user, restApi_password, restApi_path, restApi_query, restApi_event, restApi_progress, restApi_header, restApi_query_default_page
import sys

class appHandler:
	"""This method is a wrap class for HTTP client."""
	def __init__(self, appServer, user=False, password=False):
		self.appServer=appServer
		if user:
			self.user=user
		else:
			self.user=restApi_user
		if password:
			self.password=password
		else:
			self.password=restApi_password
		self.cookie_jar = cookielib.CookieJar()
		self.http=httplib2.Http(disable_ssl_certificate_validation=True)
		self.http.add_credentials(self.user, self.password)
		self.headers={'Content-Type': 'text/xml'}

	def __setSecure(self):
		self.appServer+=':443'

	def __urljoin(self, param):
		base='https://'+self.appServer+restApi_path

		return base+'/'+param

	def getData(self, param, arg=False):
		"""Http GET call."""
		if arg:
			url=self.__urljoin(param, arg=arg)
		else:
			url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "GET")
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()
		if resp['status']!='200':
			print 'request: %s' % url
			print 'return status: %s' % resp['status']
			print content
			sys.exit()
		else:
			self.xml=content.decode("utf-8")

	def putData(self, param, inputXml):
		"""Http PUT call."""
		url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "PUT", inputXml)
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()

		return content

	def deleteData(self, param):
		"""Http DELETE call."""
		url=self.__urljoin(parm)
		try:
			resp, content=self.http.request(url, "DELETE")
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()

		return content

	def postData(self, param, inputXml):
		"""Http POST call."""
		url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "POST", inputXml, restApi_header)
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()

		return content

	def getQuery(self, inputXml):
		"""This is specific for Accelops REST API to get query."""
		self.queryXml=[]
		url1=self.__urljoin(restApi_query)
		try:
			resp, content1=self.http.request(url1, "POST", inputXml, restApi_header)
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()
		queryId=content1.decode("utf-8")
		if 'error code="255"' in queryId:
			print "Query Error, check sending XML file."
			print content1
			print inputXml
			return None

		url2=self.__urljoin(restApi_progress % queryId)
		content2=''
		if(resp['status']=="200"):
			response1, content2=self.http.request(url2)
		else:
			print("DataCollector doesn't return query. Test failed. Error code is %s" % resp['status'])
			print content2
			exit()

		while (content2.decode("utf-8")!="100"):
			response1, content2=self.http.request(url2)

		content3=''
		if (content2.decode("utf-8")=="100"):
			url3=self.__urljoin(restApi_event % (queryId+"/0/"+str(restApi_query_default_page)))
			response2, content3=self.http.request(url3)

		if content3!='':
			self.queryXml.append(content3.decode("utf-8"))
			p=re.compile('totalCount="\d+"')
			mlist=p.findall(content3)
			if mlist:
				mm=mlist[0].replace('"', '')
				m=mm.split("=")[-1]
				num=0
				if int(m)>restApi_query_default_page:
					num=int(m)/restApi_query_default_page
				if int(m)%restApi_query_default_page>0:
					num+=1
				if num>0:
					for i in range(num):
						if i:
							url3=self.__urljoin(restApi_event % (queryId+'/'+str(i*restApi_query_default_page)+'/'+str(restApi_query_default_page)))
							resp4, content4=self.http.request(url3)
							if content4!='':
								self.queryXml.append(content4.decode("utf-8"))
			else:
				print 'there is issue in rest api'
				print content3



