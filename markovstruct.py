import os
import sys
import copy
import time
import pickle
import random
import csv
from threading import Thread, Lock
from multiprocessing import Queue
from nltk.tokenize import sent_tokenize , word_tokenize , TweetTokenizer
from collections import defaultdict 

class markov():
    def __init__(self):
        #self.data =  {():[]}
        self.data= defaultdict(list)
        self.max_Sentence=10
        
    def readfile(self, filename ):
        word =[]
        with open(filename, u'r') as f:
            #contents = f.read()
            # Read the contents of the file
            word=[]
            reader = csv.reader(f)
            for line in reader :
                for  mot in  word_tokenize(line[1]):
                    word.append(mot)
                     
        print("markov struct start ")
        #word = word_tokenize(text)
            #word=self.With_punc(word)
        return word
    
    def With_punc(self,word): 
        stop_ponct=['.','!','?']
        code='/404'
        i=0
        for w in word : 
            if w in stop_ponct :
                word[i]= code 
            i=i+1
        return word 
    
    def _triples(self, words):
        # We can only do this trick if there are more than three words left
        if len(words) < 3:
            return

        for i in range(len(words) - 2):
            yield (words[i], words[i+1], words[i+2])

    
    def creationchaine(self, filename1) :
        words=self.readfile(filename=filename1)
        
        for w1, w2, w3 in self._triples(words):
            key = (w1, w2)
            if key in self.data :
                self.data[key].append(w3)
            else :
                self.data[key]=[w3]
    

        
        
    def generate_sentence(self,seedword=None):
        
        i=0
        error=True 
        exist=False
        if(type(seedword) in [str]):
            seedword=[seedword]
        
        while error :
            keys=self.data
            keys=list(keys)
            random.shuffle(list(keys))
            seed=random.choice(list(keys))
            print(seedword)
            w1, w2 =random.choice(list(self.data.keys()))
            if seedword != None:
                    while len(seedword) > 0:
                        # Loop through all keys (these are (w1,w2)
                        # tuples of words that occurred together in the
                        # text used to generate the database
                       # print(len(keys))
                        for i in range(len(keys)):
                           # print(i)
                           # print(keys[i])
                            if seedword[0] in keys[i]:
                                w1, w2 = keys[i]
                                seedword = []
                                exist=True 
                                break
                        if len(seedword) > 0:
                            seedword.pop(0)
                    
            words= []
            for i in range(self.max_Sentence):
                words.append(w1)
                w1, w2 = w2, random.choice(self.data[(w1, w2)])
                
            words.append(w2)
            for i in range(0, len(words)):
                if (i == 0) or (u'.' in words[i-1]) or(words[i] == u'i'):
                        words[i] = words[i].capitalize()
            ei = 0
            for i in range(len(words)-1, 0, -1):
                if words[i][-1] in [u'.', u'!', u'?']:
                    ei = i+1
                elif words[i][-1] in [u',', u';', u':']:
                    ei = i+1
                    words[i]=words[i].replace(words[i],'.')
                if ei > 0:
                    break
            words = words[:ei]
            sentence = u' '.join(words)
            if sentence != u'':
                error = False
        return exist ,sentence 

        
        """
        gen_word=list()
        max_length=len(self.data)-1
        m=int(random.randrange(3,self.max_Sentence))
        exist=False
        key=random.choice(list(self.data.keys()))
        gen_word=[key[0]]
        gen_word.append(key[1])
        stop=False
        error=False
        min_length = 5 
        pos = 0 
        for i in range(m):
            gen_word.append(random.choice(self.data[key]))
            key=(gen_word[-2],gen_word[-1])
            
            if  gen_word[-1] == "/404" :
                stop = True
                if i<min_length :
                    stop=False
                else:
                    break 
            
        return (stop,gen_word)    """    
        
                
        
    def generate_message(self):
        exist,word=self.generate_sentence()
        while not exist:
            exist,word=self.generate_sentence()
            
        return (exist,word)
        
m=markov()  
    
        
    #dataset_keywords_preprocess.csv    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    