import os
from send2trash import send2trash
folder_path = "Output\\"
os.chdir("D:\\Github\Text-to-MP4\\")
for root, dirs, files in os.walk(folder_path):
    if "combined.wav.wav" in files:
        for file in files:
            if file.endswith("combined.wav.wav"):
                a = 1
            else:
                #os.remove(os.path.join(root,file))
                send2trash(os.path.join(root,file))
                #print("file")
                #print(file)
    else:
        #print("root")
        print(root)        
