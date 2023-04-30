import re
import os
import random
import time
from shutil import move
from math import ceil
import subprocess
from gtts import gTTS
from moviepy.editor import (
    TextClip,
    ImageClip,
    ColorClip
)
import logging
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
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
# filename = sorted_files[0]


def get_number(filename):
    return int(re.search(r'\d+', filename.split('_')[-1]).group())
def extract_filename_parts(filename):
    # Extract the prefix (everything before "____Chapter")
    prefix_match = re.search(r'- (.*)____Chapter', filename)
    if prefix_match:
        prefix = prefix_match.group(1).strip()
    else:
        prefix = ''

    # Extract the chapter number and title
    chapter_match = re.search(r'Chapter (\d+)_ (.+)\.txt$', filename)
    if chapter_match:
        chapter_number = 'Chapter ' + chapter_match.group(1)
        chapter_title = chapter_match.group(2).strip()
    else:
        chapter_number = ''
        chapter_title = ''

    # Extract the author name (everything before the first "-")
    author_match = re.search(r'^([^-\s]+)', filename)
    if author_match:
        author = author_match.group(1)
    else:
        author = ''

    # Return the extracted parts as a tuple
    return (author, prefix, chapter_number, chapter_title)

sentencecount = 0
paracount = 0


def extract_prefix(filename):
    return filename.split('____')[0]

def extract_number(filename):
    match = re.search(r'____Chapter (\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        return 0

# Group the files by prefix
files  = os.listdir(folder)
file_groups = {}
for filename in files:
    prefix = extract_prefix(filename)
    if prefix not in file_groups:
        file_groups[prefix] = []
    file_groups[prefix].append(filename)

# Sort the files within each group
sorted_files = []
for prefix, group in file_groups.items():
    sorted_group = sorted(group, key=extract_number)
    sorted_files.extend(sorted_group)

#print(sorted_files)


# Loop through all the text files in the folder
for filename in sorted_files:
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
        author, book, chapter_number, chapter_title = extract_filename_parts(filename)
        print(f"Author: {author}")
        print(f"Book: {book}")
        print(f"Chapter: {chapter_number}")
        print(f"Title: {chapter_title}")
        if chapter_number==chapter_title:
            title_name = f'{book} by {author}. {chapter_number}'
        else:
            title_name = f'{book} by {author}. {chapter_number} {chapter_title}'
        title_name
        for i, sentence in enumerate(sentences, 1):
            #print(f"Generating {i} out of {len(sentences)}")
            #print(sentence)
            starttime = time.time()
            format_i = "{:03d}".format(i)
            if i > highest_i:
                if i == 1:                 
                    video_start = TextClip(
                        title_name,
                        font="Arial",
                        fontsize=48,
                        color="white",
                        #bg_color="black",  # Add a black background color
                        method="caption",
                        align="south",
                        size=screensize,
                    )
                    bg_image = ColorClip(color=[0,0,0],size = screensize)
                    centered_image  = ImageClip(os.path.join("Images","hp2.jpg")).set_position(("center"))
                    result_clip = CompositeVideoClip([bg_image,centered_image,video_start])
                    result_clip.save_frame(f"frame.png", t=1)
                    tts = gTTS(text=title_name, lang="en",tld='com.au', slow=False)
                    tts.save(f"sentence.mp3")
                    sentence_cmd = f'ffmpeg -y -hide_banner -loglevel error -loop 1 -i frame.png -i sentence.mp3 -c:v libx264 -preset medium -tune stillimage -crf 18 -c:a copy -shortest sentence_merge_000.mp4'
                    subprocess.call(sentence_cmd,shell=True)
                if len(sentence) != 0:
                    print(f'{i} out of {len(sentences)}')
                    print(f'{sentence}')
                    # Convert the sentence into an mp3 file using gTTS
                    tts = gTTS(text=sentence, lang="en",tld='com.au', slow=False)
                    try:
                        tts.save(f"sentence_{format_i}.mp3")
                    except:
                        # #print("try failed")
                        # create 2 seconds of silence
                        cmd_1 = f'ffmpeg -y -hide_banner -loglevel error -f lavfi -i anullsrc=r=44100:cl=mono -t 2 -q:a 9 -acodec libmp3lame sentence_{format_i}.mp3'
                        subprocess.call(cmd_1,shell=True)
                    # Create a video file with the sentence text
                    video = TextClip(
                        "sentence",
                        font="Arial",
                        fontsize=48,
                        color="white",
                        bg_color="black",  # Add a black background color
                        method="caption",
                        align="south",
                        size=screensize,
                    )
                    bg_image = ColorClip(color=[0,0,0],size = screensize)
                    random_file = random.choice(os.listdir(os.path.join(os.getcwd(),"Images")))
                    centered_image = ImageClip(os.path.join("Images",random_file)).set_position(("center"))
                    result_clip = CompositeVideoClip([bg_image,centered_image,video])
                    result_clip.save_frame(f"frame_{format_i}.png", t=1)
                    sentence_cmd = f'ffmpeg -y -hide_banner -loglevel error -loop 1 -i frame_{format_i}.png -i sentence_{format_i}.mp3 -c:v libx264 -preset medium -tune stillimage -crf 18 -c:a copy -shortest sentence_merge_{format_i}.mp4'
                    subprocess.call(sentence_cmd,shell=True)
                    try:
                        os.remove(f"sentence_{format_i}.mp3")
                        os.remove(f"frame_{format_i}.png")
                    except:
                        print(f'error with deletion{format_i}')
            print(f'Currently elapsed time: {time.time()-starttime}')
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
            print(f'Deleting {z}')
            try:
                os.remove(z)
            except:
                print("An exception occurred")
        # os.remove(os.path.join(folder,filename))
        move(os.path.join(folder, filename),
             os.path.join(donefolder, filename))
        highest_i = -1
        print(time.time()-starttime)



## merge chapters into 1









# ##check

# import time
# import subprocess
# import os
# import re
# os.chdir("D:\\Users\\Henry\\Downloads\\github\\Learning-Python\\texttomp4")

# def get_number(filename):
#     return int(re.search(r'\d+', filename).group())
# mp4_files = []
# for filename_1 in os.listdir():
#     if "sentence_merge_" in filename_1:
#         if filename_1.endswith(".mp4"):
#             mp4_files.append(filename_1)          
# mp4_files_sorted = sorted_list = sorted(mp4_files, key=get_number)
# with open('list.txt', 'w') as f:
#     for file in mp4_files_sorted:
#         f.write(f"file '{file}'\n")

# command2 = f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 -c:v h264_nvenc output2.mp4'
# command1 = f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i list.txt -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 output1.mp4'
# starttime = time.time()
# subprocess.call(command1, shell=True)
# endtime = time.time()
# subprocess.call(command2, shell=True)
# endtime2 = time.time()

# endtime2-endtime
# endtime-starttime