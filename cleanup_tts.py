import os
folder_path = "Output\\"
os.chdir("D:\\Github\Text-to-MP4\\")
for root, dirs, files in os.walk(folder_path):
    if "combined.wav" in files:
        for file in files:
            if file.endswith("combined.wav"):
                a = 1
            else:
                os.remove(os.path.join(root,file))
                #print("file")
                #print(file)
    else:
        #print("root")
        print(root)        
