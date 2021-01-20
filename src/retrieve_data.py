from firebase import firebase  
import pprint


# setting up prettyPrint: because the o/p is messy
pp = pprint.PrettyPrinter(indent=4)

# creating the connection
fb = firebase.FirebaseApplication('https://cdac-argus-default-rtdb.firebaseio.com/', None)  
result = fb.get('cdac-argus-default-rtdb/metrics', None)

# seperating data
cachestat_data_ms = []
cachestat_data_IO = [] 

# this is seperated from source so no need to seperate
io_latency_data = []

for val in result.values():

    # easiest way to get the values since firebase adds its own key
    # nesting(complicating) the already awful dict structure
    metrics = (list(val.values()))

    # extracting metrics
    if (metrics[0].startswith("ms_range")):
        # cachestat_data.append(metrics[0])
        ms_range_metrics, IO_metrics = metrics[0].split("IO", 1)

        # A very hacky fix to remove ms_range attached to the list so the EVAL() works in the code beneath 
        garbage, ms_range_metrics = ms_range_metrics.split("ms_range")
        
        # storing cleaned and sorted data
        cachestat_data_ms.append(eval(ms_range_metrics))
        cachestat_data_IO.append(eval(IO_metrics))

    elif (metrics[0].startswith("{")):
        
        # storing cleaned and sorted data
        io_latency_data_cleaned = eval(metrics[0])
        io_latency_data.append(io_latency_data_cleaned)



print("-------------------------------------------------")
print("Cachestat MS RANGE DATA")
print("-------------------------------------------------")
pp.pprint( cachestat_data_ms)

print("-------------------------------------------------")
print("Cachestat IO DATA")
print("-------------------------------------------------")
pp.pprint(cachestat_data_IO)

print("-------------------------------------------------")
print("IO_LATENCY IO DATA")
print("-------------------------------------------------")
pp.pprint(io_latency_data)

# pp.pprint(result)
# metric_data = result.values()
# pp.pprint(metric_data)
# print(type(result.values()))
