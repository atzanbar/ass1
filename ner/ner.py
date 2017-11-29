import pickle
from memm.MemmGreedyTagger import load_map, load_edict

from memm.memmviterbi import MemmViterbiTagger

from tag_utils import multiTagger, validateTest
from utilty import get_abs_file


def main(args):
    # if (len(args)<6):
    #     print("wrong args")
    #     return
    map_file_name = 'map.txt'
    test_x_file_name = get_abs_file('..\\data\\ass1-tagger-test-input')
    test_y_file_name = get_abs_file('..\\data\\ass1-tagger-test')
    emapfilename = get_abs_file('..\\data\\e_mle')
    model_file_name= 'model.sav'
    featuremap,tagmap = load_map(map_file_name)
    rev_tagmap = {int(v):k for k,v in tagmap.items()}
    emap,words = load_edict(emapfilename)
    model = pickle.load(open(model_file_name, 'rb'))
    tagger = MemmViterbiTagger(model,featuremap,tagmap,rev_tagmap,emap,words)
    taggedlist = multiTagger(tagger.tag_line,test_x_file_name )
    validateTest(taggedlist,test_y_file_name)
    #greedy_tagger("ass1-tagger-test-input","q.mle","e.mle","outy.txt","")

if __name__ == "__main__":
    main(sys.argv)
