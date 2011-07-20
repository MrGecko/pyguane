

from pygame.rect import Rect

from Box2D import b2PolygonShape, b2Vec2
from pyguane.physics.world import PhysicWorld



class Solid(object):
    
    def __init__(self, position, body_relative_position, shape_list, body_type, mass=0.0, active=True,):
        self._relative_position = body_relative_position
        if body_type is None:
            self._body = None
        else:
            world = PhysicWorld()
            self._body = world.createBody(position=position, type=body_type)
            self.addShape(world, shape_list)
                
    def addShape(self, world, shape):
        if self._body is not None:
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
    def relative_position(self): return self._relative_position
    
    def applyImpulse(self, vec, point=None):
        if self._body is not None:
            if point is None:
                point = self._body.GetWorldCenter()
                self._body.ApplyImpulse(b2Vec2(vec), point)
              
    #@property
    #def shapes(self): return self._body.shapeList
    #@property
    #def mass(self): return self._body.mass
    #@property
    #def position(self): return self._body.position
    #@property
    #def user_data(self): return self._body.userData
    #@property
    #def is_sleeping(self): return self._body.awake
    #@user_data.setter
    #def user_data(self, d): 
    #    self._body.userData = d
    #def setLinearVelocity(self, vec):
    #    self._body.linearVelocity = b2Vec2(vec)
    #def wakeUp(self):
    #    self._body.awake = True

