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
existingfiles = os.listdir()
#mp3_or_mp4_files = [f for f in existingfiles if f.endswith(".mp3") or f.endswith(".mp4")]
mp3_or_mp4_files = [f for f in existingfiles if f.endswith(".mp4")] # mp4 files are created last
i_values = [int(re.search(r"sentence_(\d+)", f).group(1)) for f in mp3_or_mp4_files]
# find the highest value of i
if len(i_values) == 0:
    highest_i=-1
else:
    highest_i = max(i_values)

#debug
filename = os.listdir(folder)[0]

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
        
        # Convert each sentence into a text to speech mp3 file and video file
        for i, sentence in enumerate(sentences):
            print(f'{i} out of {len(sentences)}' )
            print(sentence)
            if i < highest_i: #sometimes script fails, this will allow you to not have to redo if files already exists
                continue
            else:
                print("else")
                if len(sentence)!=0:
                    # Convert the sentence into an mp3 file using gTTS
                    tts = gTTS(text=sentence, lang='en')
                    try:
                        print("try succeeded")
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
                    video.write_videofile(f"sentence_{i}.mp4",fps=24)
                    video.close()

                    # # Append the audio and video files to the list
                    # audio_files.append(AudioFileClip(f"sentence_{i}.mp3"))
                    # video_files.append(VideoFileClip(f"sentence_{i}.mp4"))
        audio_files = []
        video_files = []
        sentencecount=0
        for i, sentence in enumerate(sentences):
            print(f'Appending Sentence {i} out of {len(sentences)}' )
            audio_files.append(AudioFileClip(f"sentence_{i}.mp3"))
            video_files.append(VideoFileClip(f"sentence_{i}.mp4"))
            if i % 10 == 0 or i == len(sentences):
                sentencecount+=1
                audio_files.append(AudioFileClip(f"sentence_{i}.mp3"))
                video_files.append(VideoFileClip(f"sentence_{i}.mp4"))
                
                sentence_video = concatenate_videoclips(video_files, method="compose")
                sentence_audio = concatenate_audioclips(audio_files)
                
                # Overlay the audio on top of the video
                sentence_video = sentence_video.set_audio(sentence_audio)
                
                # Write the final video file with the same name as the input text file
                #final_video.write_videofile(f"{os.path.splitext(filename)[0]}_final_video.mp4")
                sentence_video.write_videofile(f"paragraph_{sentencecount}.mp4")
                sentence_video.close() # close the final video file after saving it
                audio_files = []
                video_files = []
        
        paragraphs = ceil(len(sentences)/10)
        paracount = 0
        for i in range(paragraphs):
            print(f'Appending Paragraph {i} out of {paragraphs}' )
            video_files.append(VideoFileClip(f"paragraph_{i+1}.mp4"))
            if i % 10 == 0 or i == paragraphs:
                paracount+=1
                video_files.append(VideoFileClip(f"paragraph_{i+1}.mp4"))
                
                sentence_video = concatenate_videoclips(video_files, method="compose")

                # Write the final video file with the same name as the input text file
                #final_video.write_videofile(f"{os.path.splitext(filename)[0]}_final_video.mp4")
                sentence_video.write_videofile(f"intermediate_{paracount}.mp4")
                sentence_video.close() # close the final video file after saving it
                video_files = []
                
        
        intermediates = ceil(paragraphs/10)
        
        for i in range(intermediates):
            print(f'Appending intermediates {i} out of {intermediates}' )
            video_files.append(VideoFileClip(f"intermediate_{i+1}.mp4"))
            if i % 10 == 0 or i == intermediates:
                video_files.append(VideoFileClip(f"intermediate_{i+1}.mp4"))
                
                sentence_video = concatenate_videoclips(video_files, method="compose")

                # Write the final video file with the same name as the input text file
                #final_video.write_videofile(f"{os.path.splitext(filename)[0]}_final_video.mp4")
                sentence_video.write_videofile(os.path.join("Output",f"{os.path.splitext(filename)[0]}_final.mp4"))
                sentence_video.close() # close the final video file after saving it
                video_files = []
                
        

        # Delete the intermediate files
        for i in range(len(sentences)):
            try:
                os.remove(f"sentence_{i}.mp3")
                os.remove(f"sentence_{i}.mp4")
                os.remove(f"paragraph_{i}.mp4")
                os.remove(f"intermediate_{i}.mp4")
            except:
                print(i)
    #os.remove(os.path.join(folder,filename))
    move(os.path.join(folder,filename),os.path.join(donefolder,filename))    
