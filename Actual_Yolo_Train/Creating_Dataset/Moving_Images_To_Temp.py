import os
import shutil
import logging


def move_corresponding_images(yolov8_labels_base, yolov8_images_base, image_extension='.jpg'):
    """
    Moves images to the corresponding split directories based on where their annotation files are located.

    Args:
    - yolov8_labels_base: Base path for the YOLOv8 labels directory where train, val, and test directories exist.
    - yolov8_images_base: Base path for the YOLOv8 images directory where train, val, and test directories should be created.
    - image_extension: The file extension of the images (e.g., '.jpg').
    """
    # Ensure output directories exist for images
    for split in ['train', 'val', 'test']:
        os.makedirs(os.path.join(yolov8_images_base, split), exist_ok=True)

    # For each split, find annotation files and move the corresponding image files
    for split in ['train', 'val', 'test']:
        label_split_dir = os.path.join(yolov8_labels_base, split)
        image_split_dir = os.path.join(yolov8_images_base, split)

        # Iterate over annotation files in each split
        for annotation_file in os.listdir(label_split_dir):
            # Construct the corresponding image filename
            image_filename = annotation_file.replace('.txt', image_extension)

            # Define source and destination paths
            src_image_path = os.path.join(yolov8_images_base, image_filename)  # Update this path if necessary
            dest_image_path = os.path.join(image_split_dir, image_filename)

            # Move the image file if it exists
            if os.path.exists(src_image_path):
                shutil.copy2(src_image_path, dest_image_path)
                logging.info(f"Moved {src_image_path} to {dest_image_path}")
            else:
                logging.warning(f"Image file does not exist: {src_image_path}")


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Update these paths according to your project structure
    yolov8_labels_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V4\dataset\labels'
    yolov8_images_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V4\dataset\images'  # Base directory where images should be moved

    move_corresponding_images(yolov8_labels_base, yolov8_images_base)


if __name__ == "__main__":
    main()
