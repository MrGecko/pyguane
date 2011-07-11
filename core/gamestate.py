
from pygame.time import Clock

from pyguane.core.singleton import Singleton

     

class State(object):
    def __init__(self, *args, **kargs):
        self.name = self.__class__.__name__
        self._lock = False
    
    def release(self, *args, **kargs):
        pass
    
    def update(self, *args, **kargs):
        pass
    
    @property
    def locked(self): return self._lock
    def lock(self): self._lock = True 
    def unlock(self): self._lock = False
        
    def __str__(self):
        return self.__class__.__name__



class TimeLockedState(State):
    def __init__(self, *args, **kargs):
        super(TimeLockedState, self).__init__(*args, **kargs)
        self._lock = True
        self._waited = 0
        if not "lock" in kargs.keys():
            raise Exception("you must provide an argument named 'lock'.")
        self._time_to_wait = kargs["lock"]
        self._clock = Clock()

    def update(self, *args, **kargs):
        self._waited += self._clock.tick()
        # Is it time to unlock ?
        if self._waited > self._time_to_wait:
            self._lock = False



@Singleton
class StateManager:
    def __init__(self):
        self._states = []

    @property
    def states(self): return self._states
    
    @property
    def empty(self): return not self._states
    
    def update(self, *args, **kargs):
        if not not self._states:
            self._states[-1].update(*args, **kargs)
            
    @property
    def current(self):
        if not self._states:
            return None
        else:
            return self._states[-1]
               
    def push(self, state, *args, **kargs):
        if not self.empty:
            if not self._states[-1].locked:
                #the top item is not locked, push is allowed
                self._states.append(state(*args, **kargs))
        else:
            #the stack is empty: push is allowed
            self._states.append(state(*args, **kargs))        

    def pop(self):
        if not self.empty:
            #the top item is not locked, removing it is allowed
            if not self._states[-1].locked:
                self._states[-1].release()
                self._states.pop()
            else:
                #print "cant pop :", self.states[-1], "is locked"
                pass
    
    def set(self, state, *args, **kargs):
        self.pop()
        self.push(state, *args, **kargs)
    
    def __str__(self): return  "->".join([s.name for s in self._states])
        
