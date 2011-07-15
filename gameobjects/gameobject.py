

#from pyguane.physics.world import PhysicWorld



class GameObject(object):
    def __init__(self):
        self._last_tick = 0
        try:
            self.update = self.registerUpdateFunc(self.update)
        except AttributeError:
            self.update = self.registerUpdateFunc(lambda * args, **kwargs : None)

    def __del__(self):
        try:
            self.sprite.kill()
        except Exception as e :
            print "Error while deleting a game object: %s" % str(e)
         
    def registerUpdateFunc(self, func):
        def update(*args, **kwargs):
            func(*args, **kwargs)
        return update
    

        


        
