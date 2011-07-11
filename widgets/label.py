
#from pygame.surface import Surface
from pygame.color import Color
#from pygame.rect import Rect
from pygame.font import Font

from pyguane.sprites.factory import SpriteFactory
from pyguane.gameobjects.gameobject import GameObject


class Label(GameObject):
    def __init__(self, x, y, size, text="Label", fontname=None, layer=1000, color="white", kind="widget.label"):
        super(Label, self).__init__()
        self._text = text
        try:
            self._color = Color(color)
        except Exception, e:
            try:
                self._color = Color(*color)
            except:
                print "Label color exception:", e
                self._color = Color("white")
        self._font = Font(fontname, size)
        self._sprite = SpriteFactory().fromSurface(kind, self._font.render(text, True, self._color), (x, y), layer=layer)
        self.pinned = True
   
    @property
    def sprite(self): return self._sprite   
    
    @property
    def pinned(self): return self._sprite.pinned
    @pinned.setter
    def pinned(self, value):
        self._sprite.pinned = value
    
    def _render(self, x, y, text, color=None):
        self._text = text
        if color is not None:
            self._color = color
        self._sprite.image = self._font.render(self._text, True, self._color)
        self._sprite.dirty = 1
        self.topleft = (x, y)
    
    @property
    def text(self): return self._text
    @text.setter
    def text(self, value):
        self._render(self.topleft[0], self.topleft[1], value)  
                                                      
    @property
    def color(self): return self._color
    @color.setter
    def color(self, value):
        self._render(self.topleft[0], self.topleft[1], self._text, value)   
                                                    
    @property
    def rect(self): return self._sprite.rect
    
    @property
    def height(self): return self._sprite.height
    @property
    def width(self): return self._sprite.width
        
    @property
    def topleft(self): return self.rect.topleft
    @topleft.setter
    def topleft(self, topleft): self._sprite.rect.topleft = topleft
    
          
        
