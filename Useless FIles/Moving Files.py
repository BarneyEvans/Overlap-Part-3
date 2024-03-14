import os
import shutil

def copy_jpg_files(source_folder, destination_folder):
    # Ensure the source and destination folders exist
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Iterate through files in the source folder
    for filename in os.listdir(source_folder):
        # Check if the file is a JPEG
        if filename.lower().endswith('.jpg'):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            # Copy the file to the destination folder
            shutil.copy2(source_file, destination_file)
            print(f"Copied '{filename}' to '{destination_folder}'.")

# Replace these paths with your source and destination folders
source_folder = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\ONCE Data\cam07\cam08"
destination_folder = r"C:\Users\be1g21\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Dataset\data_root\data\000076\cam08"

copy_jpg_files(source_folder, destination_folder)
