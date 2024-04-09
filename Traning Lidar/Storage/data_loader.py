# data_loader.py
import numpy as np
import json
import os
from glob import glob
from config import DATASET_ROOT


# Load annotations from the JSON file for a given sequence
def load_annotations(sequence_id):
    json_path = os.path.join(DATASET_ROOT, sequence_id, f"{sequence_id}.json")
    if not os.path.isfile(json_path):
        raise FileNotFoundError(f"No annotation file found for sequence {sequence_id}")

    with open(json_path, 'r') as file:
        annotations = json.load(file)

    return annotations


# Load point cloud data from .bin file for a given sequence and frame
def load_point_cloud(sequence_id, frame_id):
    bin_path = os.path.join(DATASET_ROOT, sequence_id, 'lidar_roof', f'{frame_id}.bin')
    if not os.path.isfile(bin_path):
        raise FileNotFoundError(f"No point cloud bin file found for frame {frame_id} in sequence {sequence_id}")

    # Assuming the point cloud data is stored as float32
    points = np.fromfile(bin_path, dtype=np.float32).reshape(-1, 4)

    return points

# If you plan to use the ONCE toolkit, you might not need the second function,
# and instead, you would use the ONCE's load point cloud method.
