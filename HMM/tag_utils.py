from collections import defaultdict
from utilty import validate_row_loss ,run_profiler
import time
import numpy as np

np.seterr(all='raise')

class Decode:
    def __init__(self,qFile, eFile):
        self.qFile = qFile
        self.eFile = eFile
        self.edict = dict()
        self.qdict = dict()
        self.taglist = set()
        self.wordCount = defaultdict(int)
        self.totalWords = 0

    def decode(self):
        ngram = {}
        emission = {}
        #turn the q data to q dictionary
        for line in file(self.qFile):
            linelist = line.split()
            self.taglist |= set(linelist[:-1])
            ngram[tuple(linelist[:-1])] = int(linelist[-1])
        # turn the e data to e dictionary
        for line in file(self.eFile):
            linelist = line.split()
            word = linelist[0]
            tag = linelist[1]
            emission[tuple([word,tag])] = int(linelist[-1])
            self.totalWords += 1
            self.wordCount[linelist[0]]+=int(linelist[-1])

        for key,value in ngram.items():
            if len(key)>1:
                    stat = (1.0)* value / ngram[tuple(key[0:len(key)-1])]
            else:
                    stat = (1.0)* value /self.totalWords
            self.qdict[key] = stat

        for key,value in emission.items():
                stat = 1.0 * value / ngram[key[1:2]]
                self.edict[key] = stat

        return self.qdict ,self.edict ,self.totalWords, self.wordCount , self.taglist




def multiTagger(tagger, tfileinput ,lineNum=-1):
        start_time = time.time()
        lineCount=0
        linelistAnswer = []
        for line in file(tfileinput):
            lineCount+=1
            if lineNum!=-1 and lineCount>lineNum:
                break
            linelistAnswer.append(tagger(line))
            print(str(lineCount)+'\n')
        print("--- %s seconds ---" % (time.time() - start_time))
        return linelistAnswer

def validateTest(linelistAnswer,tfile,lineNum=-1):
    start_time = time.time()
    linelistTagged = []
    match = 0
    words = 0
    lineCount=0
    for line in file(tfile):
        lineCount+=1
        if lineNum!=-1 and lineCount>lineNum:
            break
        items = [item for item in line.split(" ")]
        linelistTagged.append([[w for w in d.strip('\n').split('/')] for d in items])
    for i in range(len(linelistAnswer)):
            matcht, wordst = validate_row_loss(linelistAnswer[i],linelistTagged[i])
            match += matcht
            words += wordst
    print (str(match) +'/' + str(words*1.0) + ' : ' + str(match/(words*1.0)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return  linelistTagged

def save_tagged_file(tagged_array,output_file_name):
    with open(output_file_name,'w') as out:
        for l in tagged_array:
            line =' '.join(['/'.join(w) for w in l])
            out.write(line+"\n")
