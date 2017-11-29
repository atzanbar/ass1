from collections import OrderedDict, deque

import numpy as np

from hmmscore import Scorer


class ViterbiTagger:
    def __init__(self, ngram_counts,emission_counts,emission_len,wordcount,taglist,params):
        self.ngram_counts  = ngram_counts
        self.emission_counts = emission_counts
        self.emission_len = emission_len
        self.wordCount = wordcount
        self.taglist = list(iter(taglist))
        self.taglist.append('start')
        self.scorer = Scorer(self.ngram_counts, self.emission_counts,self.emission_len,self.wordCount,params)
        self.bigram = [zip(self.taglist,self.taglist)]

    def tag_line(self,line):
        bi_per_size = len(self.taglist)**2
        # the path matrix
        mat = {0:{('start','start'):0}}
        # pointer bag
        mat_arg = {0:{('start','start'):('','')}}

        words = (line.strip('\n').split(" "))
        for i in range(1,len(words)+1):
            mat[i] = {}
            mat_arg[i] = {}
            word = words[i-1]
            for r in self.taglist:
                e_score = self.scorer.get_e_scrore(word,r,i==1)
                if e_score == 0 :
                    continue
                max_arg= -1
                for t in self.taglist:
                    max_path= 0
                    for t1 in self.taglist:
                        if not (t1,t) in mat[i-1]:
                            continue
                        q_score = mat[i-1][(t1,t)] + self.scorer.get_q_score(r,t,t1)
                        cand = e_score+q_score
                        if max_path==0:
                            max_path=cand
                            max_arg=(t1,t)
                        elif  cand > max_path:
                            max_arg = (t1,t)
                            max_path = cand
                    if max_path!=0:
                        mat[i][(t,r)] = max_path
                        mat_arg[i][(t,r)] = max_arg



        t,r =   max(mat[len(words)], key=mat[len(words)].get)
        #print(r,t,i)
        tagged_words= deque()
        for c in range(len(words),0 ,-1):
            tagged_words.appendleft([words[c-1],r])
            t, r = mat_arg[c][(t,r)]

        #print tagged_words
        return tagged_words
