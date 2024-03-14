import os
import shutil
from sklearn.model_selection import train_test_split
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to your dataset folders; adjust them to your real paths
dataset_root = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov8 Structure\V1\dataset"
original_images_dir = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam07"
original_labels_dir = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam07\Yolo_Info"

# Ensure target directories exist
phases = ["train", "val", "test"]
for phase in phases:
    os.makedirs(os.path.join(dataset_root, "images", phase), exist_ok=True)
    os.makedirs(os.path.join(dataset_root, "labels", phase), exist_ok=True)

# Listing annotation files and assuming images are .jpg
annotation_files = [f for f in os.listdir(original_labels_dir) if f.endswith('.txt')]
image_files = [f.replace('.txt', '.jpg') for f in annotation_files]

# Split the dataset
train_files, test_files = train_test_split(image_files, test_size=0.2, random_state=42)
train_files, val_files = train_test_split(train_files, test_size=0.25, random_state=42)

def copy_and_rename_if_exists(files, source_dir, target_dir, phase):
    """Copy files from source to target directory, renaming if the file already exists."""
    suffixes = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for f in files:
        base_name, ext = os.path.splitext(f)
        for suffix in ('',) + tuple(suffixes):
            new_name = f"{base_name}{suffix}{ext}"
            src_file = os.path.join(source_dir, f if suffix == '' else f"{base_name}{ext}")
            dst_file = os.path.join(target_dir, new_name)
            if not os.path.exists(dst_file):
                shutil.copy2(src_file, dst_file)
                logging.info(f"Copied {src_file} to {dst_file}")
                # Rename annotation file correspondingly
                src_label = src_file.replace('.jpg', '.txt').replace("images", "labels")
                dst_label = dst_file.replace('.jpg', '.txt').replace("images", "labels")
                if os.path.exists(src_label):
                    shutil.copy2(src_label, dst_label)
                    logging.info(f"Copied label {src_label} to {dst_label}")
                break
            elif suffix == suffixes[-1]:  # If we've exhausted our suffix options
                logging.error(f"Exhausted rename attempts for {src_file}. Skipping file.")

# Copy and rename files to their respective directories
for phase, files in zip(phases, [train_files, val_files, test_files]):
    copy_and_rename_if_exists(files, original_images_dir, os.path.join(dataset_root, "images", phase), phase)
    # Labels are handled inside the function to keep names synchronized

logging.info("Dataset organization complete.")
