import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_directories(base_path):
    """
    Creates the required directory structure for YOLOv8 training.
    """
    # Directories to be created under the base path
    dirs_to_create = [
        'images/train', 'images/val', 'images/test',
        'labels/train', 'labels/val', 'labels/test'
    ]

    for dir in dirs_to_create:
        path = os.path.join(base_path, dir)
        os.makedirs(path, exist_ok=True)
        logging.info(f"Created directory: {path}")

def main():
    # Base path for YOLOv8 dataset
    base_path = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V5\dataset'
    create_directories(base_path)

if __name__ == '__main__':
    main()
