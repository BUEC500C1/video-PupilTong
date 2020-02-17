# Twitter hashtag photo video summary generator
## Example Code
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
## Module TwitterVideoSum.py
### Architechture
This module is able to pull tweets from twitter with provided parmeters and prepare data for Module ffmpegQueue
