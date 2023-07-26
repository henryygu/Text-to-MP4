import re
import os
folder_path = 'D:\\Github\\Text-to-MP4\\Files'

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    # Check if the file is a text file with the "Chapter" pattern
    if file_name.endswith('.txt') and 'Chapter' in file_name:
        match = re.search(r'Chapter\s+(\d+)', file_name)
        if match:
            chapter_number = match.group(1)
            chapter_number_int = int(chapter_number)
            # Format the chapter number with leading zeros to have three digits
            new_file_name = file_name.replace(f'Chapter {chapter_number}', f'Chapter {chapter_number_int:03d}')
            print(new_file_name)         
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_name} -> {new_file_name}")
        else:
            print(f"Chapter number not found in the file name: {file_name}")







for file_name in os.listdir('D:\\Github\\Text-to-MP4\\Files'):
        file_path = os.path.join('D:\\Github\\Text-to-MP4\\Files', file_name)
        # Check if the file is a text file with the "Chapter" pattern
        if file_name.endswith('.txt') and 'Chapter' in file_name:
            chapter_match = re.search(r'Chapter\s+(\d+)', file_name)
            if chapter_match:
                chapter_number = int(chapter_match.group(1))
                # Check if the chapter number is consecutive
                if chapter_number > 0:
                    new_chapter_number = chapter_number - 1
                    #print(new_chapter_number, chapter_number)
                    # Generate the new file name with the updated chapter number
                    new_file_name = file_name.replace(f'Chapter {chapter_number:02d}', f'Chapter {new_chapter_number:02d}')
                    # Rename the file
                    new_file_path = os.path.join('D:\\Github\\Text-to-MP4\\Files', new_file_name)
                    
                    
                    print("old",os.path.basename(file_path))
                    print("new",os.path.basename(new_file_path))
                    print("_________________________________")
                    os.rename(file_path, new_file_path)
                    #print(f'Renamed: {file_path} to {new_file_path}')
