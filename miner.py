import sys, json, StringIO, pycurl, os
from ServiceDesk import ServiceDesk

sd = ServiceDesk()
sd.setApiKey("7ca75d929b67d59a99ffed3102f9ae13")
location = '/mnt/data/service_desk/'

def enqueue(report_inc = '862260361677721612', pagenum='1'):
	queue_file = open(location + 'queue.json')
	enqueue = json.load(queue_file)
	queue_file.close()

	# Enqueue Incidents
	incidents = sd.getIncidents(report_inc, page=pagenum)
	for i in incidents['result']['incidents']:
		print str(i['id'])
		# check that it's not already in the queue
		if i['id'] not in enqueue['incidents']:
			enqueue['incidents'].append(i['id'])
		
	# Enqueue Changes
	changes = sd.getChanges('864375787683186150')
	for i in changes['result']['changes']:
		print str(i['id'])
		# check that it's not already in the queue
		if i['id'] not in enqueue['changes']:
			enqueue['changes'].append(i['id'])
					
	# Enqueue Problems
	problems = sd.getProblems('864417728031308169')
	for i in problems['result']['problems']:
		print str(i['id'])
		# check that it's not already in the queue
		if i['id'] not in enqueue['problems']:
			enqueue['problems'].append(i['id'])
					
	# Enqueue Releases
	releases = sd.getReleases('864417977129337618')
	for i in releases['result']['releases']:
		print str(i['id'])
		# check that it's not already in the queue
		if i['id'] not in enqueue['releases']:
			enqueue['releases'].append(i['id'])
			
	# write the updated queue.json file
	queue_file = open(location + 'queue.json', 'w')
	
	queue_file.write(json.dumps(enqueue, indent=4, sort_keys=True))
	queue_file.close()
	print 'done'

def mine():
	# TODO: iterate through the queue.json file and
	queue_file = open(location + 'queue.json')
	queue = json.load(queue_file)
	queue_file.close()

	# mine from queue
	queue = processQueue(queue,'incident')
	queue = processQueue(queue,'change')
	queue = processQueue(queue,'problem')
	queue = processQueue(queue,'release')
		
	# write the updated queue.json file
	queue_file = open(location + 'queue.json', 'w')
	json.dump(queue, queue_file)
	queue_file.close()
	print 'done'

def processQueue(queue,type):
	count = len(queue[type + 's'])
	# limit the number of tries per loop
	limit = 200
	if (count > limit): count = limit;
	while (count > 0):
	
		success = False
		try:
			if (type == 'incident'):
				sd_object = sd.getIncident(str(queue[type + 's'][0]))
			elif (type == 'change'):
				sd_object = sd.getChange(str(queue[type + 's'][0]))
			elif (type == 'problem'):
				sd_object = sd.getProblem(str(queue[type + 's'][0]))
			elif (type == 'release'):
				sd_object = sd.getRelease(str(queue[type + 's'][0]))
			fullpath = 	location + type + 's/' + str(queue[type + 's'][0]) + '.json'
			
			if(sd_object['status'] == 'Success'):
				with open(fullpath, 'w') as new_file:
					json.dump(sd_object['result'][type], new_file)
				sendToDB(type,fullpath)
				success = True
			elif(sd_object['errors'][0]['error'] == '[E400] no ' + type + ' found'):
				success = True
				try:
					os.remove(fullpath)
				except OSError:
					pass
			if (success): del queue[type + 's'][0];
			count -= 1
		except IOError as e:
			print e
		except NameError as e:
			print e
		except ValueError as e:
			print e
		except KeyError as e:
			print sd_object
		except:
			print "Unexpected error:", sys.exc_info()[0]

	return queue
	
def sendToDB (type,filepath):
	api_url = "http://storage.edo.local/servicedesk/" + type + 's'
	curl = pycurl.Curl()
	curl.setopt(pycurl.URL, api_url)
	contents = StringIO.StringIO()
	curl.setopt(curl.POST, 1)
	curl.setopt(curl.HTTPPOST, [(type, (pycurl.FORM_FILE, filepath))])
	curl.perform()

	
# TODO: add method to initialize a queue.json file if it's not there
# {"incidents":[],"problems":[],"releases":[],"changes":[]}

# Exit if arguments are not valid actions
if len(sys.argv) < 2:
    sys.exit('Usage: %s action (enqueue or mine)' % sys.argv[0])

# Call methods based on action
if sys.argv[1] == 'enqueue':
	enqueue()
elif sys.argv[1] == 'mine':
	mine()
elif float(sys.argv[1]):
	enqueue(report_inc = str(sys.argv[1]),pagenum = str(sys.argv[2]))
  
# Examples of class ServiceDesk

# incident = sd.getIncident('1024')
# print str( incident['result']['incident']['title'] )

# incidents = sd.getIncidents(sys.argv[1])
# print str( incidents['result'] ['incidents'][0]['title']  )

# change = sd.getChange(sys.argv[1])
# print str( incident['result']['change']['title'] )

# problem = sd.getProblem(sys.argv[1])
# print str( incident['result']['problem']['title'] )

# release = sd.getRelease(sys.argv[1])
# print str( incident['result']['release']['title'] )

