import ffmpeg
import threading 
import uuid as uuidTools
import os
import requests
import shutil
import subprocess 

class queueItem:
    __status__ : int = 0
    keyword:str = ""
    directory :str = ""        
    callback = None
    img = tuple()
    text:str = ""
    def __init__(self,directory,text:tuple, img:tuple, callback,keyword:str):
        self.directory = directory
        self.callback = callback
        self.img = img
        self.text = text
        self.keyword = keyword
        pass
    def SetStatusStarted(self):
        self.__status__ = 1
    def SetStatusFinished(self):
        self.__status__ = 100
        if(self.callback!=None):
            self.callback()
class VideoApi:
    __queueTaskUuid = list()
    __queue = dict()
    __currentTaskLock = threading.Lock()
    __currentUuid :str =""
    def AddTask(self,item : queueItem) -> str:
        uuid:str = str(uuidTools.uuid4())
        #use a unique uuid to index every task
        self.__queueTaskUuid.append(uuid)
        self.__queue[uuid] = item
        threading.Thread(target=self.__Process__, args=(uuid,)).start()
        return uuid
    def CheckStatus(self,uuis:str) -> list:
        # 0 - unstart
        # 1~99 - processing
        # 100 - finished
        # -1 - deleted
        uuid = self.__currentUuid
        if uuid not in self.__queue:
            return [-1, - 1, "[deleted]"]
        return [self.__queue[uuid].__status__ , len(self.__queue[uuid].text), self.__queue[uuid].keyword]
        #[index,max,keyword]
    def __Process__(self,uuid:str) :
        self.__currentTaskLock.acquire()
        #lock
        currentItem = self.__queue[uuid]
        currentItem.SetStatusStarted()
        self.__currentUuid = uuid
        try:
            shutil.rmtree(currentItem.directory + "/" + currentItem.keyword)
        except:# not exist
            pass
        try:
            os.remove(currentItem.directory + "/" + currentItem.keyword + ".mp4")
        except:# not exist
            pass
        os.makedirs(currentItem.directory + "/" + currentItem.keyword ,exist_ok=True)
        subprocess.run("ffmpeg  -f lavfi  -i color=c=black:s=1280x720   -crf 25 -pix_fmt yuv420p -t 0.01 " + currentItem.directory + "/" + currentItem.keyword + "/sum.ts",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        for i in range(len(currentItem.text)):
            self.__downloadAndConvertToImage(i,currentItem,uuid)
            self.__queue[uuid].__status__ = int(i/ len(currentItem.text) * 100)
        subprocess.run("ffmpeg -i " + currentItem.directory + "/" + currentItem.keyword + "/sum.ts" +" -vcodec libx264 -crf 25 -pix_fmt yuv420p " +  currentItem.directory + "/" + currentItem.keyword + ".mp4",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        shutil.rmtree(currentItem.directory + "/" + currentItem.keyword)
        self.__queue[uuid].SetStatusFinished()
        self.__queue.pop(uuid)
        #self.__currentUuid = ""

        self.__currentTaskLock.release()
        #unlock
        pass
    def __downloadAndConvertToImage(self,index:int,currentItem:queueItem,uuid:str):
        directory = currentItem.directory
        imgUrl = currentItem.img[index][0]
        text = currentItem.text[index]
        text = text[0:text.find("http")]
        text = text.replace("'","")
        for i in range(0,len(text),30):
            text = text[0:i] + "\n" + text[i:]
        keyword = currentItem.keyword
        filename =  str(index)
        #got this code from https://stackoverflow.com/questions/30229231/python-save-image-from-url/30229298
        with open(directory + "/"+keyword+"/" + filename, 'wb') as handle:
            response = requests.get(imgUrl, stream=True)
            if not response.ok:
                raise Exception("connection Error!")

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

            handle.close()
        subprocess.run("ffmpeg -i " + directory + "/"+keyword+"/" + filename +" -vf \"scale=1280:720,drawtext=text=\'" +text + "\':fontcolor=blue:fontsize=40:x=10:y=20:\" " + directory + "/"+keyword+"/" +  filename + ".png",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        subprocess.run("ffmpeg -loop 1 -s 1280x720 -t 3 -i " + directory + "/"+keyword+"/" + filename +".png -pix_fmt yuv420p " + directory + "/"+keyword+"/" + filename +".ts",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        subprocess.run("ffmpeg -i \"concat:"+ directory + "/"+keyword+"/" + "sum.ts|" + directory + "/"+keyword+"/" + filename +".ts\" -y -c copy "+ directory + "/"+keyword+"/" + "sum_temp.ts",stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,shell=True)
        os.rename(directory + "/"+keyword+"/" + "sum_temp.ts",directory + "/"+keyword+"/" + "sum.ts")
        
        
        #os.remove(directory+"/" + filename)

    
    