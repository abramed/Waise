#!/usr/bin/env python
# coding: utf-8

# In[4]:


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy 
from markovstruct import markov
# thread 
from threading import Thread
import threading 
import time
from multiprocessing import Process, freeze_support
from tweepy import Stream
from tweepy.streaming import StreamListener
import json 
import extract_Mots_clés as keyword

class StreamerTweet():
    """
    pour connexion et recolte tweet 
    """
    def Streamtweet(self, cons_key,cons_secret,access_token,access_token_secret):
        try:
            auth = OAuthHandler(cons_key,cons_secret)
            auth.set_access_token(access_token,access_token_secret)
            return auth
        except Exception as e :
            return none
        
   


class ListnerTwitter(StreamListener,Thread):
    
    auto_tweet_bool=False
        # Consumer Key (API Key)
    cons_key ='xxxxxxxxxxxxxxxxxxxxxxxx'

        # Consumer Secret (API Secret)
    cons_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # Access Token
    access_token = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

        # Access Token Secret
    access_token_secret = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    auth=None
    api=None
   
    def connection(self) :
        connexion=StreamerTweet()
        self.auth=connexion.Streamtweet(cons_key=self.cons_key,cons_secret=self.cons_secret,access_token=self.access_token,access_token_secret=self.access_token_secret)
        self.api= tweepy.API(self.auth) 
    

    def on_error (self, status):
         print(status)
        
    ####### training 
    markov=markov()
    markov.creationchaine('dataset_chatbot_processed.csv')
    ########generation d'un tweet 
    def tweeter(self,seed=None):
        self.connection() 
        exist,tweet=self.markov.generate_sentence(seed)
        tweet=tweet+'#itdoesntwork'
        try:
            self.api.update_status(tweet)
        except tweepy.TweepError as error:
            pass
        return tweet
    
    def tweet_for(self,freq=5,seed=None) :
        while(True):
            tweet=self.tweeter(seed)
            print(tweet)
            time.sleep(freq)
        
    def respond_tweet(self)  :
        since_id=1214683218466746368
        while True :
            for tweet in tweepy.Cursor(self.api.mentions_timeline,
                since_id=since_id).items():
                since_id=max(tweet.id,since_id)
                text=tweet.text
                dicts=keyword.getKeyWordsFromPhrase(text)
                seed=list(dicts.keys())
                exist,tweetgen=self.markov.generate_sentence(seed)
                print(seed)
                try:
                    self.api.update_status(
                        status=tweetgen,
                        in_reply_to_status_id=tweet.id)
                    print(since_id)
                except tweepy.TweepError as error:
                    pass  
        print(since_id)
        time.sleep(60*3)
        
        
    def auto_tweet(self,dure=60*60,freq=5,seed=None):
        freeze_support()
        p1=Process(target=self.tweet_for,args=(freq,seed))
        print("start tweeting ")
        p1.start()
        time.sleep(dure)
        print("stop tweeting")
        p1.kill()
        
        
    def auto_respond (self,dure=40):
        freeze_support()
        p1=Process(target=self.respond_tweet)
        print("start tweeting ")
        p1.start()
        time.sleep(dure)
        print("stop tweeting")
        p1.kill()
   
        
        
#class threadtwitter(Thread)
        
        
if __name__ == '__main__':  
    duree=7 * 24 * 60 * 60
    freq=60*60*24
    seed="dream"
    tweeter=ListnerTwitter()    
    tweeter.connection()
   # dm=tweeter.direct_messages()
    #print(dm)
    #twitterStream = Stream(tweeter.auth, ListnerTwitter())
    #iterator =twitterStream.filter(track=["#itdoesntwork"])
    tweeter.auto_respond()
    
    
    
    #tweeter.tweeter('dream')
    #tweeter.auto_tweet(seed=seed)
    
   
    

# In[ ]:





# In[ ]:




