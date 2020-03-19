import httplib2, ssl, re, cookielib
from ConfigConstants.TestConstant import restApi_user, restApi_password, restApi_path, restApi_query, restApi_event, restApi_progress, restApi_query_default_page
import sys, os, gzip, StringIO

class appHandler:
	"""This method is a wrap class for HTTP client."""
	def __init__(self, appServer, user=False, password=False, debug=False):
		self.appServer=appServer
		if user:
			self.user=user
		else:
			self.user=restApi_user
		if password:
			self.password=password
		else:
			self.password=restApi_password
		if debug:
			self.debug=True
		else:
			self.debug=False
		self.cookie_jar = cookielib.CookieJar()
		if os.name=='posix':
			self.http=httplib2.Http(disable_ssl_certificate_validation=True)
		else:
			self.http=httplib2.Http()
		self.http.add_credentials(self.user, self.password)
		self.headers={'Content-Type': 'text/xml', 'Accept-encoding':'gzip,deflate'}
		self.queryDebug=[]
		self.queryResult=False
		self.xml=''

	def __setSecure(self):
		self.appServer+=':443'

	def __urljoin(self, param):
		base='https://'+self.appServer+restApi_path

		return base+'/'+param

	def __unzipIfZip(self, res, text_string):
		final_content=''
		"""if '-content-encoding' in res.keys() and res['-content-encoding']=='gzip':
		    f=gzip.GzipFile(fileobj=StringIO.StringIO(text_string))
		    final_content=f.read()
	 	else:
		    final_content=text_string"""
                final_content=text_string

		return final_content.decode("utf-8")

	def getData(self, param, arg=False):
		"""Http GET call."""
		if arg:
			url=self.__urljoin(param, arg=arg)
		else:
			url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "GET", headers=self.headers)
			if 'Cookie' not in self.headers.keys() and 'set-cookie' in resp.keys():
				self.headers['Cookie']=resp['set-cookie']
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()
		if resp['status']!='200':
			print 'request: %s' % url
			print 'return status: %s' % resp['status']
			print content
		else:
			self.xml=self.__unzipIfZip(resp, content)

	def putData(self, param, inputXml):
		"""Http PUT call."""
		url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "PUT", inputXml, headers=self.headers)
			if 'Cookie' not in self.headers.keys():
				self.headers['Cookie']=resp['set-cookie']
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			print 'test URL: %s' % url
			sys.exit()

		return content

	def deleteData(self, param):
		"""Http DELETE call."""
		url=self.__urljoin(parm)
		try:
			resp, content=self.http.request(url, "DELETE", headers=self.headers)
			if 'Cookie' not in self.headers.keys():
				self.headers['Cookie']=resp['set-cookie']
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()

		return content

	def postData(self, param, inputXml):
		"""Http POST call."""
		url=self.__urljoin(param)
		try:
			resp, content=self.http.request(url, "POST", inputXml, headers=self.headers)
			if 'Cookie' not in self.headers.keys():
				self.headers['Cookie']=resp['set-cookie']
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()

		return content

	def getQuery(self, inputXml):
		"""This is specific for Accelops REST API to get query."""
		self.queryXml=[]
		queryResult=[]
		url1=self.__urljoin(restApi_query)
		if self.debug:
			print 'query URL: %s' % url1
		try:
			resp, content1=self.http.request(url1, "POST", inputXml, headers=self.headers)
			if self.debug:
				print 'response: %s' % resp
				print 'content: %s' % content1
			if 'Cookie' not in self.headers.keys() and 'set-cookie' in resp.keys():
				self.headers['Cookie']=resp['set-cookie']
		except AttributeError as e:
			print 'Cannot make socket connection: %s' % e
			sys.exit()
		queryId=self.__unzipIfZip(resp, content1)
		if 'error code="255"' in queryId:
			print "Query Error, check sending XML file."
			print content1
			print inputXml
			return None
		else:
			queryResult.append('queryId success')

		url2=self.__urljoin(restApi_progress % queryId)
		if self.debug:
			print 'Progress URL: %s' % url2
		content2=''
		if(resp['status']=="200"):
			response1, content2_raw=self.http.request(url2)
		else:
			print("DataCollector doesn't return query. Test failed. Error code is %s" % resp['status'])
			print content2
			exit()
		content2=self.__unzipIfZip(response1, content2_raw)
		while (content2!="100"):
			response1, content2_raw=self.http.request(url2, "GET", headers=self.headers)
			content2=self.__unzipIfZip(response1, content2_raw)
		if self.debug:
			print 'progress response: %s' % response1
			print 'progress content: %s' % content2
		content3=''
		if (content2=="100"):
			queryResult.append('query progress success')
			url3=self.__urljoin(restApi_event % (queryId+"/0/"+str(restApi_query_default_page)))
			response2, content3_raw=self.http.request(url3, "GET", headers=self.headers)
			content3=self.__unzipIfZip(response2, content3_raw)
			if self.debug:
				print 'getQuery response: %s' % response2
				print 'getQuery content: %s' % content3

		if content3!='':
			self.queryXml.append(content3)
			p=re.compile('totalCount="\d+"')
			mlist=p.findall(content3)
			if mlist:
				mm=mlist[0].replace('"', '')
				m=mm.split("=")[-1]
				num=0
				if int(m):
					self.queryResult=True
					if int(m)>restApi_query_default_page:
						num=int(m)/restApi_query_default_page
					if int(m)%restApi_query_default_page>0:
						num+=1
					if num>0:
						for i in range(num):
							if i:
								url3=self.__urljoin(restApi_event % (queryId+'/'+str(i*restApi_query_default_page)+'/'+str(restApi_query_default_page)))
								resp4, content4_raw=self.http.request(url3, "GET", headers=self.headers)
								content4=self.__unzipIfZip(resp4, content4_raw)
								if content4!='':
									self.queryXml.append(content4)
					queryResult.append('query success with data')
				else:
					queryResult.append('query success but no data')
			else:
				print 'there is issue in rest api'
				print content3

			if queryResult:
				my_str=';'.join(queryResult)
				if my_str not in self.queryDebug:
					self.queryDebug.append(my_str)




