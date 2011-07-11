# encoding: utf-8
"""
pyguane.py

Created by Julien Pilla on 2010-05-19.
"""


from pyguane.core.window import Window
from pyguane.core.eventmanager import EventManager

from pygame.display import update as displayUpdate
from pygame.display import flip as displayFlip

from pygame.time import wait, Clock

from pyguane.core.observable import Observable
from pyguane.core.singleton import Singleton



@Singleton
class Egg(object):
    
    def __init__(self, width, height, fullscreen = False, opengl_mode = False):
        self._window = Window(width, height, fullscreen, opengl_mode)
        self._event_manager = EventManager()
        self._updateWorld = lambda : 0
        self._clock = Clock()
        
        self.continue_pyguane = True
    
        self._keyboard_observable = Observable()
        @self._event_manager.keyboard
        def keyboardEmitter(keysdown, keysup):
            self._keyboard_observable.emit(keysdown, keysup)
            
        self._mouse_observable = Observable()
        @self._event_manager.mouse
        def mouseEmitter(buttons, pos, relpos):
            self._mouse_observable.emit(buttons, pos, relpos)
             
    def updateWorld(self, obj):
        self._updateWorld = obj
        return self._updateWorld
    
    def observeKeyboard(self, *obj):
        self._keyboard_observable.subscribe(*obj)
        
    def unobserveKeyboard(self, *obj):
        self._keyboard_observable.unsubscribe(*obj)
       
    def observeMouse(self, *obj):
        self._mouse_observable.subscribe(*obj)   
       
    def unobserveMouse(self, *obj):
        self._mouse_observable.unsubscribe(*obj)
        
    @property
    def window(self): return self._window
    @property
    def event_manager(self): return self._event_manager
    @property
    def clock(self): return self._clock
           
    @Singleton
    class Renderer(object):
        def __init__(self, surface):
            self.surface = surface
            #my default renderer drawing callback does nothing
            self._displayCallback = lambda : [] 
            
        def __call__(self, func):
            self._displayCallback = lambda : func(self.surface)
            
        def draw(self):
            #do all the blits then update the screen surface
            displayUpdate(self._displayCallback()) 
            
    @property
    def renderer(self): return self.Renderer()

    def run(self):
        self.Renderer(None) #make a default renderer if there is not
        event_update = self._event_manager.update
        draw = self.renderer.draw
        updateWorld = self._updateWorld
        
        while self.continue_pyguane:
            wait(2)  #don't waste the cpu
            event_update()
            updateWorld()
            draw()
            
    



import sys
from random import randint as rdi

from pygame.draw import rect as drawRect
from pygame.color import Color
from pygame.rect import Rect


if __name__ == '__main__':
    
    iguane = Egg(720, 512)  
    
    pos_x = 100
    new_rect =  Rect(pos_x, 100, 190, 310)
    old_rect = new_rect
    
    @iguane.observeKeyboard
    def myKeyboardFantasticFunction(keysdown, keysup):
        global pos_x
        if "escape" in keysdown:
            print "Byebye !"
            sys.exit()
        elif "space" in keysdown:
            iguane.window.toggleFullscreen()
        elif "right" in keysdown:
            pos_x += 6
        elif "left" in keysdown:
            pos_x -= 6
        #elif "s" in keysdown:
        #    print "window size:", iguane.window.size
  
    #iguane.observeKeyboard(myKeyboardFantasticFunction)
    
    @iguane.observeMouse        
    def myMouseFantasticFunction(buttons, pos, relpos):
        pass#print buttons, pos, relpos
        
    #iguane.observeMouse(myMouseFantasticFunction)    
    
    @iguane.updateWorld
    def update():
        global old_rect, new_rect
        old_rect = Rect(new_rect)
        new_rect =  Rect(pos_x, 100, 190, 310)
        #print "i'm updating my data"
                          
    @iguane.Renderer(iguane.window.surface)       
    def myRendererDrawingFunction(surface):
        #return dirty rects
        #surface.fill(Color("black"))
        return [drawRect(surface, Color("black"), old_rect),
                drawRect(surface, Color("red"), Rect(rdi(0, 700), rdi(0, 500), 12, 12)),
                drawRect(surface, Color("yellow"), new_rect)]
            

    # Let's go !
    iguane.run()
    
    
    
    
    
    
    
    

