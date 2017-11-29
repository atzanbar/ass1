from viterbi import ViterbiTagger
from tag_utils import Decode, multiTagger, save_tagged_file, validateTest
import  sys
from greedyTagger import GreedyTagger

def viterbiTagger(input_file,q_file,e_file,output_file):
    decoder = Decode(q_file, e_file)
    #tagger = GreedyTagger(qdict,edict,totalWords,wordCount,taglist)
    params = {}
    params['tri_w'] = 0.95
    params['bi_w'] = 0.04
    params['uni_w'] = 0.01
    params['emm_w'] = 0.9
    params['sig_w'] = 0.1

    qdict,edict,totalWords,wordCount,taglist = decoder.decode()
    tagger = ViterbiTagger(qdict,edict,totalWords,wordCount,taglist,params)
    taggedlist = multiTagger(tagger.tag_line,input_file )
    save_tagged_file(taggedlist,output_file)
    #run_profiler(multiTagger,tagger.tag_line, inputFileTaged, inputFile)



def main(args):

    viterbiTagger(args[1],args[2],args[3],args[4])
    #viterbiTagger("ass1-tagger-test-input","q.mle","e.mle","outy.txt","")

if __name__ == "__main__":
    main(sys.argv)



