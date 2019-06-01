import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions
TIME_INIT = "2018-03-01"
TIME_END = "2018-03-01 00:05"

# TIME_INIT = "2012-03-01"
# TIME_END = "2012-03-01 00:05"

COLLECTOR_WIDE = 'route-views.wide'
COLLECTOR_SIDNEY = 'route-views.sydney'

# AS target
# ASN: 8966
# ASname: Etisalat
targetAS = 8966

ISPTargetAS = 2914

#---------------------------------------------------------

# Query configuration
stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s and path %s"%(COLLECTOR_WIDE,targetAS))

#---------------------------------------------------------

# Execution & parse of the query

print ''
print 'ASPATHS to the target AS:'
print '-------------------------'
print ''

index = 0
ASPATHS_v=[]
for elem in stream:
	if str(elem.fields['as-path'].split(' ')[-1]) == str(targetAS):
		index += 1
		print str(index)+' - '+elem.fields['as-path']
		ASPATHS_v.append(np.array(elem.fields["as-path"].split(' ')).astype(int))

#---------------------------------------------------------

# ISPs of the AS Etisalat (AS8966) 

print ''
print 'AS from the ISP of the target AS:'
print '---------------------------------'
print ''

ISP_AS = {}
for ASPATH in ASPATHS_v:
	TargetPosition=np.where(ASPATH==targetAS)[0]
	if ASPATH[TargetPosition-1][0] in ISP_AS:
		ISP_AS[ASPATH[TargetPosition-1][0]] += 1
	else:
		ISP_AS[ASPATH[TargetPosition-1][0]] = 1
	
print ISP_AS
