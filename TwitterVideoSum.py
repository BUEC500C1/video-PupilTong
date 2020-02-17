from ffmpegQueue import *
import tweepy
import threading 
import time
class TwitterVideoSum:
    __auth = None        
    __keywords = tuple()
    __directory = str()
    __item = 0
    __count = 0
    __progress = 0
    def __init__(self, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str,keywords:tuple,directory:str, item:int = 10):
        self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.__auth.set_access_token(access_token, access_token_secret)
        self.__keywords = keywords
        self.__directory = directory
        self.__item = item
        self.__videoApi = None
        self.__count = len(self.__keywords)
        pass
    def Start(self):
        threading.Thread(target=self.GUI, args=()).start()

        api = tweepy.API(self.__auth)
        self.__videoApi = VideoApi()
        for keyword in self.__keywords:
            #tweets = tweepy.Cursor(api.search, q="#" + str(keyword),count = self.__item,result_type="recent",).items(self.__item)
            tweets = tweepy.Cursor(api.search, q="%23" + str(keyword),count = 50,result_type="recent").items()
            i=0
            keywordsTweetsText=list()
            keywordsTweetsImgs = list()
            for tweet in tweets:
                imglist = list()
                if( hasattr(tweet,'extended_entities')):
                    for media in tweet.extended_entities['media']:
                        if(media['type'] == 'photo'):
                            imglist.append(media['media_url_https'])
                            keywordsTweetsImgs.append(tuple(imglist))
                            keywordsTweetsText.append(tweet.text)
                            i = i+1
                if(i==self.__item):
                    break
            qitem = queueItem(self.__directory,tuple(keywordsTweetsText),tuple(keywordsTweetsImgs),self.CallbackHandler,keyword)
            self.__videoApi.AddTask(qitem)
    def CallbackHandler(self):
        self.__count = self.__count - 1
    def GUI(self):
        while(self.__count!=0):
            print("Current progress:" + str(len(self.__keywords) - self.__count) + "/" + str(len(self.__keywords)) + " | Current Keywords: ", end = '')
            if(self.__videoApi!=None):
                status = self.__videoApi.CheckStatus()
                if(status[0]!= -1 ):
                    print(status[2] + "|", end='')
                    for i in range (20):
                        if(status[0]/5-i>0):
                            print("#",end='')
                        else:
                            print(" ",end='')
                    print("| " + str(status[0]) + "%",end='')
            print("",end='\r')
            time.sleep(0.1)
        print()
        print("Completed!")


                