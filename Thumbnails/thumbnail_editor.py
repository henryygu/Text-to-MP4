import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

os.chdir("Thumbnails")
# Function to overlay text on the background image
def overlay_text_on_background(bg_image, text, text_position, font_size=130, font_color=(255, 255,0)):
    img = Image.open(bg_image)
    draw = ImageDraw.Draw(img)
    # Load a font with the desired size
    font = ImageFont.truetype("arial.ttf", font_size)
    # Calculate the position for the text based on the provided coordinates
    x, y = text_position
    # Write the text on the image
    draw.text((x, y), text, font=font, fill=font_color)
    return img

# Function to generate multiple images using the Excel file
def generate_images(background_image, excel_file, output_folder):
    # Read the data from the Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file)
    filename1 = os.path.splitext(background_image)[0] 
    for index, row in df.iterrows():
        text = row['Chapter_names']  # Assuming the column containing the text is named 'Text'
        position = (70,460)  # Assuming the columns for X and Y coordinates are named 'X' and 'Y'
        # in Powerpoint, standard widescreen size, 1px = 0.03cm
        # Generate an image with the text overlay
        img_with_text = overlay_text_on_background(background_image, text, position)
        # Save the image to the output folder with a name corresponding to the row index
        img_with_text.save(f"{output_folder}/{filename1}_{index}.png")


# Replace these paths with your actual paths for the background image and Excel file
background_image_path = "brokenchains.png"
excel_file_path = "Book1.xlsx"
output_folder_path = "Completed_Thumbnails"

generate_images(background_image_path, excel_file_path, output_folder_path)
