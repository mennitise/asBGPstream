import pybgpstream
import pprint
import numpy as np
from netaddr import *

def isIPV4(ip):
	if (IPAddress(ip.split('/')[0]).version == 4):
		return True
	return False

def getSubmaskIndexes(ip):
	ipAddr = IPNetwork(ip)
	netmask = ipAddr.netmask.netmask_bits()
	if isIPV4(ip):
		return np.arange(netmask, 7, -1)
	return []

def getIP(ip, subnetmask):
	ipAddr = ip.split('/')[0] + '/' + str(subnetmask)
	network = str(IPNetwork(ipAddr).network)
	return network + '/' + str(subnetmask)

#---------------------------------------------------------

COLLECTOR = 'route-views.isc'

#---------------------------------------------------------
# Previous RIB stream

TIME_INIT = "2008-02-24 18"
TIME_END = "2008-02-24 18:15"

previous_stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR))

#---------------------------------------------------------
# Current RIB stream

TIME_INIT = "2008-02-24 20"
TIME_END = "2008-02-24 20:15"

current_stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR))

#---------------------------------------------------------
# Post RIB stream

TIME_INIT = "2008-02-24 22"
TIME_END = "2008-02-24 22:15"

post_stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR))

#---------------------------------------------------------

len_previous = 0

PREVIOUS_TARGET_AS_BY_PREFIX = {}
for elem in previous_stream:
	len_previous += 1
	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
	network = str(elem.fields['prefix'])
	if network in PREVIOUS_TARGET_AS_BY_PREFIX:
		if AS_ID not in PREVIOUS_TARGET_AS_BY_PREFIX[network]:
			PREVIOUS_TARGET_AS_BY_PREFIX[network].append(AS_ID)
	else:
		PREVIOUS_TARGET_AS_BY_PREFIX[network] = [AS_ID]

#---------------------------------------------------------

len_current = 0

CURRENT_TARGET_AS_BY_PREFIX = {}
for elem in current_stream:
	len_current += 1
	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
	network = str(elem.fields['prefix'])
	if network in CURRENT_TARGET_AS_BY_PREFIX:
		if AS_ID not in CURRENT_TARGET_AS_BY_PREFIX[network]:
			CURRENT_TARGET_AS_BY_PREFIX[network].append(AS_ID)
	else:
		CURRENT_TARGET_AS_BY_PREFIX[network] = [AS_ID]

#---------------------------------------------------------

len_post = 0

POST_TARGET_AS_BY_PREFIX = {}
for elem in post_stream:
	len_post += 1
	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
	network = str(elem.fields['prefix'])
	if network in POST_TARGET_AS_BY_PREFIX:
		if AS_ID not in POST_TARGET_AS_BY_PREFIX[network]:
			POST_TARGET_AS_BY_PREFIX[network].append(AS_ID)
	else:
		POST_TARGET_AS_BY_PREFIX[network] = [AS_ID]

#---------------------------------------------------------

if len_previous == 0 or len_current == 0 or len_post == 0:
	print "Some RIB is empty for the specified times\n"
	sys.exit(0)

#---------------------------------------------------------

# keys are the prefixes in the current RIB
keys = CURRENT_TARGET_AS_BY_PREFIX.keys()
keys.sort()

# Go through the prefixes of the current RIB
for key in keys:
	CURRENT_TARGET_AS_BY_PREFIX[key].sort()

	# If the prefix are in the posterior RIB
	if key in POST_TARGET_AS_BY_PREFIX:
		POST_TARGET_AS_BY_PREFIX[key].sort()

		# If the current and the post RIBs has different target AS...
		if CURRENT_TARGET_AS_BY_PREFIX[key] != POST_TARGET_AS_BY_PREFIX[key]:

			# Check too with the target AS from the previous RIB
			
			# If the previous RIB doesn't have the prefix, we verify a prefix that contains this
			if key not in PREVIOUS_TARGET_AS_BY_PREFIX:
				subnetmasks = getSubmaskIndexes(key)
				if len(subnetmasks) > 0:
					for subnet in subnetmasks:
						auxIP = getIP(key, subnet)
						if auxIP in PREVIOUS_TARGET_AS_BY_PREFIX:
							if PREVIOUS_TARGET_AS_BY_PREFIX[auxIP] == POST_TARGET_AS_BY_PREFIX[key]:
								print '\n	Possible hijacking prefix:'
								print '		prefix: '+key
								print '		prefix previous RIB: '+auxIP
								print '		Target ASes in Previous RIB: ' + str(PREVIOUS_TARGET_AS_BY_PREFIX[auxIP])
								print '		Target ASes in Current RIB: ' + str(CURRENT_TARGET_AS_BY_PREFIX[key])
								print '		Target ASes in Post RIB: ' + str(POST_TARGET_AS_BY_PREFIX[key])
								break
			else:
				if PREVIOUS_TARGET_AS_BY_PREFIX[key] == POST_TARGET_AS_BY_PREFIX[key]:
					print '\n	Possible hijacking prefix:'
					print '		prefix: '+key
					print '		Target ASes in Previous RIB: ' + str(PREVIOUS_TARGET_AS_BY_PREFIX[key])
					print '		Target ASes in Current RIB: ' + str(CURRENT_TARGET_AS_BY_PREFIX[key])
					print '		Target ASes in Post RIB: ' + str(POST_TARGET_AS_BY_PREFIX[key])
