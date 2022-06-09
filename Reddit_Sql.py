import Api_ID
import praw
import mysql.connector as ms

reddit = praw.Reddit(
    client_id=Api_ID.App_id,
    client_secret=Api_ID.Secret,
    password="Zuccjuicer",
    user_agent="PRAW:Link Grabbing bot by u/MetaNotFacebook",
    username="MetaNotFacebook",
)

#params={"subreddit":"aww"}
#req=requests.get("https://api.pushshift.io/reddit/subreddit/search",headers=params)
#print(req.content)



mydb=ms.connect(host="localhost",user="root",passwd="1111",database="reddit")
if mydb.is_connected():
    print("Successfully connected")
else:
    print("Not connected")
cr=mydb.cursor()
#give a list of subreddits to take all videos and push to a
def RetrieveAndSqlInsert(SubredditList):
    fails=0
    for i in SubredditList:
        for j in reddit.subreddit(i).hot(limit=10000):
            if j.url[8].lower()=='v':
                #print(j.url[18:31])
                try:
                    cr.execute(f'insert into list1 values("{j.url[18:31]}","{SubredditList}");')
                    mydb.commit()
                except Exception as e:
                    print(e)
                    fails+=1
                    if fails>50:
                       break 
                    else:
                        continue
        if fails>50:
            break
    print(f"SQL ENTRY DONE with {fails} fails")
RetrieveAndSqlInsert(["Damnthatsinteresting"])