class cachestat:

    # def __init__(self):
    # imported inside the class because we only need it when 
    # class is actually used to generate an object
    import subprocess
    import re
    from datetime import datetime

    # Setting up cache
    from pymemcache.client.base import Client
    argus_client = Client(('localhost', 11211))

    # Default time interval is set to 5
    cmd = ['../monitoring_scripts/cachestat.sh', '5']

    # Default output structure (keys for memchaced) - Used later to map o/p values to their keys
    default_struct = ['hits', 'misses','mbd','ratio','buffers_mb','cached_mb']

    def __run_cachestat(self, command):
        global cachestat_process 
        
        cachestat_process = self.subprocess.Popen(command,
                            stdout = self.subprocess.PIPE,
                            stderr = self.subprocess.STDOUT)

        # Returning values as they come from the cachestat tool
        return iter(cachestat_process.stdout.readline, b'')


    def __regex_check(self,input_string: str):

        # Check if we got a correct input first, only then we can process it in regex
        regex_check = "(hits:)"
        result_check = self.re.search(regex_check, input_string)

        # Now matching the actual regex and extracting values
        if result_check:
            regex = "(\d+)"
            result = self.re.findall(regex, input_string)
            if result: return result
        else:
            pass

    def __inject_data_cache(self, ingest_data):
        # self.argus_client.set_many()
        
        # Mapping incoming data to their identifiers
        if ingest_data is not None: 

            # Use date - time (seconds) as key 
            key_datetime = str(self.datetime.now()).replace(" ", "_")

            # Convert dict -> str to store in memcached
            input_data = str(dict(zip(self.default_struct, ingest_data)))
            
            # print(key_datetime, input_data)
            self.argus_client.set(key_datetime, input_data)
        
    # Retrieves data from memcached running instance    
    def retrive_data_cache(self, key: str):
        print(self.argus_client.get(key))

    # Capturing cachestat input upto a certain line count then killing the process
    def acquire_cachestat_data(self, count = 0, count_upto = 4):
        for line in self.__run_cachestat(self.cmd):
            print(line,'\n')

            input_string = str(line)
            result = self.__regex_check(input_string)
            # print('This is result',result)
            # Injecting data into the cache
            self.__inject_data_cache(result)

            # Limiting the amount of time the metrics are captured
            count = count + 1
            if count > count_upto: 
                cachestat_process.kill() 
                break
        
# Memcached is overwriting old data cause of the same keys
cs = cachestat()
cs.acquire_cachestat_data()
cs.retrive_data_cache('hits')
cs.retrive_data_cache('buffers_mb')
# (hits:).+(\d+), +([a-z]+): +(\d+), +([a-z]+): +((\d)+\.(\d)%), +[a-z]+_[a-z]+:.+\d