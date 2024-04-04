import tarfile
import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_tar_to_temp(tar_path, temp_path):
    """
    Extracts a .tar file to a temporary path.
    """
    logging.info(f"Starting extraction of {tar_path}")
    with tarfile.open(tar_path, 'r') as tar:
        tar.extractall(path=temp_path)
        logging.info(f"Extracted {tar_path} to {temp_path}")


def move_camera_files(src_folder, dst_folder):
    """
    Moves camera image files from the source to the destination folder.
    """
    if not os.path.exists(src_folder):
        logging.warning(f"Source directory does not exist: {src_folder}")
        return

    for image_file in os.listdir(src_folder):
        src_path = os.path.join(src_folder, image_file)
        dst_path = os.path.join(dst_folder, image_file)
        shutil.move(src_path, dst_path)
        logging.info(f"Moved {src_path} to {dst_folder}")


def process_camera_data(temp_path, dataset_root, camera):
    """
    Processes camera data by moving the image files to the corresponding dataset structure.
    """
    data_path = os.path.join(temp_path, 'data')
    for seq_id in os.listdir(data_path):
        src_folder = os.path.join(data_path, seq_id, camera)
        dst_folder = os.path.join(dataset_root, 'data', seq_id, camera)
        move_camera_files(src_folder, dst_folder)


def main():
    dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
    tar_files_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Temp'
    temp_extract_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\New_Temp'

    # Process camera tar files
    for camera in ['cam01', 'cam03', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']:
        tar_file_path = os.path.join(tar_files_dir, f"{camera}.tar")
        if os.path.exists(tar_file_path):
            extract_tar_to_temp(tar_file_path, temp_extract_dir)
            process_camera_data(temp_extract_dir, dataset_root, camera)
            # Clean up the temporary directory
            shutil.rmtree(temp_extract_dir, ignore_errors=True)
        else:
            logging.warning(f"No tar file found for {camera}")


if __name__ == "__main__":
    main()
