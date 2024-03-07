import os
from PIL import Image
import numpy as np

# Specify the paths to the two folders
folder1_path = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\ONCE Data\cam07\cam07"
folder2_path = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\ONCE Data\cam07\cam08"

# Create the output folder
output_folder = 'Camera_7_8_Normal'
os.makedirs(output_folder, exist_ok=True)

# Get the list of image names in both folders
images_folder1 = set(os.listdir(folder1_path))
images_folder2 = set(os.listdir(folder2_path))

# Find common images by intersection
common_images = images_folder1.intersection(images_folder2)

# Process each image
for image_name in common_images:
    try:
        # Construct the full path to the images
        image1_path = os.path.join(folder1_path, image_name)
        image2_path = os.path.join(folder2_path, image_name)

        # Open the images
        image1 = Image.open(image1_path)
        image2 = Image.open(image2_path)

        # Convert images to numpy arrays
        image1_array = np.array(image1)
        image2_array = np.array(image2)

        # Concatenate the images
        # Use axis=0 for vertical concatenation, axis=1 for horizontal
        concatenated_image_array = np.concatenate((image1_array, image2_array), axis=1)

        # Convert the numpy array back to an image
        concatenated_image = Image.fromarray(concatenated_image_array)

        # Save the image in the output folder
        concatenated_image.save(os.path.join(output_folder, image_name))

    except Exception as e:
        print(f"Error processing {image_name}: {e}")

print("Process completed.")
