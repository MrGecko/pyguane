

from pyguane.core.librarian import Librarian
from pyguane.core.singleton import Singleton
from pyguane.map.tile import Tile
from pyguane.physics.body import PhysicBody
from pyguane.physics.constants import BOX2D_UNITS_SYSTEM
from pyguane.physics.world import PhysicWorld
from pyguane.rect.extrect import ExtRect
from pyguane.sprites.factory import SpriteFactory

from Box2D import *

import json



@Singleton
class ResourceFactory(object):
    def __init__(self, *data):
        self._data = {}
        self._librarian = Librarian()
                
        if len(data) > 0:
            self.addFromFile(*data)

            
    @property
    def librarian(self): return self._librarian
    
    def addFromFile(self, data_source):
        with open(data_source) as f:
            new_data = json.load(f)
            
            #met a plat les symboles
            sub_resources = {}
            for symbol, data in new_data.iteritems():
                if "sprites" in data.keys():
                    #ne se recopie pas soi-meme
                    mother_data = data.copy()
                    #ne pas copier les animations du sprite parent
                    del mother_data["sprites"]                    
                    if "animations" in mother_data.keys():
                        del mother_data["animations"]
                    for sub_symbol, sub_data in data["sprites"].iteritems():
                        sub_sprite_data = mother_data.copy()
                        sub_sprite_data.update(sub_data)
                        sub_resources["%s_%s" % (symbol, sub_symbol)] = sub_sprite_data
            
            #ajoute les sprites de premier rangs
            self._data.update(new_data)
            #ajoute egalement les sous sprites, au meme niveau
            self._data.update(sub_resources)
            
        
        librarianAdd = self._librarian.add    
        #On cree enfin les data pour chaque symbole trouve        
        for symbol in self._data.keys():
            t_data = self._makeDataFromSymbol(symbol)
            if isinstance(t_data["kind"], (set, list, tuple)):
                #this symbol has many kinds
                for kind in t_data["kind"]:
                    librarianAdd(kind, symbol)   
            else:
                #this symbol has only one kind or less (default kind)
                librarianAdd(t_data["kind"], symbol)
        #pprint(self._data)        
            
    def _makeDataFromSymbol(self, symbol):
        try:
            t_data = self._data[symbol]
        except KeyError:
            raise KeyError("Error: the symbol \"%s\" is not referenced by the ressource manager." % symbol)
                
        if "reference" in t_data:
            #copy parameters from an existing tile
            ref_symbol = t_data["reference"]
            try:
                for k, v in self._data[ref_symbol].iteritems():
                    if k not in t_data:                        
                        t_data[k] = v
            except KeyError as e:
                print "[Error] Cannot get the reference for the resource %s : no declaration of %s." % (symbol, ref_symbol)
                raise e
        
        t_data.setdefault("colorkey", "green")
        t_data.setdefault("ppa", False)
        t_data.setdefault("area", None)
        t_data.setdefault("kind", "default")
        t_data.setdefault("sprites", {})
        
        if t_data["ppa"] is True:
            t_data["colorkey"] = None
        
        if t_data["area"] is not None:
            t_data["area"] = ExtRect(t_data["area"])
        
        return t_data
        
    def _bindAnimationsFromData(self, data, sprite):
        #bind the animations to the new sprite
        if "animations" in data:
            animations = data["animations"]
            if "frames" in animations:
                addFrame = sprite.addFrame
                for name, frame_area in animations["frames"].iteritems():
                    addFrame(name, ExtRect(frame_area))
            if "clips" in animations:
                addClip = sprite.addClip
                for name, frame_list in animations["clips"].iteritems():
                    addClip(name, frame_list)
    
    def _getDataFromSymbol(self, symbol):
        try:
            if symbol in self._data.keys():
                return self._data[symbol]
        except KeyError as e:
            print "[Error] Cannot get the resource %s : no declaration" % symbol
            raise e
            return {}
            
            
    def _makeSpriteFromData(self, data, x, y, layer=0):
        if data.has_key("layer"):
            layer = data["layer"]
            
        new_sprite = SpriteFactory().fromFile(data["kind"], data["filename"], data["ppa"], (x, y), data["area"], layer)
        if data["colorkey"] is not None:
            new_sprite.setColorKey(data["colorkey"])
            
        self._bindAnimationsFromData(data, new_sprite)
        
        return new_sprite
        
    
    def _makeBodyFromData(self, data, position):
        #make the physic body        
        try:
            p_world = PhysicWorld()
        except Exception, e:
            print e, ": you need to have a physic world before you create your bodies."
            raise e
        
        active = True #active = False means the body will not participate in collisions, ray casts, etc.
        shape_list = []
        mass = 0.0  
        body_type = b2_staticBody
        
        if "body" not in data: 
            #no body specified: going to use the bouding rect   
            rect = ExtRect(data["area"])
            shape_list.append([(0.0, 0.0), (0.0, rect.height * BOX2D_UNITS_SYSTEM),
                               (rect.width * BOX2D_UNITS_SYSTEM, rect.height * BOX2D_UNITS_SYSTEM), (rect.width * BOX2D_UNITS_SYSTEM, 0.0)])#(Rect((0, 0), rect.size))
        

        else:      
            
            body_data = data["body"]
            
            if body_data is None:
                return None

            if "type" in body_data:
                if body_data["type"] == "dynamic":
                    body_type = b2_dynamicBody 
                    
            
            if "active" in body_data:
                active = body_data["active"]
                
            if "mass" in body_data:
                mass = float(body_data["mass"])
            
            if "filename" not in body_data:
                #there is no filename in the body conf
                rect = ExtRect(data["area"])
                shape = [(0.0, 0.0), (0.0, rect.height * BOX2D_UNITS_SYSTEM),
                                   (rect.width * BOX2D_UNITS_SYSTEM, rect.height * BOX2D_UNITS_SYSTEM),
                                   (rect.width * BOX2D_UNITS_SYSTEM, 0.0)]
                shape.reverse()
                shape_list.append(shape)#(Rect((0, 0), rect.size))
            else:
                #try to load the meshes from the file
                try:
                    with open(body_data["filename"]) as f:
                        for line in f.readlines():
                            #begin a new shape
                            if line.startswith('g'):
                                shape_list.append([])
                            #append a vertex to the shape
                            if line.startswith('v'):
                                temp_list = line.split(" ") # [junk, x, z, y]
                                x, y = float(temp_list[1]), float(temp_list[3])
                                shape_list[-1].append((x * BOX2D_UNITS_SYSTEM, y * BOX2D_UNITS_SYSTEM))
                except IOError, e:
                    raise IOError("Error while loading the body data: %s" % (body_data["filename"]))

        #make the body    
        x, y = position
        position = (x * BOX2D_UNITS_SYSTEM, y * BOX2D_UNITS_SYSTEM)

        body = PhysicBody(p_world, position, shape_list, body_type, mass, active)
        return body
        
    def makeBodyFromSymbol(self, symbol, x, y):
        t_data = self._getDataFromSymbol(symbol)
        return self._makeBodyFromData(t_data, (x, y))
       
    
    def makeTileFromSymbol(self, symbol, x, y, layer=0):
        t_data = self._getDataFromSymbol(symbol)
        
        #make the sprite
        new_sprite = self._makeSpriteFromData(t_data, x, y, layer)
        if t_data["ppa"]:
            new_sprite.image.set_alpha(0)
                           
        #make the body
        body = self._makeBodyFromData(t_data, (x, y))
        
        #finally link them into a tile object
        new_tile = Tile(new_sprite, body, t_data["kind"])
        return new_tile
        
        
    def makeSpriteFromSymbol(self, symbol, x, y, layer=0):
        #x, y = (x / BOX2D_UNITS_SYSTEM, y / BOX2D_UNITS_SYSTEM)
        t_data = self._getDataFromSymbol(symbol)    
        new_sprite = self._makeSpriteFromData(t_data, x, y, layer)
        self._bindAnimationsFromData(t_data, new_sprite)
                
        return new_sprite
        

