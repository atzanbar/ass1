import numpy as np
import re

word_patterns = [
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
    (r'.*ould$', 'MD'),
    (r'.*ing$', 'VBG'),
    (r'.*ed$', 'VBD'),
    (r'.*ness$', 'NN'),
    (r'.*ment$', 'NN'),
    (r'.*ful$', 'JJ'),
    (r'.*ious$', 'JJ'),
    (r'.*ble$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*ive$', 'JJ'),
    (r'.*ic$', 'JJ'),
    (r'.*est$', 'JJ'),
    (r'^a$', 'PREP'),
    (r'.*s$', 'NNS'),
    (r'.*s$', 'NNPS')

]
capital =   (r'^[A-Z]*')
reg_ex_dic = dict((l[1],l[0]) for l in word_patterns)


class Scorer:


    def __init__(self, ngram_counts,emission_counts,emission_len,wordcount,params):
        self.ngram_counts  = ngram_counts
        self.emission_counts = emission_counts
        self.emission_len = emission_len
        self.wordCount = wordcount
        self.e_score_cache = {}
        self.q_score_cache = {}
        self.params = params


    def get_regex_score(self,word,tag,start):
        ret = 0.1**6
        reg_value = 1
        if (tag in reg_ex_dic) and re.search(reg_ex_dic[tag],word):
            ret= 1
        if (tag=='NNP' and not(start)) and re.search(capital,word):
            ret = 1
        return ret





    def get_e_scrore(self,word,tag,start):
        tp = tuple([word,tag])
        if tp in self.e_score_cache:
            return self.e_score_cache[tp]
        altword = word
        sig_score=0
        word_count = self.wordCount[word]
        if (word_count) < 2:
            word_count = self.wordCount[word.lower()]
            if word_count >1:
                altword = word.lower()
            else:
                altword='unk'
                sig_score = self.get_regex_score(word,tag,start)

        emission_prob = self.emission_counts.get(tuple([altword, tag]),0)
        if emission_prob ==0:
            return 0
        escore = self.params['emm_w'] * emission_prob + self.params['sig_w']*sig_score
        if escore>0.55:
            ret = 1
        else:
            ret = np.log(escore+0.1**10)

        self.e_score_cache[tp] = ret
        return  ret

    def get_q_score(self,tag,prev_tag,prev_prev_tag):
        tp = tuple([tag,prev_tag,prev_prev_tag])
        if tp in self.q_score_cache:
            return self.q_score_cache[tp]

        trigram_prob = self.ngram_counts.get(tuple([prev_prev_tag,prev_tag,tag]),0)
        bigram_prob = self.ngram_counts.get(tuple([prev_tag,tag]),0)
        unigram_prob = self.ngram_counts.get(tuple([tag]),0)
        #print(tag + " : " + str(trigram_prob))
        a = self.params['tri_w'] * trigram_prob
        b = self.params['bi_w'] * bigram_prob
        c = self.params['uni_w'] * unigram_prob
        pos_score = a + b + c
        ret = np.log(pos_score+0.1**10)
        self.q_score_cache[tp] = ret
        return ret

