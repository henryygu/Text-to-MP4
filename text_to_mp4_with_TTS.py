import re
import os
from shutil import move
from math import ceil
import subprocess
#from gtts import gTTS
from moviepy.editor import (
    TextClip,
)
import logging
from TTS.api import TTS
from tqdm import tqdm

logging.basicConfig(level=logging.WARNING)

def remove_spaces(sentence):
    return sentence.strip() != ""


os.chdir("D:\\Users\\Henry\\Downloads\\github\\Learning-Python\\texttomp4")

folder = "Files"
donefolder = "Done"


screensize = (1920, 1080)
existingfiles = os.listdir()
# #mp3_or_mp4_files = [f for f in existingfiles if f.endswith(".mp3") or f.endswith(".mp4")]
mp4_files = [f for f in existingfiles if f.endswith(".mp4")] # mp4 files are created last
filtered_list = [item for item in mp4_files if 'sentence_merge' in item]
numbers = [int(re.search(r'\d+', item).group()) for item in filtered_list]
# i_values = [int(re.search(r"sentence_merge_(\d+)", f).group(0)) for f in mp4_files]
# # find the highest value of i
if len(numbers) == 0:
    highest_i = -1
else:
    highest_i = max(numbers)

# debug
# filename = os.listdir(folder)[0]


def get_number(filename):
    return int(re.search(r'\d+', filename).group())

model_name = TTS.list_models()[7]
tts = TTS(model_name)

sentencecount = 0
paracount = 0

# Loop through all the text files in the folder
for filename in os.listdir(folder):
    #print(filename)
    if len(numbers) == 0:
        highest_i = -1
    else:
        highest_i = max(numbers)
    if filename.endswith(".txt"):
        # Load the text file
        with open(os.path.join(folder, filename), "r", encoding="utf8") as file:
            text = file.read()
        # Split the text into sentences based on new line or full stops
        sentences = re.split(r"[.\n]", text)
        sentences = list(filter(None, sentences))
        sentences = list(filter(remove_spaces, sentences))
        # Create a list to store the audio and video files
        audio_files = []
        video_files = []
        video_files_paragraph = []
        video_files_intermediate = []
        paragraphs = ceil(len(sentences) / 10)
        intermediates = ceil(len(sentences) / 100)
        # Convert each sentence into a text to speech mp3 file and video file
        print(filename)
        for i, sentence in enumerate(sentences, 1):
            #print(f"Generating {i} out of {len(sentences)}")
            #print(sentence)
            if i > highest_i:
                if len(sentence) != 0:
                    # Convert the sentence into an mp3 file using gTTS
                    try:
                        tts.tts_to_file(text=sentence, file_path=f"sentence_{i}.mp3")
                    except:
                        # #print("try failed")
                        # create 2 seconds of silence
                        cmd_1 = f'ffmpeg -y -hide_banner -loglevel error -f lavfi -i anullsrc=r=44100:cl=mono -t 2 -q:a 9 -acodec libmp3lame sentence_{i}.mp3'
                        subprocess.call(cmd_1,shell=True)
                
                    # Create a video file with the sentence text
                    video = TextClip(
                        sentence,
                        font="Arial",
                        fontsize=48,
                        color="white",
                        bg_color="black",  # Add a black background color
                        method="caption",
                        align="center",
                        size=screensize,
                    )
                    video.save_frame(f"frame_{i}.png", t=1)
                    #print(f"Appending Sentence {i} out of {len(sentences)}")
                    sentence_cmd = f'ffmpeg -y -hide_banner -loglevel error -loop 1 -i frame_{i}.png -i sentence_{i}.mp3 -c:v libx264 -preset medium -tune stillimage -crf 18 -c:a aac -shortest sentence_merge_{i}.mp4'
                    subprocess.call(sentence_cmd,shell=True)
                    try:
                        os.remove(f"sentence_{i}.mp3")
                        os.remove(f"frame_{i}.png")
                    except:
                        print(i)
        mp4_files = []
        for filename_1 in os.listdir():
            if "sentence_merge_" in filename_1:
                if filename_1.endswith(".mp4"):
                    mp4_files.append(filename_1)          
        mp4_files_sorted = sorted_list = sorted(mp4_files, key=get_number)
        with open('list.txt', 'w') as f:
            for file in mp4_files_sorted:
                f.write(f"file '{file}'\n")
        # Run the ffmpeg command with Nvidia GPU acceleration
        # command = f'ffmpeg -hwaccel_output_format cuda -i "concat:{files}" -c:v h264_nvenc -preset fast -movflags +faststart -c:a copy output.mp4'
        final_file_save_loc = os.path.join("Output", f"{os.path.splitext(filename)[0]}.mp4")
        #command = f'ffmpeg -safe 0 -f concat -i list.txt -c copy "{final_file_save_loc}"'
        command = f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 -c:v h264_nvenc "{final_file_save_loc}"'
        print("final merge")
        subprocess.call(command, shell=True)
        os.remove("list.txt")
        # Delete the intermediate files
        #mp4_files_end = [f for f in os.listdir() if f.endswith(".mp4")] # mp4 files are created last
        mp4_files_end = os.listdir()
        filtered_list_end = [item for item in mp4_files_end if 'sentence' in item]
        for z in filtered_list_end:
            print(z)
            try:
                os.remove(z)
            except:
                print("An exception occurred")
        # os.remove(os.path.join(folder,filename))
        move(os.path.join(folder, filename),
             os.path.join(donefolder, filename))
        highest_i = -1


##check

import time
import subprocess
import os
import re
os.chdir("D:\\Users\\Henry\\Downloads\\github\\Learning-Python\\texttomp4")

def get_number(filename):
    return int(re.search(r'\d+', filename).group())
mp4_files = []
for filename_1 in os.listdir():
    if "sentence_merge_" in filename_1:
        if filename_1.endswith(".mp4"):
            mp4_files.append(filename_1)          
mp4_files_sorted = sorted_list = sorted(mp4_files, key=get_number)
with open('list.txt', 'w') as f:
    for file in mp4_files_sorted:
        f.write(f"file '{file}'\n")

command2 = f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 -c:v h264_nvenc output2.mp4'
command1 = f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 output1.mp4'
starttime = time.time()
subprocess.call(command1, shell=True)
endtime = time.time()
subprocess.call(command2, shell=True)
endtime2 = time.time()

endtime2-endtime
endtime-starttime

