# -*- coding: utf-8 -*-

class Link(object):
    
    def __init__(self):
        self.Ents = []
        self.comm = ''
        
    def add_ent(self, Ent):
        self.Ents.append(Ent)
        
    def __unicode__(self, debug=False):
        s = 'L(%s):  '%self.comm
        for Ent in self.Ents:
            s+= 'E%s - '%Ent.id
        return s[:-2]

    def __str__(self):
        return self.__unicode__().encode('utf-8')