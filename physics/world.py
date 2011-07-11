
from pygame.rect import Rect
from Box2D import *

from pyguane.core.singleton import Singleton
#from pyguane.core.window import Window

from pygame.draw import *
#from pygame.display import flip as displayFlip

from pyguane.physics.body import PhysicBody



class myDebugDraw(b2DebugDraw):
    def __init__(self): super(myDebugDraw, self).__init__()
    
    def convertColor(self, color):
        """
        Take a floating point color in range (0..1,0..1,0..1) and convert it to (255,255,255)
        """
        if isinstance(color, b2Color):
            return (int(255 * color.r), int(255 * color.g), int(255 * color.b))
        return (int(255 * color[0]), int(255 * color[1]), int(255 * color[2]))
        
    def DrawCircle(self, center, radius, color):
        pass
    def DrawSegment(self, p1, p2, color):
        pass
    def DrawXForm(self, xf):
        pass
    def DrawSolidCircle(self, center, radius, axis, color):
        pass
    def DrawPolygon(self, vertices, vertexCount, color):
        color = self.convertColor(color)
        polygon(self.surface, color, vertices, 1)
        #print "DrawPolygon [Vertices: %s Count: %d Color: (%f, %f, %f)]" % (vertices, vertexCount, color.r, color.g, color.b)
        pass
    def DrawSolidPolygon(self, vertices, vertexCount, color):
        color = self.convertColor(color)
        polygon(self.surface, color, vertices, 1)
        #print "DrawSolidPolygon [Vertices: %s Count: %d Color: (%f, %f, %f)]" % (vertices, vertexCount, color.r, color.g, color.b)
        pass
        #displayFlip()


class MyContactListener(b2ContactListener):
    def __init__(self): 
        super(MyContactListener, self).__init__() 
       
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
    
    
@Singleton
class PhysicWorld:
    
    DEBUG_COLOR = (220, 20, 20)
    
    def __init__(self, bb, gravity=(0, 0), sleep=True):
        worldAABB = b2AABB()
        worldAABB.lowerBound = (bb.left, bb.top)
        worldAABB.upperBound = (bb.width, bb.height)    
        self._world = b2World(worldAABB, gravity, sleep) 
        self.debug = False
        
        self._cl = MyContactListener()
        self._world.SetContactListener(self._cl)
        
        #self.myDraw = myDebugDraw()
        #self.myDraw.SetFlags(self.myDraw.e_shapeBit) # and whatever else you want it to draw 
        #self.myDraw.surface  = Window().surface
        #self._world.SetDebugDraw( self.myDraw )
    
    @property
    def world(self): return self._world
    
    
    def step(self, f, velocity, position):
        self._world.Step(f, velocity, position)
    
    def createBodyDef(self, pos, active=True):
        body_def = b2BodyDef()
        body_def.active = active
        body_def.allowSleep = True
        #body_def.resitution = 0.2
        #body_def.friction = 0.5
        #body_def.density = 1.0
        #body_def.IsSleeping = True
        #body_def.massData.mass = 2.0
        body_def.position = pos
        return body_def
        

    def createBodyFromDef(self, body_def):
        return self._world.CreateBody(body_def)


    def shapeDefFromVertices(self, vertices):
        shape_def = b2PolygonDef()
        shape_def.setVertices(vertices)
        return shape_def
        
    def shapeDefFromRect(self, r):
        return self.shapeDefFromVertices([r.topleft, r.bottomleft, r.bottomright, r.topright])
    
    
    def createPhysicBody(self, *args, **kargs):
        return PhysicBody(self, *args, **kargs)
        
    def query(self, *args, **kargs):
        return self._world.Query(*args, **kargs)


     
if __name__ == "__main__":
    p_world = PhysicWorld(Rect(0, 0, 5000, 5000))

    my_entity = p_world.createPhysicBody((200, 100), [], [], mass=10)
    
    i = 0
    while i < 100:
        #body.ApplyForce(b2Vec2(0,15), body.GetPosition())
        #my_entity.applyForce(b2Vec2(0,15))
        i += 1
        p_world.step(1.0 / 60, 10, 8)
        print my_entity.position, my_entity.mass

