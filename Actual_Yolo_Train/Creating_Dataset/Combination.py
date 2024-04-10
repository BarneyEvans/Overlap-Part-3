import os
import logging
import cv2
from once import ONCE
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_sequence_ids(split_file):
    with open(split_file, 'r') as file:
        sequence_ids = file.read().splitlines()
    return sequence_ids

def process_images_based_on_annotations(dataset, source_dir, temp_dir, yolov8_labels_base, yolov8_images_base, sequence_ids, cameras, image_extension='.jpg'):
    for seq_id in sequence_ids:
        for camera in cameras:
            src_camera_dir = os.path.join(source_dir, seq_id, camera)
            if os.path.exists(src_camera_dir):
                for image_file in os.listdir(src_camera_dir):
                    # Check if corresponding annotation exists
                    base_filename = image_file.split('.')[0]
                    annotation_file = f"{base_filename}.txt"
                    for split in ['train', 'val', 'test']:
                        annotation_path = os.path.join(yolov8_labels_base, split, annotation_file)
                        if os.path.exists(annotation_path):
                            # Process and copy the image
                            new_image_name = f"{camera}_{image_file}"
                            dest_file_path = os.path.join(temp_dir, new_image_name)
                            image_split_dir = os.path.join(yolov8_images_base, split)
                            final_image_path = os.path.join(image_split_dir, new_image_name)

                            # Load, undistort, and save the image
                            frame_id = base_filename
                            img_buf, _ = dataset.undistort_image_v2(seq_id, frame_id)
                            camera_index = dataset.camera_names.index(camera)
                            undistorted_img = img_buf[camera_index]
                            cv2.imwrite(dest_file_path, cv2.cvtColor(undistorted_img, cv2.COLOR_RGB2BGR))

                            # Copy to final destination
                            os.makedirs(image_split_dir, exist_ok=True)
                            shutil.copy2(dest_file_path, final_image_path)
                            logging.info(f"Processed and copied {dest_file_path} to {final_image_path}")
                            break
            else:
                logging.warning(f"Source camera directory does not exist: {src_camera_dir}")

def main():
    dataset_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov8 Structure\V2\dataset'
    original_dataset_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\data'
    split_files_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\ImageSets'
    temp_dir = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\temp_images'
    yolov8_labels_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V5\dataset\labels'
    yolov8_images_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V5\dataset\images'
    dataset = ONCE(dataset_root=r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet")
    cameras = ['cam01', 'cam03', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']

    train_ids = get_sequence_ids(os.path.join(split_files_dir, 'train.txt'))
    val_ids = get_sequence_ids(os.path.join(split_files_dir, 'val.txt'))
    test_ids = get_sequence_ids(os.path.join(split_files_dir, 'test.txt'))

    # Process images based on annotations
    process_images_based_on_annotations(dataset, original_dataset_dir, temp_dir, yolov8_labels_base, yolov8_images_base, train_ids + val_ids + test_ids, cameras)

if __name__ == '__main__':
    main()
