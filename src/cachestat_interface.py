class cachestat:

    # def __init__(self):
    # imported inside the class because we only need it when 
    # class is actually used to generate an object
    import subprocess
    import re 

    # Default time interval is set to 5
    cmd = ['../monitoring_scripts/cachestat.sh', '5']


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
            if result: print(result)
        else:
            pass

    # Capturing cachestat input upto a certain line count then killing the process
    def acquire_cachestat_data(self, count = 0, count_upto = 4):
        for line in self.__run_cachestat(self.cmd):
            print(line,'\n')

            input_string = str(line)
            self.__regex_check(input_string)

            # Limiting the amount of time the metrics are captured
            count = count + 1
            if count > count_upto: 
                cachestat_process.kill() 
                break
        
    

cs = cachestat()
cs.acquire_cachestat_data()
# (hits:).+(\d+), +([a-z]+): +(\d+), +([a-z]+): +((\d)+\.(\d)%), +[a-z]+_[a-z]+:.+\d