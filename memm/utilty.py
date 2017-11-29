import os

import np


def words(stringIterable):
    #upcast the argument to an iterator, if it's an iterator already, it stays the same
    lineStream = iter(stringIterable)
    for line in lineStream: #enumerate the lines
        for word in line.split(): #further break them down
            yield word


def run_profiler(f,*args):
    import cProfile, pstats , StringIO
    pr = cProfile.Profile()
    pr.enable()
    f(*args)
    pr.disable()
    s = StringIO.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print (s.getvalue())



def validate_row_loss(orig_row,tagged_row):
    words = 0
    match = 0
    for i in range(len(orig_row)):
        if orig_row[i][0]== tagged_row[i][0]:
            words +=1
            if str(orig_row[i][1]).lower()== str(tagged_row[i][1]).lower():
                 match +=1
            else:
                print ("word: "+orig_row[i][0] + " tag_orig : " + orig_row[i][1] + " tag_tagged : " + str(tagged_row[i][1]))
    return  match,words

def get_abs_file(file):
    dir = os.path.dirname(os.path.realpath('__file__'))
    return os.path.join(dir, file)

def softmax(x):
    m = np.max(x)
    e = np.exp(x - m)
    return e / e.sum()
