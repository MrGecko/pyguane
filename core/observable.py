# encoding: utf-8
"""
observable.py

Created by Julien Pilla on 2010-05-21.
"""

class Observable(object):
    def __init__ (self):
        self._subscribers = []
    
    @property
    def clients(self): return [sub[0] for sub in self._subscribers]
    
    @property
    def responses(self): return [sub[1] for sub in self._subscribers]


    def emit(self, *args):
        '''Pass parameters to all observers and update states.'''
        for subscriber in self._subscribers:
            subscriber[1] = subscriber[0](*args)

    def subscribe(self, *clients):
        '''Add new subscribers.'''
        for new_client in clients:
            if new_client not in self.clients:
                self._subscribers.append([new_client, None])
                
                
    def unsubscribe(self, *clients):
        '''Remove the clients from the subscribing list'''
        subscribers = self.clients
        for client in clients:
            if client in subscribers:
                self._subscribers.pop(subscribers.index(client))
                
