import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions
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

# Execution & parse of the query
ROWS = set() # Set will store a single copy of repeated tuples
for elem in stream:
 	AS_ID = str(elem.fields['as-path'].split(' ')[-1])
 	network = str(elem.fields['prefix'])
 	next_hop = str(elem.fields['next-hop'])
 	path = str(elem.fields['as-path'])
 	ROWS.add((AS_ID, network, next_hop, path))

print "Full-Routing Table - desagregada"
print "Network\t\t\tNext Hop\t\tMetric\t\tLocPrf\t\tWeight\t\tPath"
idx = 0
for elem in ROWS:
	print str(elem[1]) + "   \t" + str(elem[2]) + "\t\t" + "0\t\t" + "0\t\t" + "0\t\t" + str(elem[3])
	idx += 1
	if (idx == 20):
		break

# print len(ROWS)
#print ROWS