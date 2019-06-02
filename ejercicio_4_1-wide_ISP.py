import pybgpstream
import pprint
import numpy as np

#---------------------------------------------------------

# Definitions
TIME_INIT = "2012-03-01"
TIME_END = "2012-03-01 00:05"

COLLECTOR = 'route-views.wide'

# AS target
# ASN: 8966
# ASname: Etisalat

# ISP
targetAS = 2914

#---------------------------------------------------------

# Query configuration
stream = pybgpstream.BGPStream(
		from_time=TIME_INIT,
		until_time=TIME_END,
		filter="type ribs and collector %s and path %s"%(COLLECTOR,targetAS))

#---------------------------------------------------------

# Execution & parse of the query

print ''
print 'ASPATHS to the target AS:'
print '-------------------------'
print ''

index = 0
ASPATHs = []
ASPATHS_v=[]
for elem in stream:
	if str(elem.fields['as-path'].split(' ')[-1]) == str(targetAS):
		if elem.fields['as-path'] not in ASPATHs:
			index += 1
			ASPATHs.append(elem.fields['as-path'])
			print str(index)+' - '+elem.fields['as-path']
			ASPATHS_v.append(np.array(elem.fields["as-path"].split(' ')).astype(int))
