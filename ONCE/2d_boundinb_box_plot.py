import cv2
import os
from once import ONCE  # Importing the ONCE class or relevant functions from once.py



def process_and_save_2d_boxes(dataset, seq_id, cam_path, output_directory):
    """
    For each image in the specified camera path, draw 2D bounding boxes and save the output.
    """
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through each image file in the specified camera path
    for filename in os.listdir(cam_path):
        if filename.endswith(".jpg"):
            frame_id = filename.split('.')[0]  # Extract frame_id from filename
            print(frame_id)
            # Now use the adapted project_boxes_to_image method
            img_with_boxes = dataset.project_boxes_to_image(seq_id, frame_id)
            # Assuming it returns an image array with boxes drawn

            output_path = os.path.join(output_directory, filename)
            cv2.imwrite(output_path, img_with_boxes)
            print(f"Saved annotated image to {output_path}")



if __name__ == "__main__":
    dataset_root = "C:\\Users\\be1g21\\OneDrive - University of Southampton\\Desktop\\Year 3\\Year 3 Project\\Dataset\\data_root"
    seq_id = "000076"
    cam_path = os.path.join(dataset_root, "data", seq_id, "cam07")
    output_directory = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\Edited Files'

    dataset = ONCE(dataset_root)
    process_and_save_2d_boxes(dataset, seq_id, cam_path, output_directory)

