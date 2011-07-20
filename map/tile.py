

from pyguane.gameobjects.gameobject import GameObject

#from pyguane.physics.world import PhysicWorld


class Tile(GameObject):
    def __init__(self, sprite, solid, kind):
        super(Tile, self).__init__()
        self._kind = kind
        self._sprite = sprite
        self._solid = solid
        if solid.body is not None:
            self._solid.body.userData = self 
        
    @property
    def sprite(self): return self._sprite
    
    @property
    def kind(self): return self._kind

    @property
    def body(self): return self._solid.body

