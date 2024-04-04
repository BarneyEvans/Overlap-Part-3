import os


class ONCE:
    def __init__(self, data_root):
        self.data_root = data_root
        self.image_sets_dir = os.path.join(self.data_root, 'ImageSets')
        self.data_dir = os.path.join(self.data_root, 'data')
        self.cameras = ['cam01', 'cam03', 'cam05', 'cam06', 'cam07', 'cam08', 'cam09']
        self.seq_ids = {
            'train_split.txt': ['000076', '000080', '000092', '000104', '000113', '000121'],
            'val_split.txt': ['000027', '000028', '000112', '000201'],
            'test_split.txt': ['000034', '000077', '000168', '000200', '000273', '000275', '000303', '000318', '000322',
                               '000334']
        }

    def create_directories(self):
        # Create ImageSets directory and split files
        os.makedirs(self.image_sets_dir, exist_ok=True)
        for split_file, ids in self.seq_ids.items():
            with open(os.path.join(self.image_sets_dir, split_file), 'w') as f:
                f.write('\n'.join(ids))

        # Create data directory with sequence IDs and camera/lidar_roof directories
        for _, seq_ids in self.seq_ids.items():
            for seq_id in seq_ids:
                seq_path = os.path.join(self.data_dir, seq_id)
                # Create camera directories
                for cam in self.cameras:
                    cam_path = os.path.join(seq_path, cam)
                    os.makedirs(cam_path, exist_ok=True)
                # Create lidar_roof directory
                lidar_path = os.path.join(seq_path, 'lidar_roof')
                os.makedirs(lidar_path, exist_ok=True)


def main():
    once = ONCE(data_root=r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet')  # Update this path as needed
    once.create_directories()


if __name__ == "__main__":
    main()
