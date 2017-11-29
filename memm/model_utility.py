from collections import defaultdict


START = 'start'
END = 'end'
cache = {}
def extract_word_ext(word):
    if word in cache:
        return cache[word]
    word_features = {}
    lenWord = len(word)
    for i in range(4):
        if lenWord > i:
            word_features['prefix' + str(i + 1)] = word[:i + 1]
            word_features['suffix' + str(i + 1)] = word[lenWord - i - 1:]
    word_features['contains_number'] = any(char.isdigit() for char in word)
    word_features['contains_hyphen'] = any(char == '-' for char in word)
    word_features['contains_uppercase'] = any(char.isupper() for char in word)
    cache[word] = word_features
    return word_features

def extract_word_features(line_arr, pairnum, prev_prev_tag, prev_tag, words,f_ex=True):
    feature_l = {}
    word = line_arr[pairnum]
    feature_l['form-1'] = line_arr[pairnum - 1].lower()
    feature_l['form-2'] = line_arr[pairnum - 2].lower()
    feature_l['form_1'] = line_arr[pairnum + 1].lower()
    feature_l['form_2'] = line_arr[pairnum + 2].lower()
    feature_l['pt-1'] = prev_tag
    feature_l['pt-2'] = prev_tag + "_" + prev_prev_tag

    if ((words is  None) or words[word] > 4):
        feature_l['form'] = word.lower()
    if f_ex and ((words is  None)  or words[word] <= 4):
        feature_l.update(extract_word_ext(word))

    return feature_l

def is_rear(words,word):
    return words[word] <5

def extract_word_features_reduced(line_arr, pairnum, prev_prev_tag, prev_tag, words,f_ex=True):
    feature_l = {}
    word = line_arr[pairnum]

    if (not is_rear(words,pairnum - 1)):
        feature_l['form-1'] = line_arr[pairnum - 1].lower()
    if (not is_rear(words,pairnum - 2)):
        feature_l['form-2'] = line_arr[pairnum - 2].lower()
    if (not is_rear(words,pairnum + 1)):
        feature_l['form_1'] = line_arr[pairnum + 1].lower()
    if (not is_rear(words,pairnum + 2)):
        feature_l['form_2'] = line_arr[pairnum + 2].lower()
    feature_l['pt-1'] = prev_tag
    feature_l['pt-2'] = prev_tag + "_" + prev_prev_tag

    if (not is_rear(words,word)):
        feature_l['form'] = word.lower()
    else:
        feature_l.update(extract_word_ext(word))

    return feature_l

def load_map(map_file_name):
    featuremap = {i:f for i,f in [p.split()  for p in file(map_file_name) if "=" in p]}
    tagmap = {i:f for i,f in [p.split()  for p in file(map_file_name) if "=" not in p]}
    return featuremap, tagmap

def load_edict(edict_file_name):
    emap = {}
    words = defaultdict(int)
    for l in file(edict_file_name):
        w,p,n = l.split()
        num = int(n)
        emap[(w.lower(),p)] = num
        words[w.lower()] +=num
    return emap,words
