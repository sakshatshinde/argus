from datetime import datetime
from pymemcache.client.base import Client

argus_client = Client(('localhost', 11211))


# DEFINE A DEFAULT STRUCT FOR EACH TOOL BEFORE USING THIS !!!!!!!!!

def inject_data_cache(ingest_data, default_struct):
        # self.argus_client.set_many()
        
        # Mapping incoming data to their identifiers
        if ingest_data is not None: 

            # Use date - time (seconds) as key 
            key_datetime = str(datetime.now()).replace(" ", "_")
            print(key_datetime)
        
            # Convert dict -> str to store in memcached
            input_data = str(dict(zip(default_struct, ingest_data)))
            
            # print(key_datetime, input_data)
            argus_client.set(key_datetime, input_data)

# Retrieves data from memcached running instance    
def retrive_data_cache(key: str):
    print(argus_client.get(key))
