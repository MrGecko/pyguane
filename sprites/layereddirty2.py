
from pygame.sprite import LayeredDirty
from pygame.rect import Rect
from pygame.time import get_ticks


class LayeredDirty2(LayeredDirty):
    def __init__(self, *sprites, **kwargs):
        super(LayeredDirty2, self).__init__(*sprites, **kwargs)
        self._time_threshold = 1000.0/60.0
        if kwargs.has_key("seek_dirties"):
            self._seek_dirties = kwargs["seek_dirties"]
        else:
            self._seek_dirties = True

        self._use_update = True
        self._first_draw = True
    
    @property
    def seek_dirties(self): return self._seek_dirties
    def dontSeekDirtiesNextTime(self):
        self._first_draw = True
        
    @seek_dirties.setter
    def seek_dirties(self, boolean):
        self._seek_dirties = boolean
        
    
    def draw(self, surface, bgd=None):
        """draw all sprites in the right order onto the passed surface.
        LayeredDirty.draw(surface, bgd=None): return Rect_list

        You can pass the background too. If a background is already set,
        then the bgd argument has no effect.
        """

        # speedups
        _orig_clip = surface.get_clip()
        _clip = self._clip
        if _clip is None:
            _clip = _orig_clip
        
        
        _surf = surface
        _surf_rect = _surf.get_rect()
        _sprites = self._spritelist 
        _old_rect = self.spritedict
        _update = self.lostsprites
        _update_append = _update.append
        _ret = None
        _surf_blit = _surf.blit
        _rect = Rect
        #_collidelistall = _rect.collidelistall
        if bgd is not None:
            self._bgd = bgd
        _bgd = self._bgd
        
        _surf.set_clip(_clip)
        # -------
        # 0. deside if normal render of flip
        start_time = get_ticks()

        if (self._use_update or self._seek_dirties) and not self._first_draw: # dirty rects mode
            # 1. find dirty area on screen and put the rects into _update
            # still not happy with that part
            for spr in _sprites:
                if 0 < spr.dirty:
                    # chose the right rect
                    if spr.source_rect:
                        _union_rect = _rect(spr.rect.topleft, spr.source_rect.size)
                    else:
                        _union_rect = _rect(spr.rect)
        
                    _union_rect_collidelist = _union_rect.collidelist
                    _union_rect_union_ip = _union_rect.union_ip
                    i = _union_rect_collidelist(_update)
                    while -1 < i:
                        _union_rect_union_ip(_update[i])
                        del _update[i]
                        i = _union_rect_collidelist(_update)
                    _update_append(_union_rect.clip(_clip))
        
                    _union_rect = _rect(_old_rect[spr])
                    _union_rect_collidelist = _union_rect.collidelist
                    _union_rect_union_ip = _union_rect.union_ip
                    i = _union_rect_collidelist(_update)
                    while -1 < i:
                        _union_rect_union_ip(_update[i])
                        del _update[i]
                        i = _union_rect_collidelist(_update)
                    _update_append(_union_rect.clip(_clip))
            # can it be done better? because that is an O(n**2) algorithm in
            # worst case
        
            # clear using background
            if _bgd is not None:
                for rec in _update:
                    _surf_blit(_bgd, rec, rec)
        
            # 2. draw
            for spr in _sprites:
                if 1 > spr.dirty:
                    if spr._visible:
                        # sprite not dirty, blit only the intersecting part
                        _spr_rect = spr.rect
                    
                        if spr.source_rect is not None:
                            _spr_rect = Rect(spr.rect.topleft, spr.source_rect.size)
                            _spr_source_rect_left = spr.source_rect.left
                            _spr_source_rect_top = spr.source_rect.top
                        else:
                            _spr_source_rect_left = 0
                            _spr_source_rect_top = 0
                        
                        _spr_rect_clip = _spr_rect.clip
                        for idx in _spr_rect.collidelistall(_update):
                            # clip
                            clip = _spr_rect_clip(_update[idx])
                            #print  (spr.source_rect.left + clip[0]-_spr_rect[0], spr.source_rect.top + clip[1]-_spr_rect[1],
                            #        clip[2], \
                            #        clip[3])
        
                            _surf_blit(spr.image, clip, \
                                       (_spr_source_rect_left + clip[0]-_spr_rect[0],
                                        _spr_source_rect_top + clip[1]-_spr_rect[1],
                                        clip[2], clip[3]),
                                        spr.blendmode)
                else: # dirty sprite
                    if spr._visible:
                        _old_rect[spr] = _surf_blit(spr.image, spr.rect, spr.source_rect, spr.blendmode)
                    if spr.dirty == 1:
                        spr.dirty = 0
        
            _ret = list(_update)
        else: # flip, full screen mode        
            if _bgd is not None:
                _surf_blit(_bgd, (0, 0))    
            #print len(_sprites), len(_surf_rect.collidelistall(_sprites))
            for spr in _sprites:
                if spr._visible:
                    _old_rect[spr] = _surf_blit(spr.image, spr.rect, spr.source_rect, spr.blendmode)
            _ret = [_rect(_clip)] # return only the part of the screen changed
        
        
        # timing for switching modes
        # how to find a good treshold? it depends on the hardware it runs on
        end_time = get_ticks()
        #print end_time-start_time
        if end_time-start_time > self._time_threshold:
            self._use_update = False
        else:
            self._use_update = True
        # emtpy dirty areas list
        _update[:] = []
        
        self._first_draw = False
        # -------
        # restore original clip
        _surf.set_clip(_orig_clip)
        return _ret

