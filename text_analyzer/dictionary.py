# -*- coding: utf-8 -*-
SYN_API_KEY = 'dict.1.1.20160106T132630Z.aef9ebca8f2779b7.823218b12b3d7414942be152640071ae9feee16d'
SYN_API_URL = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup'

import requests

class Dictionary(object):
    
    def __init__(self, debug=False):
        self.set_syn_api(False)
        self.dict = {}
        self.debug = debug
        
    def add(self, name, words=[]):
        '''
        Add new dictionary.
        name  - is a string that is the name of the dictionary, for example, u'Имя'.
        words - is a list of words that belong to the dictionary or function
                that return True/False for a given word.
        '''
        self.dict[name] = words

    def define(self, Ent):
        '''
        For a given entity, function define corresponding dictionaries and
        returns a list of dictionaries (or empty list).
        '''
        if not Ent.word or not Ent.nfrm:
            return []
        names = []
        syns = [Ent.nfrm] + self.prepare_syns(Ent.nfrm)
        for name in self.dict.iterkeys():
            if isinstance(self.dict[name], list):
                for syn in syns:
                    if syn in self.dict[name]:
                        names.append(name)
                        break
            else: # self.dict[name] is a function
                if self.dict[name](Ent):
                    names.append(name)
        return names    
    
    def set_syn_api(self, use_syn_api=True, key=None, url=None, syns_max_lvl=1):
        '''
        Set Yandex api key and url. If use_syn_api is True, then while
        entity check the synonims will be used.
        '''
        self.syns_max_lvl = syns_max_lvl
        self.use_syn_api = use_syn_api
        if key is not None:
            self.syn_api_key = key
        else:
            self.syn_api_key = SYN_API_KEY
        if url is not None:
            self.syn_api_url = url
        else:
            self.syn_api_url = SYN_API_URL
     
    def prepare_syns(self, word):
        syns = self.get_syns(word)
        for i in range(2, self.syns_max_lvl+1):
            syns_new = []
            for syn in syns:
                syns_new.extend(self.get_syns(syn))
            syns.extend(list(set(syns_new)))
        syns = list(set(syns))
        return syns
        
    def get_syns(self, word):
        ''' 
        Construction of list of synonims via request to Yandex api.
        '''
        if not self.use_syn_api:
            return []
        params = {'key': self.syn_api_key, 'lang': 'ru-ru', 'text': word}
        res = requests.get(self.syn_api_url, params=params).json()['def']
        if len(res)>0:
            res = [r['text'] for r in res[0]['tr']]
        return res