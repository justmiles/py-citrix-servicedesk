import sys, json, StringIO, shutil, glob, datetime, os, pycurl

location = '/mnt/data/service_desk/'

def showQueueCount():
	#sd = ServiceDesk()
	#sd.setApiKey("d8530d29b29ed621f7a49868193db838")
	queue_file = open(location + 'queue.json')
	queue = json.load(queue_file)
	queue_file.close()

	count = len(queue['incidents'])
	print count
	
def sendToDB (type,filepath):
	api_url = "http://storage.edo.local/servicedesk/" + type + 's'
	print api_url
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, api_url)
	contents = StringIO.StringIO()
	curl.setopt(curl.POST, 1)
	curl.setopt(curl.HTTPPOST, [(type, (pycurl.FORM_FILE, filepath))])
	curl.perform()
	print contents.getvalue()
	# //return json.loads( contents.getvalue() )

def concatObjectsByType(type = 'incidents'):
	timestamp = datetime.datetime.now()
	str_timestamp = timestamp.strftime("%Y-%m-%d_%H%M")
	outfilename = location + 'datasets/backups/' + type + '_' + str_timestamp + '.json'
	
	with open(outfilename, 'wb') as outfile:
		
		# populate
		for filename in glob.glob(type + '/*.json'):
			with open(filename) as readfile:
				shutil.copyfileobj(readfile, outfile)
				outfile.write('\n')
	
		# clean
		outfile.seek(-1, os.SEEK_END)
		outfile.truncate()
		
		# close
		outfile.write(']}')
		outfile.close()
		
		# TODO: send to hadoop
		shutil.copyfile(outfilename, location + 'datasets/' + type + '.json')
		
		print 'done with ' + type
		
		
		
showQueueCount()
files = os.listdir("/mnt/data/service_desk/incidents/")
for filename in files:
	print filename
	sendToDB('incident', '/mnt/data/service_desk/incidents/' + filename)

# concatObjectsByType('incidents')
# concatObjectsByType('problems')
# concatObjectsByType('changes')
# concatObjectsByType('releases')


