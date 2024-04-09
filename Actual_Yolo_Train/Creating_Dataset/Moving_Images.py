import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_sequence_ids(split_file):
    """
    Reads a split file and returns the list of sequence IDs.
    """
    with open(split_file, 'r') as file:
        sequence_ids = file.read().splitlines()
    return sequence_ids

def copy_and_rename_images(source_dir, dest_dir, sequence_ids, cameras):
    """
    Copies images from the source directory to the destination directory
    based on the provided sequence IDs and camera names. It also renames the images
    to include the camera identifier in the filename to prevent collisions.
    """
    for seq_id in sequence_ids:
        for camera in cameras:
            src_camera_dir = os.path.join(source_dir, seq_id, camera)
            if os.path.exists(src_camera_dir):
                for image_file in os.listdir(src_camera_dir):
                    # Include the camera identifier in the filename
                    new_image_name = f"{camera}_{image_file}"
                    src_file_path = os.path.join(src_camera_dir, image_file)
                    dest_file_path = os.path.join(dest_dir, new_image_name)
                    shutil.copy2(src_file_path, dest_file_path)
                    logging.info(f"Copied and renamed {src_file_path} to {dest_file_path}")
            else:
                logging.warning(f"Source camera directory does not exist: {src_camera_dir}")

def main():
    dataset_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov8 Structure\V2\dataset'
    original_dataset_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\data'
    split_files_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\ImageSets'
    cameras = ['cam01', 'cam03', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']

    # Read the sequence IDs from the split files
    train_ids = get_sequence_ids(os.path.join(split_files_dir, 'train_split.txt'))
    val_ids = get_sequence_ids(os.path.join(split_files_dir, 'val_split.txt'))
    test_ids = get_sequence_ids(os.path.join(split_files_dir, 'test_split.txt'))

    # Copy and rename images to the respective directories
    copy_and_rename_images(original_dataset_dir, os.path.join(dataset_base, 'images', 'train'), train_ids, cameras)
    copy_and_rename_images(original_dataset_dir, os.path.join(dataset_base, 'images', 'val'), val_ids, cameras)
    copy_and_rename_images(original_dataset_dir, os.path.join(dataset_base, 'images', 'test'), test_ids, cameras)

if __name__ == '__main__':
    main()