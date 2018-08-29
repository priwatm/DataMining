# -*- coding: utf-8 -*-
import pymorphy2

class Entity(object):
    
    def __init__(self, word=''):
        self.id = '0'
        self.word = word
        self.nfrm = ''
        self.wtag = []
        self.etag = []
        self.begs = ''
        self.ends = ''
        self.wlen = 0
        self.ssen = False
        self.Children = []

    def prepare_id(self, id, pre_id=''):
        if pre_id:
            self.id = pre_id + '.' + id
        else:
            self.id = id
        for i, Ent in enumerate(self.Children):
            Ent.prepare_id(unicode(i+1), self.id)
            
    def prepare(self, morph=None):
        if not self.word:
            return
         
        self.word = self.word.replace('\n', '').replace('\t', '')
        self.begs = self.word[0]
        self.ends = self.word[-1]

        punctuation = [' ', '.', ',', ':', '"', "'"]
        for punc in punctuation:
            self.word = self.word.replace(punc, '')
        self.wlen = len(self.word)
        
        if morph is None:
            morph = pymorphy2.MorphAnalyzer()
        parse = morph.parse(self.word)[0]
        self.nfrm = parse.normal_form
        self.wtag = parse.tag

    def child_append(self, Ent):
        if len(self.Children) == 0:
            self.begs = Ent.begs
            self.ssen = Ent.ssen
        self.ends = Ent.ends
        self.wlen+= Ent.wlen
        self.Children.append(Ent)       
        
    def is_like(self, word):
        if word == self.nfrm:
            return True
        for Child in self.Children:
            if Child.is_like(word):
                return True
        return False       
        
    def __unicode__(self, lvl=0, blnk=2, debug=False):
        s = ' '*(blnk*lvl)
        s+= '{E%s %s} '%(self.id, ' ; '.join(self.etag))
        if self.ssen:
            s = s[:-2] + ' sent_start } '
        if self.word :
            s+= '|%s| '%self.word
        if self.nfrm:
            s+= '(NF:%s) '%self.nfrm
        if debug and self.wtag:
            s+= '[%s] '%self.wtag.__str__()
        s+= '\n'
        for Child in self.Children:
            s+= Child.__unicode__(lvl+1, blnk, debug) + '\n'
        return s[:-1]
    
    def __str__(self):
        return self.__unicode__().encode('utf-8')