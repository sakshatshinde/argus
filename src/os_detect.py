class operating_system:
    # OS object used as an identifier

    def __init__(self):
    # lib distro is imported inside the class because we only need it when 
    # class is actually used to generate an object

        import distro

        os = distro.linux_distribution()
        self.name = os[0]
        self.version = os[1]
        self.release = os [2]

    def __repr__(self):
        return repr(
            'Values -> name: OS NAME, version: VERSION NUMBER, release: RELEASE NAME)'
        )
    
    def _details(self):
        print(self.name, self.version, self.release)

