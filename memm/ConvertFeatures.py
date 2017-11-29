import os

import sys
from collections import defaultdict

tagsset  = set()
feature_set = set()
F2I  ={}
def load_features(f_file):
    fnum = 0
    tnum = 0
    global F2I
    for l in file(f_file):
        linelist = l.split()
        for fet in linelist[1:]:
            if F2I.get(fet,-1)==-1:
                F2I[fet]=fnum
                fnum+=1
        tag  = linelist[0]
        if F2I.get(tag,-1)==-1:
                F2I[tag]=tnum
                tnum+=1
    pass

def save_words(f_file,output_q_file,map_file):

    with open(output_q_file, 'w') as outfile:
        for l in file(f_file):
                linelist = l.split()
                label = str(F2I[linelist[0]])
                features = sorted([F2I[i] for i in  linelist[1:]])
                outfile.write(label + " " +' '.join([str(f)+":1" for f in features])+"\n")
    with open(map_file,'w') as mapfile:
            for l in F2I.items():
                mapfile.write(l[0] +"\t"+ str(l[1])+"\n")



def main(args):
    if (len(args)<3):
        print("wrong args")
        return
    load_features(args[1])
    save_words(args[1],args[2],args[3])

if __name__ == "__main__":
    main(sys.argv)
    # dir = os.path.dirname(os.path.realpath('__file__'))
    # filename = os.path.join(dir, 'output.text')
    # load_features(filename)
    # save_words(filename,"output_v.txt","map.txt")




