
from pyguane.gameobjects.gameobject import GameObject
from pyguane.rect.extrect import ExtRect
from pyguane.core.window import Window
from pyguane.sprites.factory import SpriteFactory
from physics.constants import BOX2D_UNITS_SYSTEM

class Camera(GameObject):
    
    def __init__(self, rect=None):
        super(Camera, self).__init__()
        if rect is None:
            rect = Window().rect
        self._frame = ExtRect(rect)
        self._last_frame = ExtRect(rect)
        self._updateQuadGroupFromRect = SpriteFactory().updateQuadGroupFromRect
        self._dx, self._dy = 0, 0
        
    @property
    def frame(self): return self._frame    
            
    def update(self, tick):
        self._updateQuadGroupFromRect(self._frame)
        
        quadgroup = SpriteFactory().quadgroup
        if (self._last_frame != self._frame) and (quadgroup is not None):
            for spr in quadgroup.sprites():
                spr.rect.move_ip(self._dx + spr.position.left - spr.rect.left,
                                 self._dy + spr.position.top - spr.rect.top)
                spr.dirty = 1
        
        quadgroup.dontSeekDirtiesNextTime()           
        self._last_frame = self._frame.copy()
            
    def moveIP(self, dx, dy):
        #dx, dy = dx / BOX2D_UNITS_SYSTEM, dy / BOX2D_UNITS_SYSTEM
        self._frame.move_ip(-dx, -dy)
        self._dx += dx
        self._dy += dy
        
