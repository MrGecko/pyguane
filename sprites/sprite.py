
from pygame.color import Color
from pygame.sprite import DirtySprite

from pyguane.rect.extrect import ExtRect

from pygame.transform import scale, smoothscale, rotate


    
class ExtSprite(DirtySprite, object):
    
    def __init__(self, surf, dest=None, area=None, layer=0, *groups):
        super(ExtSprite, self).__init__(*groups)

        self.image = surf
        self._original_image = None
        
        self._frames = {}
        self._current_frame = None
        self._clips = {}
        self._clip = None
        self._clip_index = 0
        self._clip_len = 0
        self._clip_timer = 0
        self._clip_speed = 0
        self._clip_repeat = 0
        
        
        
        #destination rectangle. Its size is useless
        if dest is not None:
            self._position = ExtRect(dest, self.image.get_size())
        else:
            self._position = ExtRect(self.image.get_rect())
        
        self.rect = self._position.copy()  
            
        if area is not None:
            self.source_rect = ExtRect(area)
            self.rect.size = area.size

            
        self._layer = layer
        #self._original_rect = ExtRect(self.rect)
        self._pinned = False  
        self._mobile = False   
        
        
        
    def setColorKey(self, color):
        try:
            self.image.set_colorkey(Color(str(color)))
        except:
            self.image.set_colorkey(color)

        
    #def syncOriginalRect(self):
    #    self._original_rect = ExtRect(self.rect)
    
    def moveIP(self, dx, dy):
        if dx!=0 or dy!=0:
            #self.rect.move_ip(dx, dy)
            self._position.move_ip(dx, dy)
            self.rect = self._position.copy()
            #self.dirty = 1  
            
    def moveToIP(self, x, y):
        self.moveIP(x - self._position.left, y - self._position.top)
        
    
            
    def rotateIP(self, angle):
        old_center = self.rect.center
        old_colorkey = self.image.get_colorkey()
        
        if self._original_image is None:
            self._original_image = self.image.copy()        
            
        self.image = rotate(self._original_image, angle)
        self.image.set_colorkey(old_colorkey)
        #self.rect.size = self.image.get_rect().size
        #self.rect.center = old_center
        self._position.size = self.image.get_rect().size
        self._position.center = old_center 
        self.dirty = 1

        
    #def scaleIP(self, coeff_x, coeff_y):
    #    if coeff_x > 0 and coeff_y > 0:
    #        old_center = self.rect.center
    #        old_colorkey = self.image.get_colorkey()
    #        if self._original_image is None:
    #            self._original_image = self.image.copy()
    #        
    #        new_size = (int(coeff_x*self.rect.width), int(coeff_y*self.rect.width))
    #        self.image = smoothscale(self._original_image, new_size)  
    #        self.image.set_colorkey(old_colorkey)
    #        self.rect = ExtRect(self.image.get_rect())
    #        self.rect.center = old_center
    #        self.dirty = 1
    #        
    #    return self.size
    
    @property
    def pinned(self): return self._pinned
    @pinned.setter
    def pinned(self, value): self._pinned = value
    @property
    def mobile(self): return self._mobile
    @mobile.setter
    def mobile(self, value): self._mobile = value

    #@property
    #def original_rect(self): return self._original_rect

    @property
    def layer(self): return self._layer   
    
    @property
    def position(self): return self._position
    
    @property 
    def top(self): return self._position.top
    @top.setter
    def top(self, y): 
        self._position.top = y
        self.rect.top = y
    
    @property 
    def right(self): return self._position.right
    @right.setter
    def right(self, x): 
        self._position.right = x
        self._position.right = x
    
    @property 
    def bottom(self): return self._position.bottom
    @bottom.setter
    def bottom(self, y): 
        self._position.bottom = y
        self.rect.bottom = y
    
    @property 
    def left(self): return self._position.left
    @left.setter
    def left(self, x):
        self._position.left = x
        self.rect.left = x
    
    @property
    def topleft(self): return self._position.topleft
    @topleft.setter
    def topleft(self, topleft):
        self._position.topleft = topleft
        self.rect.topleft = topleft
    
    @property 
    def size(self): return self.source_rect.size
    @property 
    def width(self): return self.image.get_width()
    @property 
    def height(self): return self.image.get_height()
    #@size.setter
    #def size(self, w, h): self.rect.size = (w,h)

    @property 
    def center(self): return self._position.center
    @center.setter
    def center(self, c): 
        self.moveIP(c[0]-self.center[0], c[1]-self.center[1])


    @property
    def frames(self): return self._frames.keys()
    @property
    def clips(self): return self._clips.keys()
    @property
    def current_clip(self): return self._clip    
    @property
    def current_frame(self): return self._current_frame        
    @current_frame.setter
    def current_frame(self, name):
        if name != self._current_frame:
            if name in self._frames:
                self.source_rect = self._frames[name]
                self._position.size = self.source_rect.size
                self.rect.size = self.source_rect.size
                self._current_frame = name
                #i'm dirty, need to be updated at screen
                self.dirty = 1
            else:
                print "Cannot set the frame %s: it doesn't exist.\n\tAvailable frames are: %s " % (name, str(self.frames)) 
                raise KeyError
                
    def addFrame(self, name, frame):
        self._frames[name] = frame
        
    def addClip(self, name, frame_list):
        self._clips[name] = frame_list
            
    def playClip(self, name, repeat=10000, speed=120): 
        """ Init the clip """
        if name != self._clip:
            if name in self.clips:
                self._clip = name   
                self._clip_index = 0
                self._clip_len = len(self._clips[name])  
                self._clip_timer = 0
                self._clip_speed = speed
                self._clip_repeat = repeat #how many time to loop over the frame list
                self.current_frame = self._clips[name][0]
            else:
                print "Cannot set the clip %s: it doesn't exist.\n\tAvailable clips are: %s " % (name, str(self.clips)) 
                raise KeyError
    
    def stopClip(self, frame_name=None):
        if self._clip is not None:
            #set a custom frame or set to the last frame of the stopped clip
            if frame_name is not None:
                if frame_name in self._frames:
                    self.current_frame = frame_name
            else:
                self.current_frame = self._clips[self._clip][-1]              
            #stop the clip
            self._clip = None
                
    def _nextFrame(self):
        if self._clip is not None and self._clip_repeat > 0:
            if self._clip_index + 1 < self._clip_len:
                #play the next frame in the frame list of the current clip
                self._clip_index += 1
                self.current_frame = self._clips[self._clip][self._clip_index]
            elif self._clip_repeat > 0:
                #restarting the clip, decreasing its lifetime
                self._clip_index = 0
                self.current_frame = self._clips[self._clip][0]
                self._clip_repeat += -1
            else:
                #the lifetime of the clip is ended, stop it then
                #set the frame to the first frame of the clip
                self.current_frame = self._clips[self._clip][0]
                self._clip = None
                    
        
    def _previousFrame(self):
        if self._current_clip is not None:
            if self._index - 1 > 0:
                self._clip_index += -1
            else:
                self._clip_index = self._clip_len - 1
            self.current_frame = self._clips[self._clip][self._clip_index]
            

    def update(self, *args):
        #this method is called by the sprite_factory.update method
        if self._clip is not None:
            self._clip_timer += args[0]
            if self._clip_timer > self._clip_speed:
                self._clip_timer = 0
                self._nextFrame()
            
    def __del__(self):
        self.kill()
        
        
         