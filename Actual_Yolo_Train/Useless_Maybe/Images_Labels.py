import os
import random
import shutil
import logging

def distribute_annotations(temp_annotations_dir, yolov8_labels_base):
    """
    Distributes annotation files from a temporary folder into train, val, and test splits.

    Args:
    - temp_annotations_dir: Path to the temporary annotations directory.
    - yolov8_labels_base: Base path for the YOLOv8 labels directory where train, val, and test directories exist.
    """
    # Ensure output directories exist
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(yolov8_labels_base, split), exist_ok=True)

    # List all annotation files
    all_files = [f for f in os.listdir(temp_annotations_dir) if os.path.isfile(os.path.join(temp_annotations_dir, f))]
    random.shuffle(all_files)  # Shuffle for random distribution

    # Determine split indices
    total_files = len(all_files)
    train_end = int(total_files * 0.8)
    val_end = train_end + int(total_files * 0.1)

    # Distribute files
    for i, file in enumerate(all_files):
        if i < train_end:
            split = 'train'
        elif i < val_end:
            split = 'val'
        else:
            split = 'test'

        src_path = os.path.join(temp_annotations_dir, file)
        dest_path = os.path.join(yolov8_labels_base, split, file)
        shutil.move(src_path, dest_path)
        logging.info(f"Moved {file} to {split} folder.")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Update these paths according to your project structure
    temp_annotations_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\temp_annotations'
    yolov8_labels_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V5\dataset\labels'

    distribute_annotations(temp_annotations_dir, yolov8_labels_base)

if __name__ == "__main__":
    main()
