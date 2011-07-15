
from Box2D import *
from pygame.draw import *
from pygame.rect import Rect
from pyguane.core.singleton import Singleton
from pyguane.physics.body import PhysicBody



class MyContactListener(b2ContactListener):
    def __init__(self): 
        super(MyContactListener, self).__init__() 
        pass
       
    def Add(self, point):
        """Handle add point"""
        print "point:", point
        pass
    def Persist(self, point):
        """Handle persist point"""
        print "point:", point
        pass
    def Remove(self, point):
        """Handle remove point"""
        print "point:", point
        pass
    def Result(self, point):
        """Handle results"""
        print "point:", point
        pass
    
class MyContactFilter(b2ContactFilter):
    def __init__(self):
        super(MyContactFilter, self).__init__()
    def ShouldCollide(self, shape1, shape2):
        return True

    
@Singleton
class PhysicWorld:
    
    DEBUG_COLOR = (220, 20, 20)
    
    def __init__(self, bb, gravity=(0, 0), sleep=True):
        worldAABB = b2AABB()
        worldAABB.lowerBound = (bb.left, bb.top)
        worldAABB.upperBound = (bb.width, bb.height)    
        self._world = b2World(gravity, sleep)#, contactListener=MyContactListener())
        self.debug = False

    @property
    def world(self): return self._world    
    
    def step(self, f, velocity, position):
        self._world.Step(f, velocity, position)
    
    def createBody(self, position, type):
        return self._world.CreateBody(type=type, position=position)
    
    def createPhysicBody(self, *args, **kargs):
        return PhysicBody(self, *args, **kargs)
        
    def query(self, *args, **kargs):
        return self._world.Query(*args, **kargs)


     
if __name__ == "__main__":
    p_world = PhysicWorld(Rect(0, 0, 5000, 5000))

    my_entity = p_world.createPhysicBody((200, 100), [], [], mass=10)
    print my_entity.body
    
    i = 0
    while i < 100:
        #body.ApplyForce(b2Vec2(0,15), body.GetPosition())
        #my_entity.applyForce(b2Vec2(0,15))
        i += 1
        p_world.step(1.0 / 60, 10, 8)
        print my_entity.position, my_entity.mass

