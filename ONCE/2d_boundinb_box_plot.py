import cv2
import os
from once import ONCE  # Importing the ONCE class or relevant functions from once.py

def process_and_save_2d_boxes(dataset, seq_id, dataset_root, output_directory):
    """
    Process and save 2D boxes for frames that appear in all specified camera paths.
    """
    camera_ids = ["cam01", "cam03", "cam05", "cam06", "cam07", "cam08", "cam09"]
    frame_sets = []

    # Gather frame IDs from all camera paths
    for cam_id in camera_ids:
        cam_path = os.path.join(dataset_root, "data", seq_id, cam_id)
        frame_ids = {filename.split('.')[0] for filename in os.listdir(cam_path) if filename.endswith(".jpg")}
        frame_sets.append(frame_ids)

    # Find common frame IDs across all camera paths
    common_frame_ids = set.intersection(*frame_sets)

    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Process each common frame ID
    for frame_id in common_frame_ids:
        print(frame_id)
        # Use the adapted project_boxes_to_image method
        # Assuming this method is adapted to handle and return an image for a specific frame_id
        img_with_boxes_dict = dataset.project_boxes_to_image(seq_id, frame_id)

        for cam_id, img_with_boxes in img_with_boxes_dict.items():
            if img_with_boxes is not None:
                filename = f"{frame_id}_{cam_id}.jpg"
                output_path = os.path.join(output_directory, filename)
                cv2.imwrite(output_path, img_with_boxes)
                print(f"Saved annotated image to {output_path}")
            else:
                print(f"No boxes drawn for {frame_id} in {cam_id}")

if __name__ == "__main__":
    dataset_root = "C:\\Users\\be1g21\\OneDrive - University of Southampton\\Desktop\\Year 3\\Year 3 Project\\Dataset\\data_root"
    seq_id = "000076"
    output_directory = r'C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\Edited Files'

    dataset = ONCE(dataset_root)
    process_and_save_2d_boxes(dataset, seq_id, dataset_root, output_directory)
