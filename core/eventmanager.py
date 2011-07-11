# encoding: utf-8

import pygame
from pygame.locals import *
from pygame import event, mouse
from pygame.key import set_repeat, name as getKeyName
from pygame.time import Clock, wait

from pyguane.core.singleton import Singleton

import sys


@Singleton
class EventManager(object):
    
    def __init__(self):
        pygame.init()
        set_repeat(20)
        self._keys_down = set([])
        self._keys_up = set([])
        self._user_events = {}
        self._clock = Clock()
    
    def _keyboardCallback(self, keysdown):
        if "escape" in keysdown:
            quit()
    
    def _mouseCallback(self, buttons_down, pos, relpos):
        for i, but in enumerate(buttons_down):
            if but: print "Button",i,"pressed at pos",pos,"  rel:",relpos
            
    def keyboard(self, func):
        """ register a function as a keyboard callback """
        self._keyboardCallback = func
        return self._keyboardCallback
        
    def mouse(self, func):
        """ register a function as a mouse callback """
        self._mouseCallback = func
        return self._mouseCallback
    
    @property
    def keysdown(self):
        """ get a list of the keys currently pressed """
        return [getKeyName(k) for k in self._keys_down]
        
    @property
    def keysup(self):
        """ get a list of the keys just released """
        return [getKeyName(k) for k in self._keys_up]
         
                  
    @property
    def buttons_down(self): return mouse.get_pressed()
    @property
    def mouse_pos(self): return mouse.get_pos()
    @property
    def mouse_relpos(self): return mouse.get_rel()
              
    def update(self):
        """Update the event loop
        
           Calls the callbacks binded to the mouse and keyboard
           Calls the USEREVENT callback() methods
        """
        self._keys_up = set([])
        for e in event.get():
            if e.type == QUIT:
                pygame.quit()
                sys.exit()
            elif e.type == KEYDOWN:
                self._keys_down.add(e.key)
            elif e.type == KEYUP:
                if e.key in self._keys_down:
                    self._keys_down.remove(e.key)
                    self._keys_up.add(e.key)
            elif e.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
                self._mouseCallback(self.buttons_down, self.mouse_pos, self.mouse_relpos) 
            elif e.type == USEREVENT:
                try: 
                    e.callback()
                except AttributeError:
                    print e," is a USEREVENT with no callback function defined."
                          
        self._keyboardCallback(self.keysdown, self.keysup)


    
if __name__ == "__main__":
    
    manager = EventManager()
    run = True
    
    @manager.keyboard
    def mycallback(keysdown, keysup):
        global run
        if "escape" in keysdown:
            run = False
        
    while run:
        wait(2)
        manager.update()
        
    
    
    

