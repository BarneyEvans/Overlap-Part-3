import tarfile
import os
import shutil
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_tar_to_temp(tar_path, temp_path):
    logging.info(f"Extracting {tar_path} to {temp_path}")
    try:
        with tarfile.open(tar_path, 'r') as tar:
            tar.extractall(path=temp_path)
            # Log the names of all members that were extracted
            for member in tar.getmembers():
                logging.info(f"Extracted {member.name} to {temp_path}")
        logging.info(f"Finished extracting {tar_path}")
    except Exception as e:
        logging.error(f"Error extracting {tar_path}: {e}")


def move_files(src_path, dst_path):
    if not os.path.exists(src_path):
        logging.warning(f"Source directory does not exist: {src_path}")
        return
    for item in os.listdir(src_path):
        s = os.path.join(src_path, item)
        d = os.path.join(dst_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
            logging.info(f"Copied directory {s} to {d}")
        else:
            shutil.copy2(s, d)
            logging.info(f"Copied file {s} to {d}")


def main():
    dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
    tar_files_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Temp'
    temp_extract_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\New_Temp'

    # Get the list of all tar files to process
    tar_files = [os.path.join(tar_files_dir, f) for f in os.listdir(tar_files_dir) if f.endswith('.tar')]

    # Process each tar file
    for tar_file in tar_files:
        # Extract the contents of the tar file
        extract_tar_to_temp(tar_file, temp_extract_dir)

        # Depending on the tar file name, move the extracted files to the correct location
        # Assuming the naming convention is consistent (e.g., 'train_cam07.tar' contains 'train' and 'cam07')
        parts = os.path.basename(tar_file).split('_')
        if len(parts) == 2:
            # Example: 'train', 'cam07.tar'
            subset, camera = parts[0], parts[1].split('.')[0]  # 'train', 'cam07'
            # Determine destination directory
            for seq_id in os.listdir(os.path.join(temp_extract_dir, 'data')):
                src_folder = os.path.join(temp_extract_dir, 'data', seq_id, camera)
                dst_folder = os.path.join(dataset_root, 'data', seq_id, camera)
                move_files(src_folder, dst_folder)

        # Clean up the temporary extraction directory after each tar file
        shutil.rmtree(temp_extract_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
