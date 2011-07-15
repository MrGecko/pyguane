
from pyguane.physics.world import PhysicWorld


def flatten(l):
    res = []
    res_append = res.append
    for sublist in l:
        #doesnt trigger with basestring
        if isinstance(sublist, (list, set)):
            for item in sublist:
                res_append(item)
        else:
            res_append(sublist)
    return res


def rec(l):
    flat = flatten(l) 
    if l == flat:
        return l
    else:
        return rec(flat)
    
    
class Librarian(object):
    
    def __init__(self):
        self._data = {}
        
    def __str__(self):
        return str(self._data)
        
    def add(self, section, obj):
        group = self._data
        
        if isinstance(obj, list):
            obj = set(obj)
            
        #adds the obj and avoids to create duplicates at the same level
        if section in group:
            if isinstance(group[section], set):
                try:
                    group[section] |= obj
                except TypeError:
                    group[section].add(obj)
            else:
                try:
                    if isinstance(group[section], basestring):
                        group[section] = obj | set([group[section]]) 
                    else:                        
                        group[section] = obj | set(group[section]) 
                except TypeError:
                    group[section] = set([group[section], obj])
        else:
            group[section] = obj
            
    @property
    def data(self): return rec(self._data.values())
    
    @property
    def keys(self): return rec(self._data.keys())
        
    def get(self, path):
        if path == "*":
            answer = self._data.values()
        else:
            answer = [self._data[key] for key in self._data if key.startswith(path + ".") or (key == path)]        
            answer = rec(answer)

        return answer
                    
    def getByName(self, path):
        answer = [self._data[key] for key in self._data if path in key]
        answer = rec(answer)

        return answer    
    
    def update(self, *args, **kargs):
        if "path" in kargs.keys():
            answer = rec(self.get(kargs["path"]))
            del kargs["path"] #on ne propage pas le path comme argument    
        else:
            answer = rec(self._data.values())
        
        for obj in answer:
            #try:
            obj.update(*args, **kargs)
            #except TypeError:
            #    pass
                
 
    def deleteAll(self):
        #kill the sprites if any
        for key in self._data.keys():
            try:
                for obj in self._data[key]:
                    obj.__del__()
            except TypeError:
                self._data[key].__del__()
            #remove the obj from the librarian
            self._data.pop(key)
        
        
    def delete(self, path):
        path = path + "."
        keys = [k for k in self._data.keys() if k.startswith(path)]
        #delete the root of the path branch
        if path[:-1] in self._data.keys():
            keys.append(path[:-1])
       
        for key in keys:            
            #remove the obj from the librarian
            objs = self._data.pop(key)
            if isinstance(objs, (list, set)):
                #del objs
                for obj in objs:
                    try:
                        if obj.body is not None:
                            PhysicWorld().world.DestroyBody(obj.body.body) #pourri, mais je n'ai pas reussi a le caser ailleurs
                    except AttributeError:
                        pass
                    del obj
            else:
                #un seul objet
                try:
                    if objs.body is not None:
                        PhysicWorld().world.DestroyBody(objs.body.body) #pourri, mais je n'ai pas reussi a le caser ailleurs
                except AttributeError:
                    pass
                objs.__del__()
        
            
                
 


