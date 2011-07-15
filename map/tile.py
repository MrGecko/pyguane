

from pyguane.gameobjects.gameobject import GameObject

from pyguane.physics.world import PhysicWorld


class Tile(GameObject):
    def __init__(self, sprite, body, kind):
        super(Tile, self).__init__()
        self._kind = kind
        self._sprite = sprite
        self._body = body
        if body is not None:
            self._body.user_data = self 
        
    @property
    def sprite(self): return self._sprite
    
    @property
    def kind(self): return self._kind

    @property
    def body(self): return self._body
    
    @property
    def shapes(self): return self._body.shapes


