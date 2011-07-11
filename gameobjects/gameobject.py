
#from math import modf

#from pygame.rect import Rect
from pyguane.physics.world import PhysicWorld

class GameObject(object):
    #_shared = []
    
    def __init__(self):
        self._last_tick = 0
        
        try:
            self.update = self.registerUpdateFunc(self.update)
        except AttributeError:
            self.update = self.registerUpdateFunc(lambda tick : None)

        #make me linked to the other game objects
        #self._shared.append(self)

    def __del__(self):
        try:
            self.sprite.kill()
            if self.body is not None:
                PhysicWorld().world.DestroyBody(self.body.body)
        except Exception:# as e :
            pass#print "Error while deleting a game object: %s" % str(e)
         
    def registerUpdateFunc(self, func):
        def update(tick):
            self._last_tick = tick
            func(tick)
        return update
    

        


        
