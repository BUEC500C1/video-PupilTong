from TwitterVideoSum import *
import sys
import configparser
if __name__ == "__main__":
    #sample function
    #consumer_key = str(sys.argv[1])
    #consumer_secret = str(sys.argv[2])
    #access_token = str(sys.argv[3])
    #access_token_secret = str(sys.argv[4])
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
        assert t.Start() == 0
    except:
        # if key file non-exist
        t = TwitterVideoSum("", "", "", "",["test","test"],".",20)
        assert t.stub_Start() ==0
    pass