from moviepy.editor import ImageSequenceClip, AudioFileClip, ImageClip, CompositeVideoClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import os

# Function to create a text image with custom font and size
def create_text_image(text, size, font_size=50):
    # Create an image with a black background
    img = Image.new('RGB', size, color=(0, 0, 0, 0))  # Transparent background
    draw = ImageDraw.Draw(img)

    # Load a font (use a system font or specify your own font path)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)  # Default to Arial or specify font path
    except IOError:
        font = ImageFont.load_default()  # Use default if specified font is not found

    # Calculate text size and position using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Center the text horizontally and position near the bottom
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 50  # 50 pixels from the bottom

    # Draw the text on the image
    draw.text((text_x, text_y), text, fill='white', font=font)

    # Save to a temporary path
    temp_path = os.path.join(r'D:\Work\Test', f'{text}.png')
    img.save(temp_path)
    return temp_path

# List of images to include in the video
image_files = [
    r'D:\Work\Test\genimg_0.png',
    r'D:\Work\Test\genimg_1.png'
]

# Open the first image to get its size
base_image = Image.open(image_files[0])
base_size = base_image.size

# Resize all images to match the size of the first image
resized_images = []
for img_path in image_files:
    img = Image.open(img_path)
    resized_img = img.resize(base_size, Image.LANCZOS)
    resized_img.save(img_path)  # Overwrite the image with the resized version
    resized_images.append(img_path)

# Load the audio file
audio_clip = AudioFileClip(r'D:\Work\Test\output.mp3')

# Calculate the duration for each image based on the audio length
num_images = len(resized_images)
image_duration = audio_clip.duration / num_images  # Duration for each image

# Create a list to hold final clips
final_clips = []

# Create clips for images and text
for i in range(num_images):
    img_path = resized_images[i]
    text_image_path = create_text_image(f"Image {i + 1}", base_size)

    # Create image clip
    image_clip = ImageClip(img_path).set_duration(image_duration).set_position("center")

    # Add fade in/out transitions to each image
    image_clip = image_clip.fadein(1).fadeout(1)

    # Create text clip from the generated text image
    text_clip = ImageClip(text_image_path).set_duration(image_duration).set_position(('center', 'bottom')).set_opacity(0.7)
    
    # Create a composite clip with the image and text
    combined_clip = CompositeVideoClip([image_clip, text_clip])

    final_clips.append(combined_clip)

# Concatenate all the individual clips into one video
final_video = concatenate_videoclips(final_clips, method="compose")

# Set audio to the final concatenated video
final_video = final_video.set_audio(audio_clip)

# Export the final video with fps specified
final_video.write_videofile(r'D:\Work\Test\final_movie_with_fades.mp4', fps=24, codec="libx264", audio_codec="aac")
