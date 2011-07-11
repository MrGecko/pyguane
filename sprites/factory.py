
from pygame.color import Color
from pygame.image import load as loadImage
from pygame.rect import Rect
from pygame.display import flip as displayFlip


from pyguane.core.singleton import Singleton
from pyguane.sprites.sprite import ExtSprite
from pyguane.sprites.layereddirty2 import LayeredDirty2
from pyguane.gameobjects.gameobject import GameObject
from pyguane.core.librarian import Librarian
from pyguane.core.window import Window

from math import ceil

import sys
from pprint import pprint as printPretty


class Leaf(object):
    def __init__(self, r, group, leafs):
        self._rect = r
        self._group = group
        self._leafs = leafs
        
    @property
    def rect(self): return self._rect
    @property
    def group(self): return self._group
    @property
    def leafs(self): return self._leafs
        
    def printPretty(self, indent=1):
        print "RECT: %s  ----  GROUP: %s sprites \n" % (tuple(self.rect), len(self.group.sprites())),
        if self.leafs is not None:
            indent += 1
            for leaf in self.leafs:
                print "   " * indent,
                leaf.printPretty(indent)
            
        
        

#@Singleton
class SpritesQuadTree(object):
    def __init__(self, group, depth=3):
        self._group = group        
        self._depth = depth
        self._rect = self.computeBoundingRect()
        self._structure = self._makeLeafFromRect(self._rect, depth)
        self.fill(self._structure, self._group.sprites())
        self.i = 0
        
    @property
    def structure(self): return self._structure
    
    @property
    def depth(self): return self._depth
    
    @property
    def rect(self): return self._rect
    
    def computeBoundingRect(self): 
        _sprites = self._group.sprites()
        if len(_sprites) == 0:
            return None
        else:
            bouding_rect = _sprites[0].position.unionall([spr.position for spr in _sprites])
            window_rect = Window().rect
            return bouding_rect#.inflate(window_rect.width, window_rect.height)
    
        
    def _makeLeafFromRect(self, r, depth):
        if r is None:
            return None
        elif depth == 0:
            return Leaf(r, LayeredDirty2(), None)
        else:
            r1 = Rect(r.left, r.top, r.w / 2, r.h / 2)
            size = ceil(r.w / 2.0), ceil(r.h / 2.0)
            r2 = Rect(r.midtop, size)
            r3 = Rect(r.midleft, size)
            r4 = Rect(r.center, size)
            if depth == 1:
                return Leaf(r,
                            LayeredDirty2(),
                            (
                               Leaf(r1, LayeredDirty2(), None),
                               Leaf(r2, LayeredDirty2(), None),
                               Leaf(r3, LayeredDirty2(), None),
                               Leaf(r4, LayeredDirty2(), None),
                            )
                       )
            else:
                depth -= 1
                return Leaf(r,
                            LayeredDirty2(),
                            (
                               self._makeLeafFromRect(r1, depth),
                               self._makeLeafFromRect(r2, depth),
                               self._makeLeafFromRect(r3, depth),
                               self._makeLeafFromRect(r4, depth)
                            )
                       )
                        

    def fill(self, leaf, sprites):
        if leaf is None:
            return
        else:
            #filtre les sprites
            my_sprites = [sprites[i] for i in leaf.rect.collidelistall([spr.position for spr in sprites])]
            
            #pinned sprites are in every leaf
            for spr in sprites:
                if spr.pinned or spr.mobile:
                    if spr not in my_sprites:
                        my_sprites.append(spr)
                        
            #repertorie les sprites
            leaf.group.add(my_sprites)
            if leaf.leafs is None:
                return
            else:
                #distribue les sprites dans les feuilles 
                for child_leaf in leaf.leafs:
                    self.fill(child_leaf, my_sprites)
            
        
    def makeGroupFromRect(self, rect, leaf, group=LayeredDirty2()):
        if leaf is None:
            return group
        else:            
            if not leaf.rect.colliderect(rect):     
                self.i += 1       
                return group
            else:
                if leaf.leafs is None:
                    group.add(leaf.group.sprites())
                else:
                    for child_leaf in leaf.leafs:
                        if child_leaf.rect.colliderect(rect):
                            self.i += 1
                            self.makeGroupFromRect(rect, child_leaf, group)
                return group
        
     
    
    def printPretty(self):
        self.structure.printPretty()
    
    
        
@Singleton
class SpriteFactory(object):
    _layered_dirty = LayeredDirty2(_time_threshold=1000. / 60, seek_dirties=False)
    _resources = {} 
    _extra_dirties = []
    _librarian = Librarian()
    _quadtree = None
    _quadgroup = None#_layered_dirty#.copy()
    
    def initQuadTree(self, depth=3):
        if depth < 1:
            depth = 1
        self._quadtree = SpritesQuadTree(self._layered_dirty, depth)
    
    def makeQuadGroupFromRect(self, rect):
        if self._quadtree is None:
            self.initQuadTree()     
        if self._quadgroup is not None:
            old_group = self._quadgroup.copy()
            self._quadgroup.empty()    
            
        group = self._quadtree.makeGroupFromRect(rect, self._quadtree.structure)
        self._quadgroup = old_group
        return group
            
    def updateQuadGroupFromRect(self, rect):
        if self._quadtree is None:
            self.initQuadTree()
        if self._quadgroup is not None:
            seek_dirties = self._quadgroup.seek_dirties 
            #print len(self._quadgroup), rect, 
            self._quadgroup.empty()
        else:
            seek_dirties = None
     
        self._quadgroup = self._quadtree.makeGroupFromRect(rect, self._quadtree.structure)
        
        if seek_dirties is not None:
            self._quadgroup.seek_dirties = seek_dirties
        #self._quadtree.printPretty()
            #print len(self._quadgroup), "  nb collidrect : ", self._quadtree.i
        self._quadtree.i = 0
        
    @property
    def quadgroup(self): return self._quadgroup
    @property
    def quadtree(self): return self._quadtree
    
    @property
    def everything(self): return self._layered_dirty
  
    @property
    def kinds(self): return self._librarian.keys
    
    def getSpritesFromKind(self, path="*"): return self._librarian.get(path)
    def getSpritesNotFromKind(self, path="*"):
        from_kind = self._librarian.get(path)
        return [spr for spr in self._layered_dirty.sprites() if spr not in from_kind]
        
    def hideSpritesFromKind(self, path, only=False):
        from_kind = self._librarian.get(path)
        for sprite in from_kind:
            sprite.visible = 0
            sprite.dirty = 1
        #but show the others    
        if only:
            not_from_kind = [spr for spr in self._layered_dirty.sprites() if spr not in from_kind]
            for sprite in not_from_kind:
                sprite.visible = 1
                sprite.dirty = 1
            
    def showSpritesFromKind(self, path, only=False):
        from_kind = self._librarian.get(path)
        for sprite in from_kind:
            sprite.visible = 1
            sprite.dirty = 1
        #but hide the others    
        if only:
            not_from_kind = [spr for spr in self._layered_dirty.sprites() if spr not in from_kind]
            for sprite in not_from_kind:
                sprite.visible = 0
                sprite.dirty = 1
    
        
    def delSpritesFromKind(self, path):
        #sprites = self._librarian.get(path)
        #print len(self._layered_dirty.sprites())#, len(self._quadgroup.sprites())
        #self._layered_dirty.remove(sprites)
        self._librarian.delete(path)
        #print len(self._layered_dirty.sprites())#, len(self._quadgroup.sprites())
        

  
    def getSpritesFromLayer(self, path, *layer):
        return [sprite for sprite in self.getSpritesFromKind(path) if sprite.layer in layer]
            
    def updateSpritesFromKind(self, *args, **kargs): self._librarian.update(*args, **kargs)
    
    def fromSurface(self, group_path, surf, dest=None, area=None, layer=0, *groups):
        """ make a new sprite then add it to the layered_dirty group 
        """
        new_sprite = ExtSprite(surf, dest, area, layer, *groups)
        self._layered_dirty.add(new_sprite)
        self._librarian.add(group_path, new_sprite)
        return new_sprite
        
        
    def fromFile(self, group_path, filename, per_pixel_alpha=False, dest=None, area=None, layer=0, *groups):
        """ load a sprite using a resources cache:
            the surfaces are shared and unique in memory
        """
        if filename in self._resources.keys():
            surf = self._resources[filename]
            #surf.convert()
        else:
            surf = loadImage(filename)
            surf = surf.convert_alpha() if per_pixel_alpha else surf.convert()
            self._resources[filename] = surf

            
        return self.fromSurface(group_path, surf, dest, area, layer, *groups)
       

    def addDirty(self, *rects):
        self._extra_dirties.extend(rects)    

    def draw(self, surface, bgd=None):
        """draw all the sprites by drawing the layered_dirty group """
        if self._quadgroup is None:
            return self._layered_dirty.draw(surface, bgd)
            
        if self._quadgroup.seek_dirties:
            #print self._quadgroup
            dirties = self._quadgroup.draw(surface, bgd) + self._extra_dirties
            self._extra_dirties = []
            #only update the dirty rects 
            return dirties
        else:
            #update the whole screen
            return self._quadgroup.draw(surface, bgd)
        

    def update(self, path, tick, *args):
        """update all the sprites by updating the layered_dirty group """
        params = [tick, ] #make the tick always the first param
        params.extend(args)
        
        if path == "*":
            self._layered_dirty.update(*params)
        else:
            self.updateSpritesFromKind(path, *params)
        
        
        
    
