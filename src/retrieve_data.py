from firebase import firebase  
import pprint

# setting up prettyPrint: because the o/p is messy
pp = pprint.PrettyPrinter(indent=4)

# creating the connection
fb = firebase.FirebaseApplication('https://cdac-argus-default-rtdb.firebaseio.com/', None)  

# metrics = db.reference('metrics')
result = fb.get('cdac-argus-default-rtdb/metrics', None)

# seperating data
cachestat_data = []
io_latency_data = []

for val in result.values():

    # easiest way to get the values since firebase adds its own key
    # nesting(complicating) the already awful dict structure
    metrics = (list(val.values()))

    # extracting metrics
    if (metrics[0].startswith("ms_range")):
        cachestat_data.append(metrics[0])
    elif (metrics[0].startswith("{")):
        io_latency_data.append(metrics[0])


pp.pprint(cachestat_data)
print("-------------------------------------------------")
pp.pprint(io_latency_data)


# pp.pprint(result)
# metric_data = result.values()
# pp.pprint(metric_data)
# print(type(result.values()))
