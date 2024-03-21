import numpy as np
from Cameras import camera5, camera6, camera7, camera8

camera_used_1 = camera7
camera_used_2 = camera8
def distance_calculation(cam1, cam2):
    R1, t1 = cam1.extrinsic_matrix[:, :3], cam1.extrinsic_matrix[:, 3]
    R2, t2 = cam2.extrinsic_matrix[:, :3], cam2.extrinsic_matrix[:, 3]

    rotation_matrix = np.dot(R1, R2.T)
    translation_vector = t1 - np.dot(rotation_matrix, t2)

    camera2_position = -np.dot(rotation_matrix.T, translation_vector)

    distance = np.linalg.norm(camera2_position)

    return distance

def get_distance():
    pass


camera_distance = distance_calculation(camera_used_1, camera_used_2)
print(camera_distance)
#camera_system = overlap_calculation(camera5, camera6)
