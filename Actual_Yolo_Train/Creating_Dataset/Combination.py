import os
import logging
import shutil
import cv2
from once import ONCE
from multiprocessing import Pool


def copy_images_to_temp(source_dir, temp_dir, cameras):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    for seq_id in os.listdir(source_dir):
        for camera in cameras:
            src_camera_dir = os.path.join(source_dir, seq_id, camera)
            if os.path.exists(src_camera_dir):
                for image_file in os.listdir(src_camera_dir):
                    src_file_path = os.path.join(src_camera_dir, image_file)
                    dest_file_path = os.path.join(temp_dir, f"{seq_id}_{camera}_{image_file}")
                    shutil.copy2(src_file_path, dest_file_path)
                    logging.info(f"Copied {src_file_path} to {dest_file_path}")
            else:
                logging.warning(f"Source camera directory does not exist: {src_camera_dir}")


def process_image(image_info):
    dataset, temp_dir, yolov8_images_base, image_file, annotation_path = image_info

    seq_id, cam_id, frame_id_with_extension = image_file.split('_')
    frame_id, image_extension = os.path.splitext(frame_id_with_extension)

    dest_dir = os.path.join(yolov8_images_base, 'train')  # Assuming always 'train' for now
    os.makedirs(dest_dir, exist_ok=True)

    src_file_path = os.path.join(temp_dir, image_file)
    dest_file_path = os.path.join(dest_dir, image_file)
    print(seq_id)
    # Check if the file already exists in the destination directory
    if os.path.exists(dest_file_path):
        logging.info(f"Skipping {src_file_path} as it already exists in {dest_file_path}")
        return  # Skip processing this image if it already exists in the destination

    # Load, undistort, and save the image
    img = cv2.imread(src_file_path)
    # Assuming img_buf returns a correctly undistorted image; this logic may need to be adjusted
    img_buf, _ = dataset.undistort_image_v2(seq_id=seq_id, frame_id=frame_id)
    camera_index = dataset.camera_names.index(cam_id)
    undistorted_img = img_buf[camera_index]
    cv2.imwrite(dest_file_path, cv2.cvtColor(undistorted_img, cv2.COLOR_RGB2BGR))

    logging.info(f"Undistorted and moved {src_file_path} to {dest_file_path}")


def move_images_based_on_annotations(dataset, temp_dir, yolov8_labels_base, yolov8_images_base):
    image_infos = []

    for image_file in os.listdir(temp_dir):
        # Extract seq_id, cam_id, frame_id from filename
        parts = image_file.split('_')
        seq_id, cam_id, frame_id_with_extension = parts[0], parts[1], parts[-1]
        frame_id, image_extension = os.path.splitext(frame_id_with_extension)

        base_filename = f"{seq_id}_{cam_id}_{frame_id}"
        for split in ['train', 'val', 'test']:
            annotation_file = f"{base_filename}.txt"
            annotation_path = os.path.join(yolov8_labels_base, split, annotation_file)
            if os.path.exists(annotation_path):
                image_infos.append((dataset, temp_dir, yolov8_images_base, image_file, annotation_path))

    # Use multiprocessing Pool to process images in parallel
    with Pool() as pool:
        pool.map(process_image, image_infos)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Using paths provided earlier
    dataset_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
    source_dir = os.path.join(dataset_base, "data")
    temp_dir = os.path.join(dataset_base, "temp_images")
    yolov8_labels_base = os.path.join(dataset_base, "Yolov8 Structure", "V6", "dataset", "labels")
    yolov8_images_base = os.path.join(dataset_base, "Yolov8 Structure", "V6", "dataset", "images")
    dataset = ONCE(dataset_root=dataset_base)
    cameras = ['cam01', 'cam03', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']

    #copy_images_to_temp(source_dir, temp_dir, cameras)
    move_images_based_on_annotations(dataset, temp_dir, yolov8_labels_base, yolov8_images_base)


if __name__ == "__main__":
    main()
