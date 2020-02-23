from TwitterVideoSum import *
import importlib
import shutil
import sys
if __name__ == "__main__":
    #sample function
    #consumer_key = str(sys.argv[1])
    #consumer_secret = str(sys.argv[2])
    #access_token = str(sys.argv[3])
    #access_token_secret = str(sys.argv[4])
    shutil.copy('key','key.py')
    from key import *
    keywords = str(input("input hashtags  u choosed, spilt them with ',': ")).split(',')
    directory = input("input video storage dir: ")
    item = int(input("how many photos do u want: "))
    t = TwitterVideoSum(consumer_key, consumer_secret, access_token, access_token_secret,keywords,directory,item)
    t.Start()
    pass