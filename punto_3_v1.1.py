import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions

# Youtube and Telecom Pakistan
# 24 February 2008, 20:07 
# TIME_INIT = "2008-02-24 20:00"
# TIME_END = "2008-02-24 23:00"

COLLECTOR = 'route-views.isc'

#---------------------------------------------------------
# Previous STREAM

TIME_INIT = "2008-02-24 20"
TIME_END = "2008-02-24 20:15"

previous_stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR))
#---------------------------------------------------------
# Current STREAM

TIME_INIT = "2008-02-24 22"
TIME_END = "2008-02-24 22:15"

current_stream = pybgpstream.BGPStream(
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

print 'Length of the previous stream ' + str(len_previous)
print 'Length of the current stream ' + str(len_current)+'\n'

#---------------------------------------------------------

idx = 0

keys = PREVIOUS_TARGET_AS_BY_PREFIX.keys()
keys.sort()
for key in keys:
	PREVIOUS_TARGET_AS_BY_PREFIX[key].sort()
	if key in CURRENT_TARGET_AS_BY_PREFIX:
		CURRENT_TARGET_AS_BY_PREFIX[key].sort()
		if PREVIOUS_TARGET_AS_BY_PREFIX[key] != CURRENT_TARGET_AS_BY_PREFIX[key]:
			print '\n	Possible hijacking prefix:'
			print '		prefix: '+key
			print '		Target ASes in RIB 1: ' + str(PREVIOUS_TARGET_AS_BY_PREFIX[key])
			print '		Target ASes in RIB 2: ' + str(CURRENT_TARGET_AS_BY_PREFIX[key])

#---------------------------------------------------------
