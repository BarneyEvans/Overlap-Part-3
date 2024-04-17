import numpy as np
from once import ONCE
from Plot_Frustrum import plot_frustum, plot_two_frustums
from Camera_Frustum import CameraFrustum
import json


def extract_information(dataset_root, seq_id, frame_id, cam_name):
    dataset = ONCE(dataset_root)

    # Ensure the new FOV and intrinsics function is defined and being used correctly
    h_fov, v_fov, new_intrinsic_matrix = dataset.get_new_fovs_and_intrinsics(seq_id, frame_id, cam_name)

    # Properly using the refined or existing method to get frame information
    frame_info = dataset.get_frame_info(seq_id, frame_id)
    cam_calib = frame_info['calib'][cam_name]

    # Extracting extrinsic matrix and distortion coefficients correctly
    extrinsic_matrix = np.array(cam_calib['cam_to_velo'])
    distortion_coefficients = np.array(cam_calib['distortion'])  # ensure this is an array, not a tuple

    # Setting near and far plane distances based on typical LiDAR range
    near_plane_distance = 0.3
    far_plane_distance = 200

    # Assuming image size is constant; make sure this aligns with actual image dimensions used
    image_size = (1920, 1020)

    return new_intrinsic_matrix, extrinsic_matrix, near_plane_distance, far_plane_distance, h_fov, v_fov, image_size, distortion_coefficients


dataset_root = r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet"
seq_id = "000076"
frame_id = "1616343528200"
cameras = ["cam07", "cam08"]
intrinsic_matrix1, extrinsic_matrix1, near_plane1, far_plane1, h_fov1, v_fov1, image_size1, dc1 = extract_information(dataset_root, seq_id, frame_id, cameras[0])
intrinsic_matrix2, extrinsic_matrix2, near_plane2, far_plane2, h_fov2, v_fov2, image_size2, dc2 = extract_information(dataset_root, seq_id, frame_id, cameras[1])

frustum_1 = CameraFrustum(intrinsic_matrix1, extrinsic_matrix1, near_plane1, far_plane1, image_size1, h_fov1, v_fov1, dc1)
frustum_2 = CameraFrustum(intrinsic_matrix2, extrinsic_matrix2, near_plane2, far_plane2, image_size2, h_fov1, v_fov1, dc2)

frustum_1.position_and_orient_frustum()
frustum_2.position_and_orient_frustum()




#plot_frustum(frustum_2.frustum_corners)

#plot_two_frustums(frustum_1.frustum_corners, frustum_2.frustum_corners)

#calculate_frustum_intersection(frustum_1.frustum_corners, frustum_2.frustum_corners)

#print(frustum_1.distortion_coeffs)
#print(frustum_1.calculate_new_fov())
#print(frustum_1.calculate_original_fov())
#print(frustum_2.calculate_new_fov())
#print(frustum_2.calculate_original_fov())

#intersection = calculate_frustum_intersection(camera1.frustum_corners, camera2.frustum_corners)


