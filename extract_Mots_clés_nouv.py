
import pandas as pd
from nltk.corpus import stopwords as stp_nltk
from sklearn.feature_extraction import stop_words as stp_sk
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
import preprocessor as p
import re
from nltk.corpus import wordnet,words
from os import path



def load_docs_keywords_traiter(csvpath=None):
    df_all=pd.DataFrame(index=None, columns=['text'], dtype=None, copy=False)
    if path.exists(csvpath) :# c'est que le prétraitement est déja fait ! 
        df_all = pd.read_csv(csvpath,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["text"])
        
    else : 
        # read json into a datafram
        paths=["data/trumptweets1205_127.csv","data/2017_01_28_trump_tweets.csv","data/2016_12_05_trumptwitterall.csv","data/gotTwitter.csv"]
        # print schema
        typedata=["trump","trump","trump","got"]
        df_all=LoadData(paths,typedata)
        df_all.to_csv(path_or_buf=csvpath, sep=',')
        
    return df_all
    


def pre_process_tweets(text):
    
    # lowercase
    print("avant traitement tweet")
    print(text)
    text=text.lower()
        #remove hashtags !! pour les tweets ! 
    p.set_options(p.OPT.URL,p.OPT.MENTION,p.OPT.HASHTAG)
    text= "".join(p.clean(text))
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    words_text=text.split()
    resultat=""
    for w in words_text :
        if  w not in words.words(): #ce n'est pas un mot anglais 
            w = re.sub(r'([a-z])\1+', r'\1' , w) # donc on enléve les caractére redondant ! 
            print(w)
        resultat = resultat + " "+ w
    print("aprés traitement tweet")   
    print(resultat)
    
    return resultat
    
def pre_process_stacks(text):
    print("avant traitement stack ")
    print(text)
   
    text=text.lower()
    #remove tags
    text=re.sub("</?.*?>"," <> ",text)
    #remove hashtags !! pour les tweets ! 
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    print("aprés traitement stack ")
    print(text)
    
    return text


def LoadData(paths,typedata):
    
    df_idf=pd.read_json("data/stackoverflow-data-idf.json",lines=True)
    df_all=pd.DataFrame(index=None, columns=['text'], dtype=None, copy=False)
    df_all['text']= df_idf['title'] + df_idf['body'] # de stackoverflow ! 
    df_all['text'] = df_all['text'].apply(lambda x:pre_process_stacks(x))
    df_all['text']=df_all['text'].to_frame()
    # tweets !! 
    i=0
    for path in paths :
        if typedata[i] == "got":
            df_temps=pd.read_csv(path,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["text"])
            df_temps['text'] = df_temps['text'].apply(lambda x:pre_process_tweets(x))
        else : 
            df_temps=pd.read_csv(path,engine="python",error_bad_lines=False, index_col=None,sep=',',usecols =["tweet"])
            df_temps['tweet'] = df_temps['tweet'].apply(lambda x:pre_process_tweets(x))
        if typedata[i] != "got" : 
            df_temps['text']=df_temps['tweet']
        
        df_all=pd.concat([df_all, df_temps])
        i=i+1
    
    return df_all 

	
from sklearn.feature_extraction.text import CountVectorizer
import re

# sa c 'est pour avoir les stop words  qui sont les plus utilisé comme the , your , ... '
def get_stop_words(stop_file_path):
    """load stop words """
    
    with open(stop_file_path, 'r', encoding="utf-8") as f:
        stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        stop_words=frozenset(stop_set).union(set(stp_nltk.words("english"))).union(stp_sk.ENGLISH_STOP_WORDS)
        
    return stop_words

		
'''		
def ConstruireLeVocabulaire():
    #load a set of stop words
	df_idf=load_docs_keywords_traiter("data/dataset_keywords_preprocess")
    stopwords=get_stop_words("ressources/stopwords.txt")
    print(len(stopwords))
    #get the text column  dans une liste  
    docs=df_idf['text'].tolist()

    #create a vocabulary of words, 
    #ignore words that appear in 85% of documents, 
    #eliminate stop words

   
    cv=CountVectorizer(max_df=0.85,stop_words=stopwords,max_features=30000)
    word_count_vector=cv.fit_transform(docs)
    #c est une matrice ou chaque element représente l 'aapparence du mot j dans le doc i ou le post i !! 
    
    return cv,word_count_vector
# 20000 lignes donc post et 125278 mots 


# In[ ]:




def Fit_The_TFIDF(word_count_vector):
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    #store the content
    with open("tfidf_transformer_stack.pkl", 'wb') as handle:
        pickle.dump(tfidf_transformer, handle)
    return tfidf_transformer
tfidf_transformer=Fit_The_TFIDF(word_count_vector)


# In[ ]:


# read test docs into a dataframe and concatenate title and body
def readTestDoc():
    df_test=pd.read_json("data/stackoverflow-test.json",lines=True)
    df_test['text'] = df_test['title'] + df_test['body']
    df_test['text'] =df_test['text'].apply(lambda x:pre_process(x))

    # get test docs into a list
    docs_test=df_test['text'].tolist()
    docs_title=df_test['title'].tolist()
    docs_body=df_test['body'].tolist()
    docs_test[0]
    


# In[ ]:


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    for idx, score in sorted_items:
        fname = feature_names[idx]
        
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    #results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]
    
    return results


# In[ ]:


def TF_IDF():
    cv,word_vector=ConstruireLeVocabulaire()
    tfidf_transformer = pickle.load(open("tfidf_transformer_stack.pkl", "rb" ) )
    #tous les mots de  notre vocabulaire ! 
    feature_names=cv.get_feature_names()  
    return feature_names,tfidf_transformer



def getKeyWords(doc): 
	feature_names,tfidf_transformer=TF_IDF()
    # la phrase souhaitant avoir ses mots clés  ! 
    #doc = docs_title[8]
    #generate tf-idf for the given document
    tf_idf_vector=tfidf_transformer.transform(cv.transform([doc]))

    #sort the tf-idf vectors by descending order of scores
    sorted_items=sort_coo(tf_idf_vector.tocoo())

    #extract only the top n; n here is 10
    keywords=extract_topn_from_vector(feature_names,sorted_items,10)
    return keywords
	

#getKeyWords("Trump")
'''

df_idf=load_docs_keywords_traiter("data/dataset_keywords_preprocess") 
print(df_idf)
