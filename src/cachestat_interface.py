class cachestat:

    # def __init__(self):
    # imported inside the class because we only need it when 
    # class is actually used to generate an object
    import subprocess
            
    # Default time interval is set to 5
    cmd = ['../monitoring_scripts/cachestat.sh', '5']


    def __run_cachestat(self, command):
        global cachestat_process 
        
        cachestat_process = self.subprocess.Popen(command,
                            stdout = self.subprocess.PIPE,
                            stderr = self.subprocess.STDOUT)

        # Returning values as they come from the cachestat tool
        return iter(cachestat_process.stdout.readline, b'')


    # Capturing cachestat input upto a certain line count then killing the process
    def acquire_cachestat_data(self, count = 0, count_upto = 10):
        for line in self.__run_cachestat(self.cmd):
            print(line)
            count = count + 1
            if count > count_upto: 
                cachestat_process.kill() 
                break
        
    

# cs = cachestat()
# cs.acquire_cachestat_data()
