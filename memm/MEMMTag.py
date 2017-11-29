from collections import  deque

import numpy as np
import sys

from model_utility import extract_word_features, START, END, load_edict, load_map
from tag_utils import  multiTagger, save_tagged_file
from utilty import softmax, get_abs_file, run_profiler
import pickle


class MemmViterbiTagger:
    def __init__(self, model,fmap,tmap,revtmap,emap,words):
        self.model = model
        self.fmap = fmap
        self.tmap =tmap
        self.revtmap =revtmap
        self.emap = emap
        self.words = words
        self.taglist = tmap.keys()
        self.taglist.append(START)
        self.class_cache = {}

    def extract_test_word_features(self,line_arr,word_num,prev_t,prev_prev_t,f_ex):
        return extract_word_features(line_arr,word_num,prev_t,prev_prev_t,None,f_ex)

    def convert_features(self,feature_l):
        dense_fet_v = np.zeros(len(self.fmap))
        for fet,val in feature_l.items():
            feaure_text =fet + "=" + str(val)
            if feaure_text in self.fmap:
                f = int(self.fmap[feaure_text])
                dense_fet_v[f] = 1.0
        return [dense_fet_v]

    def get_softmaxprob(self,feature_l):
        feature_v = self.convert_features(feature_l)
        prob = self.model.predict_proba(feature_v)
        return prob

    def get_prob(self,inputSentence,word_num,tag,prev_t,prev_prev_t):
        line_arr = inputSentence[:]
        feature_l= self.extract_test_word_features(line_arr,word_num,prev_t,prev_prev_t,False)
        tp = tuple(feature_l.values())
        if tp not in self.class_cache:
            feature_v= self.extract_test_word_features(line_arr,word_num,prev_t,prev_prev_t,True)
            prob_v = self.get_softmaxprob(feature_v)
            self.class_cache[tp] = prob_v[0]
        else:
            pass
        return self.class_cache[tp][int(self.tmap[tag])]

    def tag_line(self,line):
        # the path matrix
        mat = {1:{('start','start'):1}}
        # pointer bag
        mat_arg = {1:{('start','start'):('','')}}

        inputSentence = line.strip('\n').split(" ")
        inputSentence.insert(0,START)
        inputSentence.insert(0,START)
        inputSentence.append(END)
        inputSentence.append(END)
        for i in range(2,len(inputSentence)-2):
            mat[i] = {}
            mat_arg[i] = {}
            for r in self.taglist:
                word = inputSentence[i].lower()
                if r==START:
                    continue
                if self.words[word]!=0 and (self.emap.get((word,r),-1)==-1):
                    continue
                max_arg= -1
                for t in self.taglist:
                    max_path= 0
                    for t1 in self.taglist:
                        if not (t1,t) in mat[i-1]:
                            continue
                        q_score = mat[i-1][(t1,t)] * self.get_prob(inputSentence,i,r,t,t1)
                        cand = q_score
                        if max_path==0:
                            max_path=cand
                            max_arg=(t1,t)
                        elif  cand > max_path:
                            max_arg = (t1,t)
                            max_path = cand
                    if max_path!=0:
                        mat[i][(t,r)] = max_path
                        mat_arg[i][(t,r)] = max_arg


        mat_len = len(mat)
        t,r =   max(mat[mat_len], key=mat[mat_len].get)
        #print(r,t,i)
        tagged_words= deque()
        for c in range(mat_len,1 ,-1):
            tagged_words.appendleft([inputSentence[c],r])
            t, r = mat_arg[c][(t,r)]

        #print tagged_words
        return tagged_words




def main(args):
    # if (len(args)<6):
    #     print("wrong args")
    #     return

    test_x_file_name = args[1]
    model_file_name = args[2]
    map_file_name = args[3]
    out_file_name = args[4]
    emap_file_name = args[5]


    featuremap,tagmap = load_map(map_file_name)
    rev_tagmap = {int(v):k for k,v in tagmap.items()}
    model = pickle.load(open(model_file_name, 'rb'))
    emap,words = load_edict(emap_file_name)
    tagger = MemmViterbiTagger(model,featuremap,tagmap,rev_tagmap,emap,words)
    taggedlist = multiTagger(tagger.tag_line,test_x_file_name )
    #run_profiler(multiTagger,tagger.tag_line,test_x_file_name,1)
    save_tagged_file(taggedlist,out_file_name)



if __name__ == "__main__":
    main(sys.argv)


