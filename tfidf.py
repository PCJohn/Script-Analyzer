'''
This module handles TFIDF methods for scripts. Contains methods to train a TFIDF model and load the scores for all the words. For a TFIDF_Model object t, t.get_keywords(script) will extract the keywords from the script, their TFIDF scores, and a separate list with the names of all the characters in the script.

Author: Prithvijit Chakrabarty (prithvichakra@gmail.com)
'''

import script_manager as sm
import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk import pos_tag
from nltk import bigrams
from nltk import trigrams
from nltk.collocations import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer,TfidfTransformer,CountVectorizer
import cPickle as pickle

#Decompose the 
def preprocess(script):
    dialogue = ''
    char_list = {}
    scenes = []
    for line in script:
        line = line.strip()
        if not line.isupper():
            dialogue = dialogue+'\n'+line
        else:
            line = line.lower()
            if line in char_list:
                char_list[line] = char_list[line]+1
            else:
                char_list[line] = 1
    return (char_list,dialogue)

class Tokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
        self.stop = stopwords.words('english')

    def __call__(self,script):
        stop = stopwords.words('english')
        dialogue = pos_tag(word_tokenize(script))
        dialogue = [w for w,pos in dialogue if pos[0].upper() in ['N','V']]
        dialogue = [self.wnl.lemmatize(w) for w in dialogue if self.good_word(w)]
        return dialogue

    def good_word(self,word):
        if not word.isalpha():
            return False
        if word.lower() in self.stop:
            return False
        return True

class TFIDF_Model:
    def __init__(self,path=None):
        self.count_vect = CountVectorizer(tokenizer=Tokenizer())
        self.vec = None
        if not path is None:
            self.load_model(path)

    #Train a TFIDF model
    def train(self):
        #Load movie scripts
        print 'Loading raw scripts...'
        path = 'PATH_TO_FOLDER_WITH_TRAINING_SCRIPTS'
        scripts = sm.load_scripts_path(path)
        raw_doc = [preprocess(script)[1] for name,script in scripts]
        #Frequency count
        print 'Scripts loaded. Running transform.'
        X_train_counts = self.count_vect.fit_transform(raw_doc)
        #Tfidf transform
        self.vec = TfidfVectorizer(tokenizer=Tokenizer())
        tfs = self.vec.fit_transform(raw_doc)

        #Save model
        print 'Saving model...'
        with open('PATH_TO_MODEL_FILE','wb') as f:
            pickle.dump(self.vec,f)

    #Load a model
    def load_model(self,path):
        self.vec = pickle.load(open(path,'rb'))

    #Returns the keywords and their TFIDF scores along with a list of all characters in the script
    def get_keywords(self,script):
        char_list = set([line.strip().lower() for line in script if ((line.strip() != sm.DESC_TAG) & (line.strip().isupper()))])
        res = self.vec.transform(['\n'.join(script)])
        feature_names = self.vec.get_feature_names()
        words = dict([(feature_names[col],res[0,col]) for col in res.nonzero()[1] if (not feature_names[col] in char_list)])
        return (list(char_list),words)
