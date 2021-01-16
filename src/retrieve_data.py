from firebase import firebase  
import pprint

# setting up prettyPrint: because the o/p is messy
# pp = pprint.PrettyPrinter(indent=4)

# creating the connection
fb = firebase.FirebaseApplication('https://cdac-argus-default-rtdb.firebaseio.com/', None)  

# metrics = db.reference('metrics')
result = fb.get('cdac-argus-default-rtdb/metrics', None)


print(result.values())

# pp.pprint(result)
# metric_data = result.values()
# pp.pprint(metric_data)
# print(type(result.values()))
