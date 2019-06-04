import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions

TIME_INIT = "2019-06-03 12"
TIME_END = "2019-06-03 12:10"

COLLECTOR = 'route-views.sg'

stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s" % (COLLECTOR))

#---------------------------------------------------------

len = 0

TARGET_AS_BY_PREFIX = {}
for elem in stream:
	len += 1
	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
	network = str(elem.fields['prefix'])
	if network in TARGET_AS_BY_PREFIX:
		if AS_ID not in TARGET_AS_BY_PREFIX[network]:
			print '\n - Possible hijacking prefix:'
			print '     prefix: '+network+' - Target ASes: '+TARGET_AS_BY_PREFIX[network][0]+ ', ' + AS_ID
	else:
		TARGET_AS_BY_PREFIX[network] = [AS_ID]

#---------------------------------------------------------
