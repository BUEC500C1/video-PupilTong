import pytest 
from TwitterVideoSum import *
import configparser
def test():
    try:
        open("./key")
        # if key file exist
        conf = configparser.ConfigParser()
        conf.read("./key")    
        consumer_key = conf.get('auth', 'consumer_key')
        consumer_secret = conf.get('auth', 'consumer_secret')
        access_token = conf.get('auth', 'access_token')
        access_token_secret = conf.get('auth', 'access_secret')
        keywords = str(input("input hashtags  u choosed, spilt them with ',': ")).split(',')
        directory = input("input video storage dir: ")
        item = int(input("how many photos do u want: "))
        t = TwitterVideoSum(consumer_key, consumer_secret, access_token, access_token_secret,keywords,directory,item)
        t.Start()
    except:
        # if key file non-exist
        t = TwitterVideoSum("", "", "", "",["test","test"],".",20)
        t.stub_Start()
    
    pass