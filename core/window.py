# encoding: utf-8


import pygame
from pygame.locals import *
#from pygame.color import Color

from pyguane.core.singleton import Singleton


#====================  VIDEO FLAGS  ===========================
#default mode
F_DEFAULT = 0
F_DEFAULT_FULLSCREEN = HWSURFACE | FULLSCREEN | DOUBLEBUF 
#opengl mode
F_OGL = OPENGL | DOUBLEBUF
F_OGL_FULLSCREEN = OPENGL | DOUBLEBUF | FULLSCREEN
#============================================================


@Singleton
class Window(object):
    """Window class
    
       The window is the main surface. 
       You can have a standard or an OpenGL display.
    """    
    def __init__(self, width, height, fullscreen=False, opengl_mode=False):        
        self._surf = None
        self._fullscreen = fullscreen
        self._opengl_mode = opengl_mode
        pygame.display.init()
        self.size = (width, height)
        self.bgd = None

    @property
    def caption(self): return pygame.display.get_caption()
    @caption.setter
    def caption(self, title): pygame.display.set_caption(title)
    
    @property
    def width(self): return  self.rect.width
    @width.setter
    def width(self, w): self.size = (w, self.height)
    
    @property
    def height(self): return  self.rect.height
    @height.setter
    def height(self, h): self.size = (self.width, h)
    
    @property
    def surface(self): return self._surf
    
    @property
    def bgd(self): return self._bgd
    @bgd.setter
    def bgd(self, color): 
        if color is None:
            self._bgd = None
        else:
            self._bgd = self._surf.copy()
            try:
                self._bgd.fill(Color(color))
            except:
                self._bgd.fill(color)
                
    
    @property
    def rect(self): return self._surf.get_rect()
    @rect.setter
    def rect(self, r): self.size = r.size
    
    @property
    def size(self): return self.rect.size
    @size.setter
    def size(self, new_size):
        if self._fullscreen:
            flags = F_OGL_FULLSCREEN if self._opengl_mode else F_DEFAULT_FULLSCREEN
        else:
            flags = F_OGL if self._opengl_mode else F_DEFAULT
        self._surf = pygame.display.set_mode(new_size, flags)

    
    def toggleFullscreen(self):
        if self._fullscreen:
            flags = F_OGL if self._opengl_mode else F_DEFAULT
        else:
            flags = F_OGL_FULLSCREEN if self._opengl_mode else F_DEFAULT_FULLSCREEN
        self._surf = pygame.display.set_mode(self.size, flags)
        self._fullscreen = not self._fullscreen

    def isFullscreen(self): return self._fullscreen
    
    

if __name__ == "__main__":

    win = Window(720, 580, fullscreen=False, opengl_mode=True)    
    """
    win.width = 900
    print  win.rect
    win.size = 350, 500
    win.rect = win.rect.inflate(300,300)
    print win.height
    win.toggleFullscreen()
    win.toggleFullscreen()
    """
    
    tictac = pygame.time.Clock()
    waited = 0
    
    while waited < 5000 :
        waited += tictac.tick()
        pygame.time.delay(10)
        
      
    
