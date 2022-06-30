#params={"subreddit":"aww"}
#req=requests.get("https://api.pushshift.io/reddit/subreddit/search",headers=params)
#print(req.content)

def RetrieveAndDownload(SubredditList):
    fails=0
    for i in SubredditList:
        for j in reddit.subreddit(i).hot(limit=10000):
            if j.url[8].lower()=='v':
                #print(j.url[18:31])
            pass