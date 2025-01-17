from PIL import Image
import random

# Define augmentation parameters
def augment_image(image):
    # Slight rotation
    angle = random.uniform(-1.5, 1.5)  # Random rotation between -10 to 10 degrees
    rotated_image = image.rotate(angle, resample=Image.BICUBIC, expand=False)

    # Zoom in/out
    scale = random.uniform(0.95, 1.05)  # Random zoom factor (0.8 = zoom out, 1.2 = zoom in)
    w, h = rotated_image.size
    new_w, new_h = int(w * scale), int(h * scale)
    resized_image = rotated_image.resize((new_w, new_h), resample=Image.BICUBIC)

    # If zoomed in, crop to original size; if zoomed out, pad to original size
    if scale > 1.0:  # Zoom in: center crop
        left = (new_w - w) // 2
        top = (new_h - h) // 2
        resized_image = resized_image.crop((left, top, left + w, top + h))
    elif scale < 1.0:  # Zoom out: center pad
        background = Image.new("RGB", (w, h), (0, 0, 0))  # Black background
        left = (w - new_w) // 2
        top = (h - new_h) // 2
        background.paste(resized_image, (left, top))
        resized_image = background

    return resized_image

# Load the image

import os
from PIL import Image

# Path to your folder containing images
folder_path = "seepain_data/Schmerzzeichnungen/"

# Get the list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp'))]

# Iterate over each image file
for idx, image_file in enumerate(image_files, 0):  # Starts counting from 1
    # Build the full path to the image
    image_path = os.path.join(folder_path, image_file)

    # Open the image
    org_image = Image.open(image_path)

    # Run your loop 20 times on the image

    for i in range(20):

        # Perform augmentation
        augmented_image = augment_image(org_image)

        # Load the image
        image = augmented_image.convert("RGBA")  # Replace with your image file path

        # Get the pixel data
        pixels = image.load()

        # Define the threshold for "blackness"
        threshold = 255  # Adjust this value as needed

        # Loop through all pixels
        width, height = image.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]  # Get RGBA values

                # Check if the pixel is "close enough" to black
                if r < threshold and g < threshold and b < threshold:
                    pixels[x, y] = (255, 255, 255, a)  # Replace with white (preserve alpha)

        background_image_path = "background_image.png"  # Path to the background image

        # Load the images
        modified_image = image.convert("RGBA")  # Ensure RGBA mode
        background_image = Image.open(background_image_path).convert("RGBA")  # Ensure RGBA mode

        # Make white pixels transparent in the modified image
        pixels = modified_image.load()
        width, height = modified_image.size

        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]  # Get RGBA values
                if r == 255 and g == 255 and b == 255:  # Check if the pixel is white
                    pixels[x, y] = (255, 255, 255, 0)  # Make it transparent

        # Ensure the background image matches the size of the modified image
        background_image = background_image.resize((width, height))

        # Merge the images
        merged_image = Image.alpha_composite(background_image, modified_image)

        # Save the resulting image
        output_path = "seepain_data/aug_images/aug_image_" + str(idx) + "_" + str(i) + ".png"  # Path for the merged image
        merged_image.save(output_path)

        print(f"Augmented image saved to {output_path}")