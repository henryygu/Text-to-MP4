import os
import re
from tqdm import tqdm


def sanitize_filename(filename):
    pattern = r'[\\/:*?"<>|\r\n]+'
    return re.sub(pattern, '_', filename)

folder_name = 'D:\\Github\\Text-to-MP4\\OG Files\\'
output_folder = 'D:\\Github\\Text-to-MP4\\Files1\\'
for file_name in tqdm(os.listdir(folder_name)):
    if file_name.endswith(".txt"):
        file_path = os.path.join(folder_name, file_name)
        with open(file_path, 'r', encoding="utf8") as file:
            file_content = file.read()
        chapter_titles = re.findall(r'(\*Chapter \d+\*\:.*?)(?:\n|$)', file_content)            
        chapter_titles.insert(0,"Desc")
        chapters = re.split(r'\*Chapter \d+.*\r?\n', file_content)
        # chapter_regex = r'\*Chapter \d+\*: .+?\n.+?(?=\*Chapter \d+:|$)'
        # chapters = re.findall(chapter_regex, file_content, re.DOTALL)
        for i, chapter in enumerate(chapters):
            sanitized_filename = sanitize_filename(chapter_titles[i])
            chapter_name = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}___{sanitized_filename}.txt")
            with open(chapter_name, 'w', encoding="utf8") as file:
                text_to_write = chapter_titles[i] +"\n\n\n\n"+ chapter
                a = file.write(text_to_write)
                file.close()
            
                
