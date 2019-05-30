import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions
TIME_INIT = "2018-03-01"
TIME_END = "2018-03-01 00:05"

TIME_INIT_2 = "2012-03-01"
TIME_END_2 = "2012-03-01 00:05"

COLLECTOR_WIDE = 'route-views.wide'
COLLECTOR_SIDNEY = 'route-views.sydney'

# AS target
# ASN: 8966
# ASname: Etisalat
targetAS = 8966

#---------------------------------------------------------

# Query configuration
stream = pybgpstream.BGPStream(
        from_time=TIME_INIT,
        until_time=TIME_END,
        filter="type ribs and collector %s and path %s"%(COLLECTOR_WIDE,targetAS))

#---------------------------------------------------------

# Execution & parse of the query
index = 0
for elem in stream:
    if str(elem.fields['as-path'].split(' ')[-1]) == str(targetAS):
        index += 1
        print str(index)+' - '+elem.fields['as-path']

#---------------------------------------------------------