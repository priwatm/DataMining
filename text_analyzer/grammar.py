# -*- coding: utf-8 -*-
from entity import Entity
from link import Link

class Grammar(object):
    
    def __init__(self, debug=False):
        self.rules_repl = []
        self.rules_seq = []
        self.rules_link = []
        self.debug = debug
        
    def add_seq(self, rule, res):
        self.rules_seq.append([rule, res])
        
    def add_repl(self, names, name):
        self.rules_repl.append([names, name])
        
    def add_link(self, names, comment, max_sent=1):
        self.rules_link.append([names, comment, max_sent])
        
    def compose(self, Ent):
        if len(Ent.etag) <= 1:
            return
        for rule_repl in self.rules_repl:
            repl, res = rule_repl
            found = True
            for r in repl:
                if not r in Ent.etag:
                    found = False
                    break
            if found:
                for r in repl:
                    Ent.etag.remove(r)
                Ent.etag.append(res)
            
    def combine(self, Ents, i0):
        for rule_seq in self.rules_seq:
            found = True
            seq, res = rule_seq
            for i in range(len(seq)):
                if i0+i >= len(Ents):
                    found = False
                    break
                if not seq[i] in Ents[i0+i].etag:
                    found = False
                    break
            if found == True:
                Ent_new = Entity()
                Ent_new.etag = [res]
                for i in range(len(seq)):
                    Ent_new.child_append(Ents[i0+i])
                Ents[i0] = Ent_new
                for i in range(len(seq)-1):
                    Ents.remove(Ents[i0+1])
              
    def parse_links(self, Ents):
        Links = []
        for rule_link in self.rules_link:
            seq, comm, max_sent = rule_link
            i_seq = 0; num_sent = 0; L = Link()
            for i in range(len(Ents)):
                if Ents[i].ssen:
                    num_sent+= 1
                if num_sent > max_sent:
                    i_seq = 0; num_sent = 0; L = Link()
                if seq[i_seq] in Ents[i].etag:
                    i_seq += 1
                    L.add_ent(Ents[i])
                if i_seq == len(seq):
                    L.comm = comm
                    Links.append(L)
                    i_seq = 0; num_sent = 0; L = Link()
        return Links