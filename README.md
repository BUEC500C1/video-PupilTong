# Twitter hashtag photo video summary generator
## requirement
python > 3.5
## Deployment Guide
### Environment Configuration
```bash
git clone https://github.com/BUEC500C1/video-PupilTong.git
cd video-PupilTong
pip3 -r requirements.txt
python3 Sample.py
```
### import your own Twitter API key info
Keys should be stores as global varibles like this:
```python
consumer_key:str = ""
consumer_secret:str = ""
access_token:str = ""
access_token_secret:str = ""
```
We recommond you store it in a python file and import it in the Sample.py, like this:
```python
from key import *
```
### Run sample program
The program will ask you a series parmaters, an example is given as follow:
```bash
input hashtags  u choosed, spilt them with ',': cats,dogs
input video storage dir: .
how many photos do u want: 10
```
This means we are trying to search 10 tweets which is attached at least one photo for each hashtag, "#cats" or "#dogs, and tell the program where to store the summary video.
### Gui shows progress
on programm running, you may see something like this:
```bash
Current progress:2/2 | Current Keywords: dogs|################    | 90%
```
This means our program now is processing the 2nd hashtag, dogs, you gave, and it has finished 90% of whole workload.
## Module ffmpegQueue.py
This module is able to convert a tuple of texts and a tuple of images' url to a summary video.
### Architechture
 ![Architechture](/photos/queue_arch.png)
### Class queueItem
One task of the work load pool
#### Constructor Parameters
| Name  | Description | type |
| ------------- | ------------- | ------------- |
| directory  | Output video storage directory  | str |
| text  | List of texts  | tuple  |
| img  | Images list for each text. Program will use the first as the background  | tuple  |
| keyword  | keyword of this task, will use this to create a temp directory. Program will try to delete the directory first  | str  |
### Class VideoApi
video processing core
#### Method AddTask
| Name  | Description | type |
| ------------- | ------------- | ------------- |
| item  | the task to be added to the workload pool  | ququeItem |
##### return
return a unique uuid of this task.
#### Method CheckStatus
| Name  | Description | type |
| ------------- | ------------- | ------------- |
| uuid  | check the status of a specificaed task by uuid   | str |
##### return
type: int
```python
# 0 - unstart
# 1~99 - processing
# 100 - finished
# -1 - deleted
```
## Module TwitterVideoSum.py
This module is able to pull tweets from twitter with provided parmeters and prepare data for Module ffmpegQueue
### Architechture
 ![Architechture](/photos/tws_arch.png)
### Class TwitterVideoSum:
#### Constructor
| Name  | Description | type |
| ------------- | ------------- | ------------- |
| consumer_key  | twitter api key  | str |
| consumer_secret  | twitter api key  | str |
| access_token  | twitter api key  | str |
| access_token_secret  | twitter api key  | str |
| keywords  | List of hashtags  | tuple  |
| directory  | video storage directory  | str  |
| item  | number of photos for each hashtag to be converted  | str  |
#### Method Start
Start the process
