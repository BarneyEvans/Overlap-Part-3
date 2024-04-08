import json
import os
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

def load_json_annotations(json_path):
    """
    Loads JSON annotations for a sequence ID.
    """
    with open(json_path, 'r') as file:
        return json.load(file)

def save_yolo_annotations(annotations, output_dir, class_mapping, image_dimensions):
    """
    Saves YOLO formatted annotations for all frames and cameras.
    """
    for frame in annotations.get("frames", []):
        frame_id = frame["frame_id"]
        for camera, boxes_2d in frame.get("annos", {}).get("boxes_2d", {}).items():
            if not boxes_2d:
                continue
            output_file_path = os.path.join(output_dir, f"{camera}_{frame_id}.txt")
            with open(output_file_path, 'w') as file:
                for name, box in zip(frame.get("annos", {}).get("names", []), boxes_2d):
                    if name not in class_mapping or box[0] == -1.0:
                        continue  # Skip if class not recognized or invalid box
                    # Normalize and format bounding box
                    class_id = class_mapping[name]
                    x_center, y_center, width, height = convert_bbox_to_yolo(box, image_dimensions)
                    file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")
                logging.info(f"Annotations saved to {output_file_path}")

def convert_bbox_to_yolo(box, image_dimensions):
    """
    Converts bounding box coordinates to YOLO format.
    """
    x1, y1, x2, y2 = box
    width = image_dimensions[0]
    height = image_dimensions[1]
    dw = 1. / width
    dh = 1. / height
    x = (x1 + x2) / 2.0
    y = (y1 + y2) / 2.0
    w = x2 - x1
    h = y2 - y1
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return x, y, w, h


def main():
    # This should point to the directory that contains 'ImageSets' and 'data'.
    full_dataset_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'

    # Path to the YOLOv8 dataset structure.
    yolov8_dataset_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Yolov8 Structure\V2\dataset'

    # Now we point to the correct location of the ImageSets directory.
    split_files_dir = os.path.join(full_dataset_base, 'ImageSets')

    class_mapping = {"Car": 0, "Truck": 1, "Cyclist": 2, "Pedestrian": 3, "Bus": 4}
    image_dimensions = (1920, 1080)  # Assuming all images have the same dimensions

    # Make sure the ImageSets directory exists and contains the split files.
    if not os.path.exists(split_files_dir) or not os.listdir(split_files_dir):
        logging.error(f"Split files are missing in the directory: {split_files_dir}")
        return

    # Iterate through each sequence ID to process annotations
    for sequence_id in os.listdir(os.path.join(full_dataset_base, 'data')):
        json_path = os.path.join(full_dataset_base, 'data', sequence_id, f"{sequence_id}.json")
        if not os.path.isfile(json_path):
            logging.warning(f"JSON file not found for sequence ID: {sequence_id}")
            continue
        annotations = load_json_annotations(json_path)

        # Determine split based on sequence ID
        split = "train" if sequence_id in get_sequence_ids(os.path.join(split_files_dir, "train_split.txt")) else \
            "val" if sequence_id in get_sequence_ids(os.path.join(split_files_dir, "val_split.txt")) else \
                "test" if sequence_id in get_sequence_ids(os.path.join(split_files_dir, "test_split.txt")) else None
        if split is None:
            logging.warning(f"Sequence ID {sequence_id} is not listed in any split.")
            continue

        output_dir = os.path.join(yolov8_dataset_base, "labels", split)

        # Save annotations in YOLO format
        save_yolo_annotations(annotations, output_dir, class_mapping, image_dimensions)

if __name__ == "__main__":
    main()
