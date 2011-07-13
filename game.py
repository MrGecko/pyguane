# encoding: utf-8
"""
game.py

Created by Julien Pilla on 2010-05-20.
"""


from pyguane.core.window import Window

from pyguane.core.egg import Egg
from pyguane.physics.world import PhysicWorld
from pyguane.sprites.factory import SpriteFactory
from pyguane.core.librarian import Librarian
from pyguane.core.gamestate import StateManager

from pygame.rect import Rect
from pygame.gfxdraw import polygon
from pygame.display import flip as displayFlip


class Game(object):
    def __init__(self, width, height):
        self._egg = Egg(width, height,)
        self.clock = self._egg.clock
        
        self.physic_world = PhysicWorld(Rect(-width, -height, width * 3, height * 3))
        self.state_manager = StateManager()
        
        self.sprite_factory = SpriteFactory()
        self._go_librarian = Librarian()
        Window().bgd = "grey"
        
        @self.renderer(Window().surface)
        def renderGame(surface):
            
            if self.physic_world.debug:
                for b in self.physic_world.world:
                    x, y = b.position
                    for fixture in b:
                        vertices = [(vx + x, vy + y) for vx, vy in fixture.shape.vertices]
                        polygon(surface, vertices, self.physic_world.DEBUG_COLOR)
                displayFlip()
                
            return self.sprite_factory.draw(surface, Window().bgd)
    
    
    def getObjects(self, path="*"): return self._go_librarian.get(path)
    def delObjects(self, path): self._go_librarian.delete(path)
    def addObjects(self, path, objs): self._go_librarian.add(path, objs)
    def updateObjects(self, *args, **kargs): self._go_librarian.update(*args, **kargs)
    def getObjectsKeys(self): return self._go_librarian.keys         
    
    def renderer(self, *args):
        return self._egg.Renderer(*args)
    
    def updateWorld(self, *args):
        self._egg.updateWorld(*args)
    
    def observeKeyboard(self, *args):
        self._egg.observeKeyboard(*args)
    
    def unobserveKeyboard(self, *args):
        self._egg.unobserveKeyboard(*args)
    
    def observeMouse(self, *args):
        self._egg.observeMouse(*args)
    
    def unobserveMouse(self, *args):
        self._egg.unobserveMouse(*args)
    
    def hatch(self, *args):
        self._egg.run(*args)
        
    def stop(self):
        self._egg.continue_pyguane = False
    
        
        
        

if __name__ == "__main__":
    
    MYGAME = Game(120, 120)
    
    def myKeyboard(keysdown, keysup):
        if "escape" in keysdown:
            print "Exit !"
            MYGAME.stop()
        else:
            if keysdown != []:
                print keysdown
    
    MYGAME.observeKeyboard(myKeyboard)
    
    MYGAME.hatch()

        
        
