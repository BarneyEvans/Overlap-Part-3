import os
import random
import shutil
import time


def shuffle_and_copy_files(base_path, target_base_path, category_folders):
    # Seed the random number generator for reproducibility
    random.seed(42)

    # Prepare dictionaries to track original and new file locations
    original_files = {}
    for folder in category_folders:
        folder_path = os.path.join(base_path, folder)
        original_files[folder] = os.listdir(folder_path)

    all_files = [f for sublist in original_files.values() for f in sublist]
    random.shuffle(all_files)

    # Assign files back ensuring original counts are maintained
    new_distribution = {}
    start = 0
    for folder, files in original_files.items():
        count = len(files)
        new_distribution[folder] = all_files[start:start + count]
        start += count

    # Create target folders if they do not exist
    for folder in category_folders:
        os.makedirs(os.path.join(target_base_path, folder), exist_ok=True)

    # Copy files to their new locations
    file_count = 0
    for folder, files in new_distribution.items():
        for file in files:
            original_folder = [f for f, flist in original_files.items() if file in flist][0]
            original_path = os.path.join(base_path, original_folder, file)
            new_path = os.path.join(target_base_path, folder, file)
            if not os.path.exists(new_path):  # Skip copying if file already exists
                shutil.copy2(original_path, new_path)
                print(f'Copied {original_path} to {new_path}')
            file_count += 1
            if file_count % 100 == 0:  # Clear screen every 100 files processed
                os.system('clear')
                print(f'Processed {file_count} files...')


# Base paths for images and labels
root_path = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset'
image_path = os.path.join(root_path, 'images')
label_path = os.path.join(root_path, 'labels')

# Target base paths for images and labels
target_root_path = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V7\dataset'
target_image_path = os.path.join(target_root_path, 'images')
target_label_path = os.path.join(target_root_path, 'labels')

# Folders
folders = ['test', 'train', 'val']

# Shuffle and copy images
shuffle_and_copy_files(image_path, target_image_path, folders)
# Shuffle and copy labels in the same way as images
shuffle_and_copy_files(label_path, target_label_path, folders)
