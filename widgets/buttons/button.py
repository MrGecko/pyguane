
from pygame.surface import Surface
from pygame.color import Color
#from pygame.rect import Rect

from pyguane.sprites.factory import SpriteFactory
from pyguane.gameobjects.gameobject import GameObject

from pyguane.widgets.label import Label



class Widget(GameObject):
    def __init__(self):
        super(Widget, self).__init__()
        


class Button(Widget):
    def __init__(self, x, y, padding_left, padding_top, text="button", text_size=16, layer=900):
        super(Button, self).__init__()
        
        self._label = Label(0, 0, text_size, text, layer=layer + 1)
        self._label.topleft = (x + padding_left, y + padding_top)
        
        self._padding_left = padding_left
        self._padding_top = padding_top
                               
        frame = Surface((padding_left * 2 + self._label.width, padding_top * 2 + self._label.height))
        frame.fill(Color("grey"))
        self._sprite = SpriteFactory().fromSurface("widget.button", frame, (x, y), layer=layer)
       
 
    def __del__(self):
        self._label.__del__()
        super(Button, self).__del__()
        
    @property
    def sprite(self): return self._sprite
        
    @property
    def text(self): return self._label.text
    @text.setter
    def text(self, value): 
        #set the new text
        self._label.text = value
        #reconstruction of the frame surface, maybe resized
        frame = Surface((self._padding_left * 2 + self._label.width, self._padding_top * 2 + self._label.height))
        frame.fill(Color("grey"))
        self._sprite.image = frame
        #self._sprite = SpriteFactory().fromSurface("widget.button", frame, self._sprite.rect.topleft, layer=self._sprite.layer)
        self._sprite.dirty = 1
        
    
    
    
