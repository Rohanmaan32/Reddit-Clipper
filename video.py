import os
from moviepy.editor import *
def Combinator(Vtemp,Atemp,folder,Filename):
    #TEMP to Combined video to new destination
     Video=os.path.abspath(Vtemp)
     Audio=os.path.abspath(Atemp)
     if '_Video.mp4' in Video and '_Audio.mp4' in Audio:
        videoclip = VideoFileClip(Video)
        audioclip = AudioFileClip(Audio)
        final_clip = videoclip.set_audio(audioclip)
        #videoclip.audio = audioclip
        final_clip.write_videofile(filename=folder+Filename,threads=1,codec="libx264")
        videoclip.close()
        audioclip.close()
        os.remove(os.path.abspath(Vtemp))
        os.remove(os.path.abspath(Atemp))
        #shutil.move(src:)
        
        
Combinator('Temp\\mmd44rhdlt891_Video.mp4','Temp\\mmd44rhdlt891_Audio.mp4','Test\\Cute\\',"test.mp4")