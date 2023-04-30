import re
import os
from shutil import move
from math import ceil
from gtts import gTTS
from pydub import AudioSegment
from moviepy.editor import AudioFileClip,VideoFileClip,TextClip,concatenate_audioclips,concatenate_videoclips
import cv2
import numpy as np
from io import BytesIO

def remove_spaces(sentence):
    return sentence.strip() != ""


os.chdir('D:\\Users\\Henry\\Downloads\\github\\Learning-Python\\texttomp4') 
folder = "Files"
donefolder = "Done"


screensize = (1920,1080)
# existingfiles = os.listdir()
# #mp3_or_mp4_files = [f for f in existingfiles if f.endswith(".mp3") or f.endswith(".mp4")]
# mp3_or_mp4_files = [f for f in existingfiles if f.endswith(".mp4")] # mp4 files are created last
# i_values = [int(re.search(r"sentence_(\d+)", f).group(1)) for f in mp3_or_mp4_files]
# # find the highest value of i
# if len(i_values) == 0:
highest_i=-1
# else:
#     highest_i = max(i_values)

#debug
filename = os.listdir(folder)[0]


sentencecount = 0
paracount = 0

# Loop through all the text files in the folder
for filename in os.listdir(folder):
    print(filename)
    if filename.endswith(".txt"):
    # Load the text file
        with open(os.path.join(folder,filename), "r", encoding="utf8") as file:
            text = file.read()
        
        # Split the text into sentences based on new line or full stops
        sentences = re.split(r'[.\n]', text)
        sentences = list(filter(None, sentences))
        sentences = list(filter(remove_spaces, sentences))
        
        # Create a list to store the audio and video files
        audio_files = []
        video_files = []
        video_files_paragraph = []
        video_files_intermediate = []
        
        paragraphs = ceil(len(sentences)/10)
        intermediates = ceil(len(sentences)/100)
        
        # Convert each sentence into a text to speech mp3 file and video file
        for i, sentence in enumerate(sentences, 1):
            print(f'Generating {i} out of {len(sentences)}' )
            print(sentence)

            if len(sentence)!=0:
                # Convert the sentence into an mp3 file using gTTS
                tts = gTTS(text=sentence, lang='en')
                try:
                    tts.save(f"sentence_{i}.mp3")
                except:
                    print("try failed")
                    # create 2 seconds of silence
                    silence1 = AudioSegment.silent(duration=2000)

                    # export silence as mp3 file
                    silence1.export(f"sentence_{i}.mp3", format="mp3")

                # Load the mp3 file into a pydub AudioSegment object
                audio = AudioSegment.from_file(f"sentence_{i}.mp3", format="mp3")
                
                # Create a video file with the sentence text
                video = TextClip(sentence, font="Arial", fontsize=48, color='white', method='caption',align='center',size=screensize)
                video = video.set_duration(audio.duration_seconds)
                
                video.write_videofile(f"sentence_{i}.mp4",fps=24, threads = 8)
                
                
                
                video.close()



mp3_files = []
mp4_files = []

for filename in os.listdir():
    if "sentence" in filename:
        if filename.endswith(".mp3"):
            mp3_files.append(filename)
        elif filename.endswith(".mp4"):
            mp4_files.append(filename)
            
mp3_files = sorted(mp3_files, key=lambda x: int(x.split("_")[1].split(".")[0]))
mp4_files = sorted(mp4_files, key=lambda x: int(x.split("_")[1].split(".")[0]))            

# Concatenate mp3 files
mp3_concat_cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'mp3_list.txt', '-c', 'copy', 'audio.mp3']
with open('mp3_list.txt', 'w') as f:
    for file in mp3_files:
        f.write(f"file '{file}'\n")
subprocess.call(mp3_concat_cmd)

# Concatenate mp4 files
mp4_concat_cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'mp4_list.txt', '-c', 'copy', '-shortest', '-movflags', '+faststart', 'video.mp4']
with open('mp4_list.txt', 'w') as f:
    for file in mp4_files:
        f.write(f"file '{file}'\n")
subprocess.call(mp4_concat_cmd)

# Combine audio and video
combine_cmd = ['ffmpeg', '-y', '-i', 'video.mp4', '-i', 'audio.mp3', '-c', 'copy', '-shortest', '-movflags', '+faststart', 'final.mp4']
subprocess.call(combine_cmd)