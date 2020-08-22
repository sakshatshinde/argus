class operating_system:
    # OS object used as an identifier

    def __init__(self):
    # lib distro is imported inside the class because we only need it when 
    # class is actually used to generate an object

        import distro
        import os

        # Identifying the linux distribution and its details
        os_identifiers = distro.linux_distribution()
        self.name, self.version, self.release = os_identifiers

        # Checking the program perms. 
        def perm_check():
            os_uid = os.getuid()
            if os_uid != 0 or os_uid == None:
                raise NameError('Please run this with root user permisions')
            else:
                print('Running with root user perms, as expected ...')
        
        perm_check()
        # print(os)

    def __repr__(self):
        return repr(
            'Values -> name: OS NAME, version: VERSION NUMBER, release: RELEASE NAME)'
        )
    
    def _details(self):
        try:
            print(self.name, self.version, self.release)
        except:
            print('Error detecting the platform')



os = operating_system()
print(os._details())
