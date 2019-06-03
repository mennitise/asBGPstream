import pybgpstream
import pprint
import numpy as np
import csv

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



with open('full_RIB_desagregada.csv', mode='w') as rib_desagregada:
    rib_writer = csv.writer(rib_desagregada)
    rib_writer.writerow(['Network', 'Next Hop', 'Metric', 'LocPrf', 'Weight', 'Path'])
	
    for elem in ROWS:
		network = str(elem[1])
		next_hop = str(elem[2])
		path = str(elem[3])
		rib_writer.writerow([network, next_hop, '0', '0', '0', path])
	
    rib_desagregada.close()

print ('Full RIB desagregada, de tamano ' + str(len(ROWS)) + ' correctamente guardada en full_RIB_desagregada.csv')
