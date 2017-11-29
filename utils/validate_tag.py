import sys

from __builtin__ import file

import time




def main(args):
    tagged_file = args[1]
    test_file =args[2]
    start_time = time.time()
    match = 0
    linelistTagged, words = parse_tagged_file(tagged_file)
    linelistAnswer, words = parse_tagged_file(test_file)
    for i in range(len(linelistAnswer)):
            matcht, wordst = validate_row_loss(linelistAnswer[i],linelistTagged[i])
            match += matcht
            words += wordst
    print (str(match) +'/' + str(words*1.0) + ' : ' + str(match/(words*1.0)))
    print("--- %s seconds ---" % (time.time() - start_time))
    return  linelistTagged


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

def parse_tagged_file(tfile):
    linelistTagged = []
    words = 0
    for line in file(tfile):
        items = [item for item in line.split(" ")]
        linelistTagged.append([[w for w in d.strip('\n').split('/')] for d in items])
    return linelistTagged, words


if __name__ == "__main__":
    main(sys.argv)
