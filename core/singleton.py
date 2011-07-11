

class Singleton: 
    """Singleton
    
       a simple Singleton class decorator
    """
    # on @ decoration
    def __init__(self, aClass):         
        self._aClass = aClass
        self._instance = None
        
    # on instance creation
    def __call__(self, *args, **kargs):  
        if self._instance is None:
            self._instance = self._aClass(*args, **kargs) 
        return self._instance
