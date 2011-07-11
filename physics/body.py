

from pygame.rect import Rect
#from Box2D import *

from Box2D import b2Vec2


class PhysicBody(object):
    
    def __init__(self, world, position, shape_list, collision_filter, mass=0.0, active=True,):
        b_def = world.createBodyDef(position, active)
        b_def.massData.mass = mass
        self._body = world.createBodyFromDef(b_def)
        self.addShape(world, shape_list)
                
    def addShape(self, world, shape):
        #shortcuts
        createShape = self._body.CreateShape
        shapeDefFromVertices = world.shapeDefFromVertices
        shapeDefFromRect = world.shapeDefFromRect
        #add shapes
        for s in shape:
            if isinstance(s, Rect):
                createShape(shapeDefFromRect(s))
            else:
                createShape(shapeDefFromVertices(s))
            
    @property
    def body(self): return self._body        
        
    @property
    def shapes(self): return self._body.shapeList
    
    @property
    def mass(self): return self._body.GetMass()
    
    @property
    def position(self): return self._body.position
    
    @property
    def user_data(self): return self._body.userData
    
    @property
    def is_sleeping(self): return self._body.isSleeping
    
    
    @user_data.setter
    def user_data(self, d): 
        self._body.userData = d
    
    def setLinearVelocity(self, vec):
        self._body.SetLinearVelocity(b2Vec2(vec))
    
    def applyImpulse(self, vec, point=None):
        if point is None:
            point = self._body.GetWorldCenter()
        self._body.ApplyImpulse(b2Vec2(vec), point)
    
    def wakeUp(self):
        self._body.WakeUp()

