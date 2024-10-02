from PIL import Image, ImageDraw, ImageFont
import cv2
import os

# Helper function to load images
def load_images(image_paths):
    images = []
    for img_path in image_paths:
        img = Image.open(img_path)
        images.append(img)
    return images

# Create Banner Function
def create_banner(image_paths, promo_text, color_palette, theme, output_size, output_file):
    images = load_images(image_paths)
    
    # Define the output banner size
    banner_width, banner_height = output_size

    # Create a blank banner
    banner = Image.new('RGB', (banner_width, banner_height), color=color_palette['background'])

    # Draw on the banner
    draw = ImageDraw.Draw(banner)
    font = ImageFont.truetype("arial.ttf", 40)  # Customizable font

    # Loop to add images and arrange them
    x_offset = 0
    for img in images:
        img = img.resize((banner_width // len(images), banner_height // 2))  # Resize image to fit banner
        banner.paste(img, (x_offset, 0))  # Paste image into the banner
        x_offset += img.size[0]

    # Add promotional text
    text_position = (50, banner_height // 2 + 20)
    draw.text(text_position, promo_text, fill=color_palette['text'], font=font)

    # Add theme elements like a border
    if theme == "festive":
        draw.rectangle([(5, 5), (banner_width-5, banner_height-5)], outline=color_palette['border'], width=10)

    # Save banner
    banner.save(output_file)
    print(f"Banner saved as {output_file}")

# Function to create a video (basic)
def create_video(image_paths, promo_text, color_palette, theme, output_size, video_file):
    images = load_images(image_paths)
    
    # Video specifications
    banner_width, banner_height = output_size
    fps = 30
    video = cv2.VideoWriter(video_file, cv2.VideoWriter_fourcc(*'mp4v'), fps, output_size)
    
    for i in range(len(images)):
        banner = Image.new('RGB', (banner_width, banner_height), color=color_palette['background'])
        draw = ImageDraw.Draw(banner)
        font = ImageFont.truetype("arial.ttf", 40)
        
        img = images[i].resize((banner_width, banner_height // 2))
        banner.paste(img, (0, 0))

        # Add promotional text
        text_position = (50, banner_height // 2 + 20)
        draw.text(text_position, promo_text, fill=color_palette['text'], font=font)

        if theme == "festive":
            draw.rectangle([(5, 5), (banner_width-5, banner_height-5)], outline=color_palette['border'], width=10)

        frame = cv2.cvtColor(np.array(banner), cv2.COLOR_RGB2BGR)
        video.write(frame)

    video.release()
    print(f"Video saved as {video_file}")

# Example usage
image_paths = ['product1.jpg', 'product2.jpg']  # Paths to your product images
promo_text = "Diwali Sale: Up to 50% Off!"  # Promotional text
color_palette = {
    'background': (255, 255, 255),  # White background
    'text': (255, 0, 0),            # Red text
    'border': (0, 255, 0)           # Green festive border
}
theme = "festive"
output_size = (1920, 1080)  # Full HD size
output_file = "banner.jpg"
video_file = "promo_video.mp4"

# Create a banner
create_banner(image_paths, promo_text, color_palette, theme, output_size, output_file)

# Create a video
create_video(image_paths, promo_text, color_palette, theme, output_size, video_file)
