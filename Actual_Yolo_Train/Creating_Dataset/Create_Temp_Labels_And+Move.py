import json
import os
import logging
import random
import shutil

def get_full_dataset_base_path():
    return r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'

def convert_bbox_to_yolo(box, image_dimensions):
    """
    Converts bounding box coordinates to YOLO format.

    Args:
    - box: A tuple (x1, y1, x2, y2) where (x1, y1) is the top-left corner and (x2, y2) is the bottom-right corner of the box.
    - image_dimensions: The dimensions of the image as a tuple (width, height).

    Returns:
    - A tuple (x_center, y_center, width, height) with the bounding box center coordinates and dimensions in YOLO format.
    """
    x1, y1, x2, y2 = box
    img_width, img_height = image_dimensions

    # Calculate the bounding box width and height in pixels
    box_width = x2 - x1
    box_height = y2 - y1

    # Calculate center coordinates in pixels
    x_center = x1 + (box_width / 2)
    y_center = y1 + (box_height / 2)

    # Normalize the center coordinates and dimensions to be relative to the image size
    x_center /= img_width
    y_center /= img_height
    box_width /= img_width
    box_height /= img_height

    return (x_center, y_center, box_width, box_height)

def load_json_annotations(json_path):
    with open(json_path, 'r') as file:
        return json.load(file)
def process_and_split_annotations(data_dir, temp_annotations_dir, yolov8_labels_base, class_mapping, image_dimensions, cameras):
    # Ensure temporary and final annotation directories are created
    os.makedirs(temp_annotations_dir, exist_ok=True)
    all_annotations = []

    # Process annotations
    for sequence_id in os.listdir(data_dir):
        json_path = os.path.join(data_dir, sequence_id, f"{sequence_id}.json")
        if not os.path.isfile(json_path):
            continue
        annotations = load_json_annotations(json_path)
        for frame in annotations.get("frames", []):
            frame_id = frame["frame_id"]
            for camera in cameras:
                if camera not in frame.get("annos", {}).get("boxes_2d", {}):
                    continue
                boxes_2d = frame.get("annos", {}).get("boxes_2d", {}).get(camera, [])
                if not boxes_2d:
                    continue
                # Updated output file path format to include seq_id and camera
                output_file_path = os.path.join(temp_annotations_dir, f"{sequence_id}_{camera}_{frame_id}.txt")
                all_annotations.append(output_file_path)
                with open(output_file_path, 'w') as file:
                    for name, box in zip(frame.get("annos", {}).get("names", []), boxes_2d):
                        if name not in class_mapping or box[0] == -1.0:
                            continue
                        class_id = class_mapping[name]
                        x_center, y_center, width, height = convert_bbox_to_yolo(box, image_dimensions)
                        file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


    # Shuffle and split annotations
    random.shuffle(all_annotations)
    num_annotations = len(all_annotations)
    train_end = int(num_annotations * 0.8)
    val_end = train_end + int(num_annotations * 0.1)

    splits = {
        "train": all_annotations[:train_end],
        "val": all_annotations[train_end:val_end],
        "test": all_annotations[val_end:],
    }

    # Move annotations to their respective YOLOv8 structure folders
    for split_name, annotation_paths in splits.items():
        split_dir = os.path.join(yolov8_labels_base, split_name)
        os.makedirs(split_dir, exist_ok=True)
        for annotation_path in annotation_paths:
            shutil.move(annotation_path, os.path.join(split_dir, os.path.basename(annotation_path)))
            logging.info(f"Moved annotation to {split_dir}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    full_dataset_base = get_full_dataset_base_path()
    data_dir = os.path.join(full_dataset_base, 'data')
    temp_annotations_dir = os.path.join(full_dataset_base, "temp")
    yolov8_labels_base = os.path.join(full_dataset_base, "Yolov8 Structure", "V6", "dataset", "labels")

    class_mapping = {"Car": 0, "Truck": 1, "Cyclist": 2, "Pedestrian": 3, "Bus": 4}
    image_dimensions = (1920, 1080)
    cameras = ["cam01", "cam03","cam05, cam06", "cam07", "cam08", "cam09"]

    process_and_split_annotations(data_dir, temp_annotations_dir, yolov8_labels_base, class_mapping, image_dimensions, cameras)

    logging.info("Processing complete.")

if __name__ == "__main__":
    main()
