

from pygame.rect import Rect
#from Box2D import *

from Box2D import b2PolygonShape, b2Vec2


class PhysicBody(object):
    
    def __init__(self, world, position, shape_list, body_type, mass=0.0, active=True,):
        #b_def = world.createBodyDef(position, active)
        #b_def.massData.mass = mass
        self._body = world.createBody(position=position, type=body_type)
        self.addShape(world, shape_list)
                
    def addShape(self, world, shape):
        #shortcuts
        createShape = self._body.CreateFixturesFromShapes
        #add shapes
        for s in shape:
            if isinstance(s, Rect):
                createShape(b2PolygonShape(vertices=[s.topleft, s.bottomleft, s.bottomright, s.topright]))
            else:
                createShape(b2PolygonShape(vertices=s))
            
    @property
    def body(self): return self._body        
        
    @property
    def shapes(self): return self._body.shapeList
    
    @property
    def mass(self): return self._body.mass
    
    @property
    def position(self): return self._body.position
    
    @property
    def user_data(self): return self._body.userData
    
    @property
    def is_sleeping(self): return self._body.awake
    
    
    @user_data.setter
    def user_data(self, d): 
        self._body.userData = d
    
    def setLinearVelocity(self, vec):
        self._body.linearVelocity = b2Vec2(vec)
    
    def applyImpulse(self, vec, point=None):
        if point is None:
            point = self._body.GetWorldCenter()
        self._body.ApplyImpulse(b2Vec2(vec), point)
    
    def wakeUp(self):
        self._body.awake = True

