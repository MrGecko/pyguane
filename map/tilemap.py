import json

from pprint import pprint
from pyguane.resources.resourcefactory import ResourceFactory
from pyguane.sprites.factory import SpriteFactory
from pyguane.core.window import Window

import cPickle


class TileMap(object):
    def __init__(self, map_filename):
        
        makeTileFromSymbol = ResourceFactory().makeTileFromSymbol
        try:       
            with open(map_filename) as f:
                map_data = json.load(f)
        except:
            with open(map_filename) as f:
                map_data = cPickle.load(f)         
            
        self._tiles = []
        appendTile = self._tiles.append
        self._x, self._y = 0, 0
        
        x, y = 0, 0
        shift_x, shift_y = 0, 0
        
        if "sequences" in map_data:
            max_width = 0
            block_width, block_height = 0, 0
            print "map loading..."
            for seq in map_data["sequences"]:
                #print "\tbuilding sequence %i" % i
                #location of the tiles sequence
                if "location" in seq:
                    if seq["location"]["kind"] == "absolute":
                        shift_x, shift_y = seq["location"]["pos"]
                    #place the new seq relative to the previous one 
                    elif seq["location"]["kind"] == "relative":
                        shift_x += seq["location"]["pos"][0]
                        shift_y += seq["location"]["pos"][1]
                    #place the new seq relative to the previous one 
                    elif seq["location"]["kind"] == "cardinal":
                        pos = seq["location"]["pos"]
                        if pos == "east":
                            shift_x = shift_x + max_width * block_width
                        elif pos == "west":
                            shift_x = shift_x - seq["max_width"] * seq["block_size"][0]
                        elif pos == "north":
                            shift_y = shift_y - (len(seq["symbols"]) / seq["max_width"]) * seq["block_size"][1]
                        elif pos == "south":
                            shift_y = shift_y + y
                else:
                    #no location specified
                    shift_x, shift_y = 0, 0
                    
                x, y = 0, 0
                
                max_width = seq["max_width"]
                layer = seq["layer"]
                block_width, block_height = seq["block_size"]
                j = 0
                #for each tile of the sequence
                for symbol in seq["symbols"]:
                    if symbol == "+":
                        y += block_height #new row
                        x = 0
                    else:
                        if symbol != "_":
                            #create the tile
                            j += 1
                            new_tile = makeTileFromSymbol(symbol, x + shift_x, y + shift_y, layer)
                            appendTile(new_tile)
                        #new column
                        x += block_width
                        if x / block_width >= max_width:
                            x = 0
                            y += block_height #new row

        #sprites freely located                
        if "free" in map_data:
            for s in map_data["free"]:
                new_tile = makeTileFromSymbol(s["symbol"], s["pos"][0], s["pos"][1], s["layer"])
                appendTile(new_tile)
       
    @property
    def tiles(self): return self._tiles
    
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y
    
    @property
    def position(self): return (self._x, self._y)
    

    
    
