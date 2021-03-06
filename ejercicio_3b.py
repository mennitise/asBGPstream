import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions
TIME_INIT = "2018-03-01"
TIME_END = "2018-03-01 00:05"

COLLECTOR_WIDE = 'route-views.wide'

# ISP
# ASN: 2914
# ASname: NTT-COMMUNICATIONS
ISPTargetAS = 2914

#---------------------------------------------------------

# Query configuration
stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s and path %s"%(COLLECTOR_WIDE,ISPTargetAS))

#---------------------------------------------------------

# Execution & parse of the query
index = 0
PREFIXES = []
for elem in stream:
	prefix = elem.fields['prefix']
	if str(ISPTargetAS) in str(elem.fields['as-path'].split(" ")):
		if str(prefix) not in PREFIXES:
			PREFIXES.append(prefix)
			index += 1


print 'Cantidad de prefijos: ' + str(index)
print 'Prefijos: ' + str(PREFIXES)