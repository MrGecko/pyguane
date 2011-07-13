from pyguane.sprites.factory import SpriteFactory
from pyguane.core.window import Window
from pyguane.gameobjects.gameobject import GameObject

from pygame.surface import Surface
from pygame.color import Color


class Overlay(GameObject):
    
    def __init__(self, color="black"):
        
        surface = Surface(Window().size)
        surface = surface.convert()
        
        try:
            color = Color(color)
        except:
            color = Color("black")
            
        surface.fill(color)
            
        self._sprite = SpriteFactory().fromSurface("main.fx.overlay", surface, layer=10000)
        self._sprite.pinned = True
        self._sprite.dirty = 1
        self._sprite.visible = False
        self._sprite.image.set_alpha(0)
        self._fading = 0 # 0: idle | 1: fade in | -1: fade out
        
        
    @property
    def visible(self): return self._sprite.visible
    @visible.setter
    def visible(self, b): self._sprite.visible = b
    
    @property
    def sprite(self): return self._sprite
    
    @property
    def fading(self): return self._fading
    
    def update(self, tick):
        #print self._sprite.visible
        #self._sprite.visible = True
        if self._fading != 0:
            a = self._sprite.image.get_alpha() 
            a += int(self._fading * 0.85 * tick)
             
            if self._fading == 1:
                if a > 255:
                    a = 255
                    self._fading = 0
            else:
                #fade out
                if a < 0:
                    a = 0
                    self._fading = 0
                    self._sprite.visible = False
                 
            self._sprite.image.set_alpha(a) 
            self._sprite.dirty = 1
         
        
    def fadeIn(self, speed=1):
        self._sprite.visible = True
        self._fading = 1
        
    def fadeOut(self, speed=1):
        self._sprite.visible = True
        self._fading = -1
        
        
        
