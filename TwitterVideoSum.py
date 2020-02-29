from ffmpegQueue import *
import tweepy
import threading 
import time
import json
class TwitterVideoSum:
    __auth = None        
    __keywords = tuple()
    __directory = str()
    __item = 0
    __count = 0
    __progress = 0
    def __init__(self, consumer_key:str, consumer_secret:str, access_token:str, access_token_secret:str,keywords:tuple,directory:str, item:int = 10):
        try:
            self.__auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.__auth.set_access_token(access_token, access_token_secret)
            self.__keywords = keywords
            self.__directory = directory
            self.__item = item
            self.__videoApi = None
            self.__count = len(self.__keywords)
            self.__queueCounter = 0
        except:
            print("AN error occured!")
            pass
        finally:
            pass
    def stub_Start(self):
        threading.Thread(target=self.GUI, args=()).start()
        self.__videoApi = VideoApi()
        with open("tweets_stub.json","r") as f:
            savedInfos = json.loads(f.read())
            for savedInfo in savedInfos:
                qitem = queueItem(self.__directory,tuple(savedInfo["keywordsTweetsText"]),tuple(savedInfo["keywordsTweetsImgs"]),self.CallbackHandler,savedInfo["keyword"])
                while(self.__queueCounter>4):
                    pass
                self.__videoApi.AddTask(qitem)
                self.__queueCounter = self.__queueCounter + 1

        return 0
        pass
    def Start(self):
        threading.Thread(target=self.GUI, args=()).start()

        api = tweepy.API(self.__auth)
        self.__videoApi = VideoApi()
        save = []
        for keyword in self.__keywords:
            #tweets = tweepy.Cursor(api.search, q="#" + str(keyword),count = self.__item,result_type="recent",).items(self.__item)
            tweets = tweepy.Cursor(api.search, q="%23" + str(keyword),count = 50).items()
            i=0
            keywordsTweetsText=list()
            keywordsTweetsImgs = list()
            for tweet in tweets:
                imglist = list()
                if(hasattr(tweet,'extended_entities')):
                    for media in tweet.extended_entities['media']:
                        if(media['type'] == 'photo'):
                            imglist.append(media['media_url_https'])
                            keywordsTweetsImgs.append(tuple(imglist))
                            keywordsTweetsText.append(tweet.text)
                            i = i+1
                if(i>self.__item):
                    break
            #saveitem={}
            #saveitem["keywordsTweetsText"] = tuple(keywordsTweetsText)
            #saveitem["keywordsTweetsImgs"] = tuple(keywordsTweetsImgs)
            #saveitem["keyword"]=keyword
            #save.append(saveitem)
            qitem = queueItem(self.__directory,tuple(keywordsTweetsText),tuple(keywordsTweetsImgs),self.CallbackHandler,keyword)
            while(self.__queueCounter>4):
                pass
            self.__videoApi.AddTask(qitem)
            self.__queueCounter = self.__queueCounter + 1
            
        #with open("tweets_stub.json","w") as f:
        #    f.write(json.dumps(save))
        return 0

    def CallbackHandler(self):
        self.__count = self.__count - 1
        self.____queueCounter = self.__queueCounter - 1
    def GUI(self):
        while(self.__count!=0):
            print("Current progress:" + str(len(self.__keywords) - self.__count + 1) + "/" + str(len(self.__keywords)) + " | Current Keywords: ", end = '')
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


                