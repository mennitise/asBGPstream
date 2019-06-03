import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions

# Youtube and Telecom Pakistan
# 24 February 2008, 20:07 
# TIME_INIT = "2008-02-24 20:00"
# TIME_END = "2008-02-24 23:00"
# COLLECTOR_WIDE = 'route-views.isc'

TIME_INIT = "2015-01-14"
TIME_END = "2015-01-14 00:05"

COLLECTOR_WIDE = 'route-views.wide'

#---------------------------------------------------------

# Query configuration
stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR_WIDE))

#---------------------------------------------------------

TARGET_AS_BY_PREFIX = {}
for elem in stream:
	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
	network = str(elem.fields['prefix'])
	if network in TARGET_AS_BY_PREFIX:
		# if network == '208.65.153.0/24':
		#	print network + ' - ' + AS_ID + ' - ' + str(TARGET_AS_BY_PREFIX[network])
		if AS_ID not in TARGET_AS_BY_PREFIX[network]:
			print "SECUESTRO - " + network + ' - ' + AS_ID + ' - ' + str(TARGET_AS_BY_PREFIX[network])
		TARGET_AS_BY_PREFIX[network].append(AS_ID)
	else:
		TARGET_AS_BY_PREFIX[network] = [AS_ID]

idx = 0
for elem in TARGET_AS_BY_PREFIX.keys():
	print str(idx) + ' - \t' + str(elem) + '\t' + str(TARGET_AS_BY_PREFIX[elem])
	idx += 1
	if (idx == 20):
		break

# For Youtube case:
# print TARGET_AS_BY_PREFIX['208.65.153.0/24']