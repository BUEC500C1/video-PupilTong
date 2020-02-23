import pytest 
from TwitterVideoSum import *
import shutil
import importlib
shutil.copy('key','key.py')
from key import *
def test():
    #sample function
    #consumer_key = str(sys.argv[1])
    #consumer_secret = str(sys.argv[2])
    #access_token = str(sys.argv[3])
    #access_token_secret = str(sys.argv[4])
    t = TwitterVideoSum(consumer_key, consumer_secret, access_token, access_token_secret,['cats','dogs'],'.',2)
    t.Start()
    pass