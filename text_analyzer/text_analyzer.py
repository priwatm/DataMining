# -*- coding: utf-8 -*-
import pymorphy2

from entity import Entity

class TextAnalyzer(object):

    def __init__(self, Dict, Gram, debug=False):
        self.Dict = Dict
        self.Gram = Gram
        self.Ents = []
        self.Links = []
        self.morph = pymorphy2.MorphAnalyzer()
        self.debug = debug
        
    def analyze(self, txt):
        self.prepare(txt)
        self.compose()
        self.combine()
        self.combine()
        self.parse_links()
        print self
        
    def prepare(self, txt):
        self.Ents = [Entity(word) for word in txt.split(' ') if len(word)>0]   
        for i, Ent in enumerate(self.Ents):
            Ent.prepare(self.morph)
            Ent.prepare_id(unicode(i+1))
            Ent.etag = self.Dict.define(Ent)
        
        # Помечаем сущности, являющиеся началами предложений:
        self.Ents[0].ssen = True
        for i, Ent in enumerate(self.Ents[1:]):
            if not self.Ents[i-1].ends == '.':
                continue
            if self.Ents[i].begs.lower() == self.Ents[i].begs:
                continue
            if len(self.Ents[i-1].word) == 1:
                continue
            self.Ents[i].ssen = True

    def compose(self):
        for Ent in self.Ents:
            self.Gram.compose(Ent)

    def combine(self):
        i = 0 
        while i<len(self.Ents):
            self.Gram.combine(self.Ents, i)
            self.Ents[i].prepare_id(unicode(i+1))
            i+=1
    
    def parse_links(self):
        self.Links = self.Gram.parse_links(self.Ents)                  
         
    def get_info(self, word):
        word_nfrm = self.morph.parse(word)[0].normal_form
        Ent0 = None
        for Ent in self.Ents:
            if Ent.is_like(word_nfrm):
                Ent0 = Ent
                break
        if Ent0 is None:
            print u'Похожих сущностей не найдено.'
            return
        Entr, Linksr = [], []
        for L in self.Links:
            if Ent0 in L.Ents:
                Linksr.append(L)
                Entr.extend(L.Ents)
        Entr = list(set(Entr))
        print '--- Искомая сущность:'
        print Ent0
        print '--- Связанные сущности:'
        for Ent in Entr:
            if Ent == Ent0:
                continue
            print Ent  
        print '--- Связи:'
        for L in Linksr:
            print L        
        
    def __unicode__(self):
        s = '--------> TextAnalyzer\n'
        s+= '--------| Result of text analysis:\n'
        for Ent in self.Ents:
            s+= Ent.__unicode__(debug=self.debug) + '\n'
        s+= '--------| Result of links analysis:\n'
        for Link in self.Links:
            s+= Link.__unicode__(debug=self.debug) + '\n'
        return s[:-1]
    
    def __str__(self):
        return self.__unicode__().encode('utf-8')
