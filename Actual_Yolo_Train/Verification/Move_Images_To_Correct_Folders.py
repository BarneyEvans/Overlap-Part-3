import os
import shutil

def analyze_dataset(images_base, labels_base, splits):
    """Analyze the dataset to prepare for corrections."""
    # Gather files by split
    images = {split: set(os.listdir(os.path.join(images_base, split))) for split in splits}
    labels = {split: set(os.listdir(os.path.join(labels_base, split))) for split in splits}

    # Find images with labels in different splits or without labels
    misplaced_images = {}
    orphan_images = set()

    for split in splits:
        for img_file in images[split]:
            base_name = os.path.splitext(img_file)[0]
            found = False

            for label_split, label_files in labels.items():
                label_name = f"{base_name}.txt"
                if label_name in label_files:
                    found = True
                    if split != label_split:
                        misplaced_images.setdefault(split, []).append((img_file, label_split))
                    break

            if not found:
                orphan_images.add(os.path.join(images_base, split, img_file))

    return misplaced_images, orphan_images

def correct_dataset_structure(misplaced_images, orphan_images, images_base):
    """Correct the dataset structure based on analysis."""
    # Move misplaced images to their correct split directories
    for current_split, img_info_list in misplaced_images.items():
        for img_file, correct_split in img_info_list:
            src_path = os.path.join(images_base, current_split, img_file)
            dest_path = os.path.join(images_base, correct_split, img_file)
            shutil.move(src_path, dest_path)
            print(f"Moved {img_file} from {current_split} to {correct_split}")

    # Remove orphan images
    for img_path in orphan_images:
        os.remove(img_path)
        print(f"Removed orphan image: {img_path}")

def main():
    images_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\images'
    labels_base = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet\Yolov8 Structure\V6\dataset\labels'
    splits = ['train', 'val', 'test']

    # Analyze the dataset
    misplaced_images, orphan_images = analyze_dataset(images_base, labels_base, splits)

    # Correct the dataset structure based on the analysis
    correct_dataset_structure(misplaced_images, orphan_images, images_base)

if __name__ == "__main__":
    main()
