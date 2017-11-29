from hmmscore import Scorer

count = 0
class GreedyTagger:
    def __init__(self, ngram_counts,emission_counts,emission_len,wordcount,taglist,params):
        self.ngram_counts  = ngram_counts
        self.emission_counts = emission_counts
        self.emission_len = emission_len
        self.wordCount = wordcount
        self.taglist = taglist
        self.scorer = Scorer(self.ngram_counts, self.emission_counts,self.emission_len,self.wordCount,params)


    def tag_line(self, line):

        inputSentence = line.strip('\n').split(" ")
        retdic = []
        previous2 = "start"
        previous1 = "start"
        cnt=1
        for inputWord in inputSentence:
            cnt=cnt+1
            scoreNow = None
            wordTag = None
            for tag in self.taglist:
                testScore_emm = self.scorer.get_e_scrore(inputWord, tag,cnt==1)
                if testScore_emm==00:
                    continue
                testScore_q = self.scorer.get_q_score(tag, previous1, previous2)
                testScore = testScore_emm + testScore_q
                #print (testScore)
                if testScore==1:
                    wordTag = tag
                    break
                if (scoreNow is None) or testScore > scoreNow:
                    scoreNow = testScore
                    wordTag = tag
            previous2 = previous1
            previous1 = wordTag
            retdic.append([inputWord, wordTag])

        return retdic
