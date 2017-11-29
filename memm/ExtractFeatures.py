from collections import defaultdict
from model_utility import extract_word_ext, extract_word_features, START, END
import sys

import os

# emission_counts = defaultdict(int)
# ngram_counts = [defaultdict(int) for i in range(3)]
# emission_counts_len = 0
# words_dic = defaultdict(int)
# qeue = deque(['start'])
# qeue.append('start')
# qeue.append('start')

features = []
def count_words(ifile_name,linesstart=0,lines=-1):
    words = defaultdict(int)
    with open(ifile_name) as ifile:
        for l,line in enumerate(ifile):
            if l<linesstart:
                continue
            for p in [pair.rsplit('/',1) for pair  in  line.strip().split(" ")]:
                words[p[0].lower()]+=1
            if lines!=-1 and l>=(linesstart+lines):
                break
    return words


def load_corpus(ifile_name,linesstart=0,lines=-1,unk=False):
    words = count_words(ifile_name,linesstart,lines)
    with open(ifile_name) as ifile:
        for l,line in enumerate(ifile):
            if l<linesstart:
                continue
            # todo : move to read pahse

            line_arr = [pair.rsplit('/',1) for pair  in  line.strip().split(" ")]
            line_arr.insert(0,[START,START])
            line_arr.insert(0,[START,START])
            line_arr.append([END,END])
            line_arr.append([END,END])
            for pairnum in range(2,len(line_arr)-2):
                prev_tag =line_arr[pairnum-1][1]
                prev_prev_tag =line_arr[pairnum-2][1]
                linearr = [w for w,p in line_arr]
                feature_l = extract_word_features(linearr, pairnum, prev_prev_tag, prev_tag, words)
                pos = line_arr[pairnum][1]
                features.append((pos,feature_l))

            if lines!=-1 and l>=(linesstart+lines):
                break

    #F2I = [{l:f} for l,f in enumerate()]




def save_words(output_q_file):
    with open(output_q_file, 'w') as outfile:
        for pos,feature_l in features:
                 outfile.write(pos +'\t' + '\t'.join([r+"="+str(t) for r,t in feature_l.items()])+"\n")



def main(args):
    if (len(args)<3):
        print("wrong args")
        return
    load_corpus(args[1])
    save_words(args[2])
if __name__ == "__main__":
    main(sys.argv)
    # dir = os.path.dirname(os.path.realpath('__file__'))
    # filename = os.path.join(dir, '..\\data\\ass1-tagger-train')
    # load_corpus(filename)
    # save_words("output.text")
