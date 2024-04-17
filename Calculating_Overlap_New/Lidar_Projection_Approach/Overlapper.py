import json
import numpy as np
from once import ONCE

with open(r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Calculating_Overlap_New\Lidar_Projection_Approach\vertices.json', 'r') as file:
    intersection_points = np.array(json.load(file))


# Example usage
dataset = ONCE(r'C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet')
seq_id = "000076"
frame_id = "1616343528200"
vertices = np.array(intersection_points)  # Replace with your vertices
save_path = r'C:\Users\evans\PycharmProjects\pythonProject\Overlap-Part-3\Calculating_Overlap_New\Lidar_Projection_Approach\Data\Basic_Vertice_Images'  # Specify your save path here

projected_img_dict = dataset.project_vertices_to_image(seq_id, frame_id, vertices, save_path)



