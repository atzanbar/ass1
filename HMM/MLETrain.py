import sys
from collections import deque
from collections import defaultdict

emission_counts = defaultdict(int)
ngram_counts = [defaultdict(int) for i in range(3)]
emission_counts_len = 0
words_dic = defaultdict(int)
qeue = deque(['start'])
qeue.append('start')
qeue.append('start')

def load_corpus(ifile_name,linesstart=0,lines=-1,unk=False):

    with open(ifile_name) as ifile:
        for l,line in enumerate(ifile):
            if l<linesstart:
                continue
            # todo : move to read pahse
            ngram_counts[0][tuple(['start'])] +=1
            ngram_counts[1][tuple(['start','start'])] +=1
            for pair in line.strip().split(" "):
                global  emission_counts_len
                emission_counts_len+=1
                word, pos = pair.rsplit('/',1)
                if unk:
                    if word not in words_dic:
                        word ='unk'
                else:
                    words_dic[word]+=1
                emission_counts[(word,pos)] += 1
                ngram_counts[0][tuple([pos])] +=1
                qeue.append(pos)
                qeue.popleft()
                bigram = tuple(qeue)[1:]
                ngram_counts[1][bigram] +=1
                trigram = tuple(qeue)
                ngram_counts[2][trigram] +=1
            if lines!=-1 and l>=(linesstart+lines):
                break



def save_words(output_q_file,output_e_file):
    with open(output_q_file, 'w') as outfile:
        for i in range(3):
            for key, value in ngram_counts[i].items():
                 outfile.write('\t'.join(str(s) for s in key)+'\t' + str(value) +"\n")
    with open(output_e_file, 'w') as outfile:
        for key, value in emission_counts.items():
            outfile.write('\t'.join(str(s) for s in key)+'\t' + str(value) +"\n")
    return

def HMM_stats_e():

    return

def HMM_stats(input_file_name,qfile,efile):
    import math
    num_lines = sum(1 for line in open(input_file_name))
    train_lines_num = math.ceil(num_lines*0.8)
    train_unk_lines_num = math.floor(num_lines*0.2)
    load_corpus(input_file_name,0,train_lines_num)
    load_corpus(input_file_name,train_lines_num+1,train_unk_lines_num,True)
    save_words(qfile,efile)



    #print (get_score('chief','JJ','CC','NN',ngram_counts,emission_counts,emission_counts_len))
    #print(dict(itertools.islice(ngram_counts.items(),0,100)))
   # HMM_stats_e()


def main(args):
    if (len(args)<4):
        print("wrong args")
        return
    HMM_stats(args[1],args[2],args[3])
if __name__ == "__main__":
    main(sys.argv)






