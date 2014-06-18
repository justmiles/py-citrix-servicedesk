import pycurl, json, base64, StringIO

class ServiceDesk:

	def __init__(self):
		self.api_key = ""

	def setApiKey(self,api_key):
		self.api_key = api_key

	def getApiKey(self):
		return self.api_key

	def viewEncodeAPI(self):
		encoded = base64.b64encode("x:" + self.api_key)
		return encoded
		
	# incident methods	
	def getIncident(self,id):
		incident = self._apiCall('get','v1/incidents/' + id + '.json')
		return incident
		
	def getIncidents(self,report_id, limit='500', page='1'):
		incidents = self._apiCall('get','v1/incidents.json','?report_id=' + report_id + '&limit=' + limit + '&page=' + page)
		return incidents
		
	# change methods
	def getChange(self,id):
		change = self._apiCall('get','v1/changes/' + id + '.json')
		return change
	
	def getChanges(self,report_id, limit='500', page='1'):
		changes = self._apiCall('get','v1/changes.json','?report_id=' + report_id + '&limit=' + limit + '&page=' + page)
		return changes
		
	# problem methods
	def getProblem(self,id):
		problem = self._apiCall('get','v1/problems/' + id + '.json')
		return problem
		
	def getProblems(self,report_id, limit='500', page='1'):
		problems = self._apiCall('get','v1/problems.json','?report_id=' + report_id + '&limit=' + limit + '&page=' + page)
		return problems

	# release methods
	def getRelease(self,id):
		release = self._apiCall('get','v1/releases/' + id + '.json')
		return release
		
	def getReleases(self,report_id, limit='500', page='1'):
		realease = self._apiCall('get','v1/releases.json','?report_id=' + report_id + '&limit=' + limit + '&page=' + page)
		return realease
		
	# Private methods	
	def _apiCall (self, method, api, url_params=''):
		api_url = "https://deskapi.gotoassist.com/" + api + url_params
		print api_url
		if method == 'get':
			curl = pycurl.Curl()
			curl.setopt(curl.HTTPHEADER, [
				'Authorization: Basic ' + base64.b64encode("x:" + self.api_key),
				'Content-Type: application/json',
			])
			curl.setopt(pycurl.URL, api_url)
			contents = StringIO.StringIO()
			curl.setopt(pycurl.WRITEFUNCTION, contents.write) 
			curl.perform()
			return json.loads( contents.getvalue() )