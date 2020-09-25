class iosnoop:

    # def __init__(self):
    # imported inside the class because we only need it when 
    # class is actually used to generate an object
    import subprocess
    import re
    import importlib
    import local_cache as lc
    
    # from datetime import datetime

    # Setting up cache
    # from pymemcache.client.base import Client
    # argus_client = Client(('localhost', 11211))

    # Default time interval is set to 5
    cmd = ['./iosnoop.sh', '5']

    # Default output structure (keys for memchaced) - Used later to map o/p values to their keys
    default_struct = ['COMM', 'PID','TYPE','DEV','BLOCK','BYTES','LATms']

    def __run_iosnoop(self, command):
        global iosnoop_process 
        
        iosnoop_process = self.subprocess.Popen(command,
                            stdout = self.subprocess.PIPE,
                            stderr = self.subprocess.STDOUT)

        # Returning values as they come from the cachestat tool
        return iter(iosnoop_process.stdout.readline, b'')


    def __regex_check(self,input_string: str):

        # Check if we got a correct input first, only then we can process it in regex
        regex_check = "(COMM)"
        result_check = self.re.search(regex_check, input_string)

        # Now matching the actual regex and extracting values
        if result_check:
            regex = "(\d+)"
            result = self.re.findall(regex, input_string)
            if result: return result
        else:
            pass


        
    # Retrieves data from memcached running instance    
    # def retrive_data_cache(self, key: str):
    #     print(self.argus_client.get(key))

    # Capturing cachestat input upto a certain line count then killing the process
    def acquire_iosnoop_data(self, count = 0, count_upto = 4):
        for line in self.__run_iosnoop(self.cmd):
            print(line,'\n')

            input_string = str(line)
            result = self.__regex_check(input_string)
            print('This is result',result)
            # Injecting data into the cache
            # self.__inject_data_cache(result)
            #self.lc.inject_data_cache(result, self.default_struct)

            # Limiting the amount of time the metrics are captured
            count = count + 1
            if count > count_upto: 
                iosnoop_process.kill() 
                break
        
# Memcached is overwriting old data cause of the same keys
cs = iosnoop()
cs.acquire_iosnoop_data()
# cs.lc.retrive_data_cache('2020-09-15_11:25:15.398171')
# cs.retrive_data_cache('buffers_mb')
# (hits:).+(\d+), +([a-z]+): +(\d+), +([a-z]+): +((\d)+\.(\d)%), +[a-z]+_[a-z]+:.+\d
