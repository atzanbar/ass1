
import sys
import numpy as np
from model_utility import extract_word_features, START, END, load_map
from tag_utils import multiTagger, save_tagged_file, validateTest
import pickle


count = 0
class MemmgreedyTagger:
    def __init__(self, model,fmap,tmap):
        self.model = model
        self.fmap = fmap
        self.tmap =tmap
        self.class_cache = {}
    def extract_test_word_features(self,line_arr,word_num,prev_t,prev_prev_t):
        return extract_word_features(line_arr,word_num,prev_t,prev_prev_t,None)

    def convert_features(self,feature_l):
        dense_fet_v = np.zeros(len(self.fmap))
        for fet,val in feature_l.items():
            feaure_text =fet + "=" + str(val)
            if feaure_text in self.fmap:
                f = int(self.fmap[feaure_text])
                dense_fet_v[f] = 1
        return [dense_fet_v]

    def get_features_v(self,line,word_num,prev_t,prev_prev_t):
        line_arr = line[:]
        feature_l= self.extract_test_word_features(line_arr,word_num,prev_t,prev_prev_t)
        return self.convert_features(feature_l)

    def get_class(self,inputSentence,word_num,previous1,previous2):
        tp = tuple([inputSentence[word_num],previous1,previous2])
        # if tp in self.class_cache:
        #     return self.class_cache[tp]
        f_v  =self.get_features_v(inputSentence,word_num,previous1,previous2)
        p_class = self.model.predict(f_v)
        self.class_cache[tp] = p_class
        return p_class

    def tag_line(self, line):

        inputSentence = line.strip('\n').split(" ")
        retdic = []
        previous2 = "start"
        previous1 = "start"
        inputSentence.insert(0,START)
        inputSentence.insert(0,START)
        inputSentence.append(END)
        inputSentence.append(END)
        for word_num in range(2,len(inputSentence)-2):
            p_class = self.get_class(inputSentence,word_num,previous1,previous2)
            wordTag= self.tmap[int(p_class)]
            previous2 = previous1
            previous1 = wordTag
            retdic.append([inputSentence[word_num], wordTag])

        return retdic




def main(args):

    test_x_file_name = args[1]
    model_file_name = args[2]
    map_file_name = args[3]
    out_file_name = args[4]


    featuremap,tagmap = load_map(map_file_name)
    rev_tagmap = {int(v):k for k,v in tagmap.items()}
    model = pickle.load(open(model_file_name, 'rb'))
    tagger = MemmgreedyTagger(model,featuremap,rev_tagmap)
    taggedlist = multiTagger(tagger.tag_line,test_x_file_name)
    save_tagged_file(taggedlist,out_file_name)


if __name__ == "__main__":
    main(sys.argv)
