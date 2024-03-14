import os
import shutil
from sklearn.model_selection import train_test_split
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths to your dataset folders; adjust them to your real paths
dataset_root = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov8 Structure\V1\dataset"
original_images_dir = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam08"
original_labels_dir = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam08\Yolo_Info"

# Ensure the target directories exist; create them if not
for phase in ["train", "val", "test"]:
    os.makedirs(os.path.join(dataset_root, "images", phase), exist_ok=True)
    os.makedirs(os.path.join(dataset_root, "labels", phase), exist_ok=True)
    logging.info(f"Directories for {phase} phase are ready.")

# Listing all the annotation files
annotation_files = [f for f in os.listdir(original_labels_dir) if f.endswith('.txt')]
# Assuming images are .jpg; adjust if your case is different
image_files = [f.replace('.txt', '.jpg') for f in annotation_files]

# Splitting the files
train_files, test_files = train_test_split(image_files, test_size=0.2, random_state=42)
train_files, val_files = train_test_split(train_files, test_size=0.25, random_state=42)  # Results in 60% train, 20% val, 20% test

def copy_files(files, source_dir, target_dir):
    """Copy files from source to target directory, preserving metadata."""
    for f in files:
        src_file = os.path.join(source_dir, f)
        dst_file = os.path.join(target_dir, f)
        if os.path.exists(dst_file):
            logging.warning(f"{dst_file} already exists. Skipping copy...")
        else:
            shutil.copy2(src_file, dst_file)
            logging.info(f"Copied {src_file} to {dst_file}")

# Copying the files to their respective directories and keeping track
for phase, files in zip(["train", "val", "test"], [train_files, val_files, test_files]):
    copy_files([f.replace('.jpg', '.txt') for f in files], original_labels_dir, os.path.join(dataset_root, "labels", phase))
    copy_files(files, original_images_dir, os.path.join(dataset_root, "images", phase))

logging.info("Dataset organization complete. Check the logs for details.")
