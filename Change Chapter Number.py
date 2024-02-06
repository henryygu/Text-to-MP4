import re
import os
folder_path = 'D:\\Github\\Text-to-MP4\\Files'




for file_name in os.listdir('D:\\Github\\Text-to-MP4\\Files1'):
    file_path = os.path.join('D:\\Github\\Text-to-MP4\\Files1', file_name)
    # Check if the file is a text file with the "Chapter" pattern
    if file_name.endswith('.txt') and 'Desc.txt' in file_name:
        new_file_name = file_name.replace(f'Desc.txt', f'Chapter 000_ Desc.txt')
        # Rename the file
        new_file_path = os.path.join('D:\\Github\\Text-to-MP4\\Files1', new_file_name)
        print("old",os.path.basename(file_path))
        print("new",os.path.basename(new_file_path))
        print("_________________________________")
        os.rename(file_path, new_file_path)
    if file_name.endswith('.txt') and 'Chapter' in file_name:
        chapter_match = re.search(r'Chapter\s+(\d+)', file_name)
        if chapter_match:
            chapter_number = int(chapter_match.group(1))
            # Check if the chapter number is consecutive
            if chapter_number > 0:
                new_chapter_number = chapter_number # - 1
                # print(new_chapter_number, chapter_number)
                # Generate the new file name with the updated chapter number
                new_file_name = file_name.replace(f'Chapter {chapter_number}', f'Chapter {new_chapter_number:03d}')
                # Rename the file
                new_file_path = os.path.join('D:\\Github\\Text-to-MP4\\Files1', new_file_name)
                print("old",os.path.basename(file_path))
                print("new",os.path.basename(new_file_path))
                print("_________________________________")
                os.rename(file_path, new_file_path)
                #print(f'Renamed: {file_path} to {new_file_path}')
