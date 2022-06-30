# %%
#import Subreddit_lists
import praw
import Api_ID
import logging
import requests
import progressbar
import urllib
from moviepy.editor import *
import os
import shutil


# %%
reddit = praw.Reddit(
    client_id=Api_ID.App_id,
    client_secret=Api_ID.Secret,
    password="Zuccjuicer",
    user_agent="PRAW:Link Grabbing bot by u/MetaNotFacebook",
    username="MetaNotFacebook",
)

# %%
Cute=[
'aww',
'cats',
'animalsbeingjerks',
'animalsbeingbros',
'Awwducational',
'dogs',
'corgi',
'thisismylifenow',
'blep',
'eyebleach',
'tippytaps',
'awww',
'babycorgis',
'rarepuppers'
]
Unexpected=["Unexpected"]
People_positive=[
"HumansBeingBros",
"MadeMeSmile",
"ContagiousLaughter",
"nonononoyes"
]
People_negative=[
"Whatcouldgowrong",
"WatchPeopleDieInside",
"Instant_regret"
"IdiotsInCars"
]
Misc=[
"WoahDude",
"Interestingasfuck",
"Damnthatsinteresting",
"OddlySatisfying"

]
Funny=["funny","ContagiousLaughter"]
Subreddits={'Cute':Cute,'Unexpected':Unexpected,'People_negative':People_negative,
            'People_positive':People_positive,"Misc":Misc,"Funny":Funny}


# %% [markdown]
# So it looks like reddit wont give you the video and audio together, so thats gonna need combining
# video is  (v.reddit/jsdnfkj) URL + DASH_480.mp4?source=fallback
# 
# UPDATE - got it to work, requests.head... whatever that does but allowing redirects and copying redirected url to a variable.
# 
# 
# 
# Audio is  TRICKIER IT SEEMS 
# sometimes (v.reddit/sdujfhd) URl + DASH_audio.mp4    https://v.redd.it/x228x4b25h491/DASH_audio.mp4?source=fallback
# othertimes https://v.redd.it/z08avb339n801/audio?source=fallback
# maybe other ways too
# audio is handled weirdly, but most annoyingly reddit straight up refuses v.redd.it/,,/.json
# that just fails
# but this method seems to sorta work but resolution is the problem
# the url plus the DASH_res i need to guess the resolution ig. not too challenging. start at 1080, try and except to 720,480,
# otherwise continue but there must be a better way than this

# %%
#NOT MY CODE got from stackoverflow
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None        

# %%
pbar=None

def download(url,folder,Filename):
 #try:    
    short_url = url
    orig_url = requests.head(short_url, allow_redirects=True)
    url=orig_url.url
    
    #VIDEO URL auto gets the best quality uploaded
    if url[-1]=='/':  #dk if this is necessary just trims the last / from url before a .json is concatenated
        url=url.rstrip('/')
        
    Headers={"User-Agent":"PRAW:Link Grabbing bot by u/MetaNotFacebook"}
    response=requests.get(url+".json",headers=Headers)
    Video_Url=response.json()[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    Nsfw_filter=response.json()[0]['data']['children'][0]['data']['over_18']
    
    if Nsfw_filter is False:
        
        Vtemp="temp/" + Filename +'_Video.mp4'
        Atemp="temp/" + Filename +'_Audio.mp4'
        print("Video Start")
        urllib.request.urlretrieve(url=Video_Url,reporthook= show_progress,filename=Vtemp)
        print("Video done")
        
    #AUDIO URL is a slight modification of the base v.redd.it but seems to have some variations to it
        try:
            print("A1")
            Audio_Url=short_url+'/DASH_audio.mp4?source=fallback'
            #print(Audio_Url)
            urllib.request.urlretrieve(url =Audio_Url,reporthook = show_progress,filename=Atemp)
            print("A1 Audio Done")
            Combinator(Vtemp,Atemp,folder,Filename)  
            return(0)
        except Exception as e:
            try:
                print("A2")
                Audio_Url=short_url+'/audio?source=fallback'
                urllib.request.urlretrieve(url =Audio_Url,reporthook = show_progress,filename=Atemp)
                print("A2 Audio Done")
                Combinator(Vtemp,Atemp,folder,Filename)  
                return(0)  
            except Exception as e:
                print("A2 Errorred")
                print(e)
                os.remove(os.path.abspath(Vtemp))

# %%
def Combinator(Vtemp,Atemp,folder,Filename):
    #TEMP to Combined video to new destination
     Video=os.path.abspath(Vtemp)
     Audio=os.path.abspath(Atemp)
     if '_Video.mp4' in Video and '_Audio.mp4' in Audio:
        videoclip = VideoFileClip(Video)
        audioclip = AudioFileClip(Audio)
        #print("clips")
        final_clip = videoclip.set_audio(audioclip)
        #print("audio")
        #videoclip.audio = audioclip
        final_clip.write_videofile(filename=folder+Filename,threads=1,codec="libx264")
        #print("file writing")
        videoclip.close()
        #print("close vid")
        audioclip.close()
        #print("close audio")
        os.remove(os.path.abspath(Vtemp))
        #print("del vid")
        os.remove(os.path.abspath(Atemp))
        #print("del aud")
        #shutil.move(src:)

# %%
#download("https://v.redd.it/g039fxsqzl491","downloads/Cute/",Filename="test")

# %%
def RetrieveAndDownload(SubredditDictionary:dict):
    for key,value in SubredditDictionary.items():
        for k in value:# k is subreddit name
            logging.info(f"Current Subreddit {k}")
            for j in reddit.subreddit(k).hot(limit=3):
                if j.url[8].lower()=='v':
                    url_base36=j.url[18:31]
                    print(url_base36)
                    logging.info(f"Currently Downloading {key}")
                    #i had mis spelled downloads as donwloads here, in the folder param..took right about 2 hrs of searching to find this tiny dumb mistake
                    try:
                        download(url=j.url,folder=f"Downloads/{key}/",Filename=f"{url_base36}.mp4")
                    except Exception as e:
                        print(e)
                        continue
                    with open("testDownloads.txt",'a') as f:
                        f.write(j.url)
                    logging.info("Download Complete")
                    


# %%
RetrieveAndDownload(Subreddits)


