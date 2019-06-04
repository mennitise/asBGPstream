import pybgpstream
import pprint
import numpy as np
import csv
from netaddr import *

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

#---------------------------------------------------------
# Non Agregated Full RIB

with open('full_RIB_Desagregada.csv', mode='w') as rib_desagregada:
    rib_writer = csv.writer(rib_desagregada)
    rib_writer.writerow(['Network', 'Next Hop', 'Metric', 'LocPrf', 'Weight', 'Path'])
	
    for elem in ROWS:
		network = str(elem[1])
		next_hop = str(elem[2])
		path = str(elem[3])
		rib_writer.writerow([network, next_hop, '0', '0', '0', path])
	
    rib_desagregada.close()

print ('Full RIB Desagregada, de tamano ' + str(len(ROWS)) + ' correctamente guardada en full_RIB_Desagregada.csv')


#---------------------------------------------------------
# Maximum Agregated Full RIB

ROWS_GROUPED = {}
for elem in ROWS:
    AS_ID = str(elem[0])
    network = IPNetwork(str(elem[1]))
    next_hop = str(elem[2])
    as_path = str(elem[3])

    uniqueKey = AS_ID + '_' + next_hop + '_' + as_path

    if uniqueKey in ROWS_GROUPED:
        ROWS_GROUPED[uniqueKey].append(network)
    else:
        ROWS_GROUPED[uniqueKey] = [network]


FINAL_SET = []
for elem in ROWS_GROUPED:
    FINAL_SET.append((elem, cidr_merge(ROWS_GROUPED[elem])))


AGREGATED_TABLE = set()
for row in FINAL_SET:
    ASId = str(row[0].split("_")[0])
    next_hop = str(row[0].split("_")[1])
    as_path = str(row[0].split("_")[2])

    for ip_prefix in row[1]:
        AGREGATED_TABLE.add((str(ip_prefix), next_hop, '0', '0', '0', as_path))


with open('full_RIB_Agregada.csv', mode='w') as rib_agregada:
    rib_writer = csv.writer(rib_agregada)
    rib_writer.writerow(['Network', 'Next Hop', 'Metric', 'LocPrf', 'Weight', 'Path'])

    for elem in AGREGATED_TABLE:
		rib_writer.writerow([elem[0], elem[1], elem[2], elem[3], elem[4], elem[5]])
	
    rib_agregada.close()

print ('Full RIB Agregada, de tamano ' + str(len(AGREGATED_TABLE)) + ' correctamente guardada en full_RIB_Agregada.csv')

#---------------------------------------------------------
