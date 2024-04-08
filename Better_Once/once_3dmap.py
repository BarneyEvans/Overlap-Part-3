from once import ONCE
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_lidar_with_boxes(points, boxes_3d, output_path):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1, c=points[:, 3], cmap='viridis')

    for box in boxes_3d:
        cx, cy, cz, l, w, h, theta = box
        rot_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                               [np.sin(theta), np.cos(theta), 0],
                               [0, 0, 1]])
        corners = np.array([[l/2, w/2, h/2], [l/2, -w/2, h/2], [-l/2, -w/2, h/2], [-l/2, w/2, h/2],
                            [l/2, w/2, -h/2], [l/2, -w/2, -h/2], [-l/2, -w/2, -h/2], [-l/2, w/2, -h/2]])
        corners_rotated = np.dot(corners, rot_matrix)
        corners_rotated += np.array([cx, cy, cz])
        ax.plot([corners_rotated[i][0] for i in range(8)], [corners_rotated[i][1] for i in range(8)], zs=[corners_rotated[i][2] for i in range(8)], color="r")

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.savefig(output_path)
    plt.show()
    plt.close()

def main():
    dataset_root = r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet'
    output_directory = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Better_Once\Images'
    dataset = ONCE(dataset_root)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    seq_id = "000076"
    frame_id = "1616343528200"

    points = dataset.load_point_cloud(seq_id, frame_id)
    boxes_img_dict = dataset.project_boxes_to_image(seq_id, frame_id)

    for cam_name, img in boxes_img_dict.items():
        img_path = os.path.join(output_directory, f'{cam_name}_{frame_id}_boxes.jpg')
        cv2.imwrite(img_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

    frame_anno = dataset.get_frame_anno(seq_id, frame_id)
    if frame_anno and 'boxes_3d' in frame_anno:
        boxes_3d = np.array(frame_anno['boxes_3d'])
        plot_path = os.path.join(output_directory, f'{seq_id}_{frame_id}_lidar_3d.png')
        plot_lidar_with_boxes(points[:, :4], boxes_3d, plot_path)
    else:
        print("No 3D bounding box annotations available for this frame.")

if __name__ == '__main__':
    main()
