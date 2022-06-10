import requests
import urllib.request
import progressbar

pbar=None
def download(url,folder,filename):
    
    if url[-1]=='/':
        url=url.rstrip('/')
        
    Headers={"User-Agent":"PRAW:Link Grabbing bot by u/MetaNotFacebook"}
    response=requests.get(url+".json",headers=Headers)
    Video_Url=response.json()[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    Nsfw_filter=response.json()[0]['data']['children'][0]['data']['over_18']
    if Nsfw_filter is False:
        print(Video_Url)
        urllib.request.urlretrieve(Video_Url, f'{folder}/{filename}.mp4',show_progress) 
        
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
"""
So it looks like reddit wont give you the video and audio together, so thats gonna need combining
video is  (v.reddit/jsdnfkj) URL + DASH_480.mp4?source=fallback
audio is  TRICKIER IT SEEMS 
sometimes (v.reddit/sdujfhd) URl + DASH_audio.mp4    https://v.redd.it/x228x4b25h491/DASH_audio.mp4?source=fallback
othertimes https://v.redd.it/z08avb339n801/audio?source=fallback
maybe other ways too
audio is handled weirdly, but most annoyingly reddit straight up refuses v.redd.it/,,/.json
that just fails
but this method seems to sorta work but resolution is the problem
the url plus the DASH_res i need to guess the resolution ig. not too challenging. start at 1080, try and except to 720,480,\
otherwise continue but there must be a better way than this"""

download('https://www.reddit.com/r/aww/comments/v7x39u/man_stops_to_rescue_kitten_gets_ambushed_by/','Downloads/test','test1')