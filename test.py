#import os
#size=0
#for path, dirs, files in os.walk('Downloads\\'):
#                for f in files:
#                    fp = os.path.join(path, f)
#                    size += os.path.getsize(fp)
#print(size)

#Subreddits={'Cute':'Cute','Unexpected':'Unexpected','People_negative':'People_negative',
#            'People_positive':'People_positive',"Misc":'Misc',"Funny":'Funny'}
#for key,value in Subreddits.items():
#        for k in value:# k is subreddit name
#            print(k)

import logging
logging.basicConfig(level=logging.DEBUG)
logging.info("hi")