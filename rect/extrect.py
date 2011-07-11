from pygame.rect import Rect
#from pygame.transform import rotate, scale, smoothscale

from math import modf


class ExtRect(Rect):
    def __init__(self, *args, **kargs):
        super(ExtRect, self).__init__(*args, **kargs)
        self._buffer_dx = 0.0
        self._buffer_dy = 0.0
        
    def move(self, dx, dy):
        dx += self._buffer_dx
        dy += self._buffer_dy 

        future_rect = super(ExtRect, self).move(dx, dy)
        if future_rect is self:
            #continue to put into buffer
            self._buffer_dx = dx
            self._buffer_dy = dy
            #return future_rect
        else:
            #use the buffer
            self._buffer_dx = modf(dx)[0]
            self._buffer_dy = modf(dy)[0]
        return future_rect
                    
    def move_ip(self, dx, dy):
        self.center = self.move(dx, dy).center
        
        
if __name__ == "__main__":        
    erect = ExtRect(0, 0, 20, 40)
    erect.move_ip(17.2, 0)
    erect.move_ip(17.6, 0)   
    print erect
       
