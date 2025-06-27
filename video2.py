import os
import shutil
import re
import subprocess
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip,concatenate_videoclips,TextClip,CompositeVideoClip
from moviepy.video.tools.segmenting import findObjects


Title_vid  = "D:/davinci/Title.mov"
background_video_path = "D:/davinci/backgroundvid.mp4"
# output_path = "OutputVideo/output.mp4"

# helper function
rotMatrix = lambda a: np.array( [[np.cos(a),np.sin(a)], 
                                 [-np.sin(a),np.cos(a)]] )

def vortex(screenpos,i,nletters):
    d = lambda t : 1.0/(0.3+t**8) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t)*rotMatrix(0.5*d(t)*a).dot(v)

def vortexout(screenpos,i,nletters):
    d = lambda t : max(0,t) #damping
    a = i*np.pi/ nletters # angle of the movement
    v = rotMatrix(a).dot([-1,0])
    if i%2 : v[1] = -v[1]
    return lambda t: screenpos+400*d(t-0.1*i)*rotMatrix(-0.2*d(t)*a).dot(v)

def moveLetters(letters, funcpos):
    return [ letter.set_pos(funcpos(letter.screenpos,i,len(letters)))
              for i,letter in enumerate(letters)]

screensize = (1920 ,1080)

from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


## main loop
Title_vid = VideoFileClip(Title_vid)
background_video = VideoFileClip(background_video_path)

folder_path = "D:\\AI\\3tts\\xtts-webui-v1_0-portable\\webui\\output"
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith(".wav"):
            wav_path = os.path.join(root, file)
            print("WAV file:", wav_path)
            audio = AudioFileClip(wav_path)
            #Title
            pattern = r'Chapter\s+(\d+.*)_output'
            match = re.search(pattern, file)
            chapter_name = match.group(0).replace("_output","")
            chapter_name_title = file.replace("_output_new_speaker_name.wav", "")
            print(chapter_name_title)
            # WE CREATE THE TEXT THAT IS GOING TO MOVE, WE CENTER IT.
            txtClip = TextClip(chapter_name,color='white', font="Amiri-Bold",
                            kerning = 5, fontsize=100)
            cvc = CompositeVideoClip( [txtClip.set_pos('center')],
                                    size=screensize)
            # WE USE THE PLUGIN findObjects TO LOCATE AND SEPARATE EACH LETTER
            letters = findObjects(cvc) # a list of ImageClips
            # WE ANIMATE THE LETTERS
            clips = [ CompositeVideoClip( moveLetters(letters,funcpos),
                                        size = screensize).subclip(0,3.25)
                    for funcpos in [vortex] ]
            # WE CONCATENATE EVERYTHING AND WRITE TO A FILE
            final_title = concatenate_videoclips(clips)
            # Overlay the final clip onto the background clip
            title_video_clip = CompositeVideoClip([Title_vid, final_title])
            # Write the resulting video to a file
            ##debugg using save_frame
            #title_video_clip.save_frame("frame.png", t=3)
            title_video_clip.write_videofile("title.mp4")
            ##audio 
            #modify background video to same length as audio
            audio_background = "audio_background.mp4"
            cmd = ['ffmpeg', '-i', background_video_path, '-i', wav_path, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-strict', '-2', '-shortest', audio_background]
            subprocess.run(cmd)
            video2 = audio_background
            video1 = "title.mp4"
            output_file = f"Done\{chapter_name_title}.mp4"
            ## fastest, can't figure out why the second clip doesn't work: cmd = ['ffmpeg', '-f','concat', '-safe', '0', '-i', 'mylist.txt','-c','copy',output_file]
            ## prob works, slow af ffmpeg -i Title.mp4 -i audio_background.mp4 -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mp4     
            ##recodes but works: [ffmpeg -hwaccel cuvid -c:v h264_cuvid -i Title.mp4 -hwaccel cuvid -c:v h264_cuvid -i audio_background.mp4 -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -c:v h264_nvenc -b:v 10M -c:a aac -map "[v]" -map "[a]" output.mp4]
            command = [
                'ffmpeg',
                '-hwaccel', 'cuvid',
                '-c:v', 'h264_cuvid',
                '-i', video1,
                '-hwaccel', 'cuvid',
                '-c:v', 'h264_cuvid',
                '-i', video2,
                '-filter_complex', '[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]',
                '-c:v', 'h264_nvenc',
                '-b:v', '10M',
                '-c:a', 'aac',
                '-map', '[v]',
                '-map', '[a]',
                output_file
            ]
            subprocess.run(command)
            os.remove("title.mp4")
            os.remove("audio_background.mp4")
            audio.close()
            title_video_clip.close()
            ##shutil.move(root,os.path.join("Done",root))
            shutil.move(os.path.join(root,file),os.path.join(os.path.dirname(root),"VideoMade",file))
            #os.remove(os.path.dirname(root))