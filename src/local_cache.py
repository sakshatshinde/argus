from datetime import datetime
from pymemcache.client.base import Client

argus_client = Client(('localhost', 11211))


# DEFINE A DEFAULT STRUCT FOR EACH TOOL BEFORE USING THIS !!!!!!!!!

def inject_data_cache(ingest_data, default_struct, TOOL):
        # self.argus_client.set_many()
        
        
        # Mapping incoming data to their identifiers
        if ingest_data is not None: 

            # Use date - time (seconds) as key 
            key_datetime = str(datetime.now()).replace(" ", "_")
            # print(key_datetime)
        
            if TOOL == 'CACHESTAT':
                # Convert dict -> str to store in memcached
                input_data = str(dict(zip(default_struct, ingest_data)))

            if TOOL == 'IO_LATENCY':
                ms_range = list(ingest_data.keys())
                IO = list(ingest_data.values())
                IO = sum(IO, [])
                print('Ms', ms_range)
                print('IO', IO)
                
                input_data = 'ms_range' + str(ms_range) + 'IO' + str(IO)
                # print(input_data)

            print('This will be injected:', input_data)

            # print(key_datetime, input_data)
            if input_data != 'ms_range[]IO[]':
                argus_client.set(key_datetime, input_data)

# Retrieves data from memcached running instance    
def retrive_data_cache(key: str):
    print(argus_client.get(key))

# reset the entire cache
def flush_entire_cache():
    argus_client.flush_all()
    print('The entire cache has been flushed')

# KEY = DATE_TIME
retrive_data_cache('2021-01-14_18:43:10.533409')
# flush_entire_cache()