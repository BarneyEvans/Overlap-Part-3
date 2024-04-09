# dataset_splitter.py

import os
import shutil
from sklearn.model_selection import train_test_split
from config import (
    OUTPUT_ROOT,
    TRAIN_IMAGE_DIR,
    VAL_IMAGE_DIR,
    TEST_IMAGE_DIR,
    TRAIN_LABEL_DIR,
    VAL_LABEL_DIR,
    TEST_LABEL_DIR,
    TRAIN_SIZE,
    VAL_SIZE
)


def move_files(files, destination):
    """
    Move files to a destination directory, creating it if it doesn't exist.
    """
    if not os.path.exists(destination):
        os.makedirs(destination)

    for file in files:
        shutil.move(file, destination)


def split_dataset(image_files, label_files):
    """
    Split the dataset into train, val, and test sets and move the files.
    """
    # Ensure the same order by sorting both lists
    image_files.sort()
    label_files.sort()

    # Splitting the data
    image_train, image_test, label_train, label_test = train_test_split(
        image_files, label_files, test_size=1 - TRAIN_SIZE - VAL_SIZE, random_state=42
    )
    image_train, image_val, label_train, label_val = train_test_split(
        image_train, label_train, test_size=VAL_SIZE / (TRAIN_SIZE + VAL_SIZE), random_state=42
    )

    # Move files
    move_files(image_train, TRAIN_IMAGE_DIR)
    move_files(image_val, VAL_IMAGE_DIR)
    move_files(image_test, TEST_IMAGE_DIR)
    move_files(label_train, TRAIN_LABEL_DIR)
    move_files(label_val, VAL_LABEL_DIR)
    move_files(label_test, TEST_LABEL_DIR)


def get_all_files_from_dir(file_dir, extension=""):
    """
    Retrieve all files from a directory with the given extension.
    """
    return [os.path.join(file_dir, f) for f in os.listdir(file_dir) if f.endswith(extension)]


def run_split():
    """
    The function to be called to perform the dataset split.
    """
    bev_images = get_all_files_from_dir(os.path.join(OUTPUT_ROOT, 'bev_images'), extension=".png")
    labels = get_all_files_from_dir(os.path.join(OUTPUT_ROOT, 'labels'), extension=".txt")

    split_dataset(bev_images, labels)


if __name__ == "__main__":
    run_split()
