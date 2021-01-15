class iolatency:

    # imported inside the class because we only need it when 
    # class is actually used to generate an object
    import subprocess
    import re
    import importlib
    import local_cache as lc
    # from firebase import firebase 

    # Database connection
    # fb = firebase.FirebaseApplication('https://cdac-argus-default-rtdb.firebaseio.com/', None)  

    # Default time interval is set to 5
    cmd = ['../monitoring_scripts/iolatency.sh', '5']

    # Default output structure (keys for memchaced) - Used later to map o/p values to their keys
    default_struct = ['ms_range','I/O','Distribution']

    def force_kill_iolatency(self):
        self.subprocess.call(['rm','~/var/tmp/.ftrace-lock'])
        

    def __run_iolatency(self, command):
        global iolatency_process 
        
        iolatency_process = self.subprocess.Popen(command,
                            stdin   = self.subprocess.PIPE,
                            stdout  = self.subprocess.PIPE,
                            stderr  = self.subprocess.STDOUT)

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
            # match = self.re.findall('#',input_string)
            # result.append(len(match))
            if result: return result


    # Capturing cachestat input upto a certain line count then killing the process
    
    def acquire_iolatency_data(self):

        # batch_check is used to detect batches of outputs from the tool, since we only need 1
        batch_check = 0
        final_result = {}

        for line in self.__run_iolatency(self.cmd):
            print(line,'\n')

            # Here C makes sure that only 1 batch of output is recorded for 1 cache ingest
            if line == b'\n':
            	batch_check = batch_check + 1

            if batch_check > 1:
            	iolatency_process.kill()
            	break

            input_string = str(line)
            result = self.__regex_check(input_string)

            if result and len(result) > 1:
                # making range from using first two values
                key = (result[0],result[1])

                # Popping first 2 vals (keys) so they aren't repeated
                result = result[2:]
                final_result[key] = result
            
            
        

        print('This is final result', final_result)

        # Injecting data into the cache
        self.lc.inject_data_cache(final_result, self.default_struct, 'IO_LATENCY')

        # Sometimes ftrace gets blocked by the process, 
        # so we have to remove the lock and recurse the function
        if(not bool(final_result)):
            self.subprocess.call(['rm', '/var/tmp/.ftrace-lock'])
            self.acquire_iolatency_data() #-> Might cause a bad recursion loop if /var not found
                
                
            
    
cs = iolatency()
cs.acquire_iolatency_data()


# Failed attempts to solve the ftrace blocking problem

# I don't like this solution
                # try:
                #     iolatency_process.send_signal(self.signal.SIGINT)
                # except: 
                #     print("sigint")
        # final_result = {}
        
        # for line in self.__run_iolatency(self.cmd):
        #     print(line,'\n')

        #     input_string = str(line)
        #     result = self.__regex_check(input_string)

        #     # Making first "ms_range as KEY"
        #     if result and len(result)>1:
        #         # making range from using first two values
        #         key = (result[0],result[1])
        #         result.pop(0)
        #         result.pop(0)
        #         final_result[key] = tuple(result)
            
        #     # Injecting data into the cache
        #     # self.lc.inject_data_cache(final_result, self.default_struct)
            
        #     # Limiting the amount of time the metrics are captured
            
        #     count = count + 1
        #     if count > count_upto: 
        #         iolatency_process.kill()
        #         break