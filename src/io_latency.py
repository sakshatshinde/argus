class iolatency:

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
    cmd = ['./iolatency.sh', '5']

    # Default output structure (keys for memchaced) - Used later to map o/p values to their keys
    default_struct = ['range','I/O','Distribution']

    def __run_iolatency(self, command):
        global iolatency_process 
        
        iolatency_process = self.subprocess.Popen(command,
                            stdout = self.subprocess.PIPE,
                            stderr = self.subprocess.STDOUT)

        # Returning values as they come from the cachestat tool
        return iter(iolatency_process.stdout.readline, b'')


    def __regex_check(self,input_string: str):

        # Check if we got a correct input first, only then we can process it in regex
        regex_check = "(>)"
        result_check = self.re.search(regex_check, input_string)

        # Now matching the actual regex and extracting values
 
        if result_check:
        	regex = "(\d+)"
        	result = self.re.findall(regex, input_string)
        	match = self.re.findall('#',input_string)
        	result.append(len(match))
        	if result: return result


    # Capturing cachestat input upto a certain line count then killing the process
    def acquire_iolatency_data(self, count = 0, count_upto = 10):
        c = 0
        res = {}
        for line in self.__run_iolatency(self.cmd):
            print(line,'\n')
            if line == b'\n':
            	c = c + 1
            if c > 1:
            	iolatency_process.kill()
            	break
            input_string = str(line)
            result = self.__regex_check(input_string)
            if result and len(result)>1:
            	# making range from using first two values
            	key = (result[0],result[1])
            	result.pop(0)
            	result.pop(0)
            	res[key] = tuple(result)
            #print('This is result',result)
            # Injecting data into the cache
            # self.__inject_data_cache(result)
            # self.lc.inject_data_cache(result, self.default_struct)

            # Limiting the amount of time the metrics are captured
            count = count + 1
            if count > count_upto: 
                iolatency_process.kill() 
                break
        print(res)
        
# Memcached is overwriting old data cause of the same keys
cs = iolatency()
cs.acquire_iolatency_data()

