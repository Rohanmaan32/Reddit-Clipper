import requests
import urllib.request
import progressbar

pbar=None
def download(url,folder):
    
    if url[-1]=='/':
        url=url.rstrip('/')
        
    Headers={"User-Agent":"PRAW:Link Grabbing bot by u/MetaNotFacebook"}
    response=requests.get(url+".json",headers=Headers)
    Video_Url=response.json()[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
    Nsfw_filter=response.json()[0]['data']['children'][0]['data']['over_18']
    if Nsfw_filter is False:
        print(Video_Url)
        urllib.request.urlretrieve(Video_Url, f'Downloads/{folder}/File.mp4',show_progress) 
        
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
#download('https://www.reddit.com/r/Funnymemes/comments/usuw7b/exactly/')