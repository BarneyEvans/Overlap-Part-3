import numpy as np
from once import ONCE
from Calculating_Angles_And_Distance import check_camera_alignment, distance_calculation
from Plot_Frustrum import plot_frustum, plot_two_frustums
from Camera_Frustum import CameraFrustum


def calculate_frustum_intersection(frustum1, frustum2):
    pass
    # Use computational geometry to find the intersection of two frustums
    # This might involve more complex mathematics or the use of a library
    # Return the intersection volume or shape

def extract_information(dataset_root, seq_id, frame_id, cam_name):
    dataset = ONCE(dataset_root)

    split_name = dataset._find_split_name(seq_id)
    frame_info = getattr(dataset, f'{split_name}_info')[seq_id][frame_id]

    camera_calibrations = frame_info['calib']
    cam_calib = camera_calibrations[cam_name]
    intrinsic_matrix = np.array(cam_calib['cam_intrinsic'])
    extrinsic_matrix = np.array(cam_calib['cam_to_velo'])
    distortion_coefficients = cam_calib['distortion'],

    # Assuming camera 7 and 8 have the same FOVs as CAM_3-8
    h_fov = 120  # Horizontal field of view in degrees
    v_fov = 74  # Vertical field of view in degrees (-37 to +37)

    near_plane_distance = 0.1
    far_plane_distance = 100

    image_size = (1920, 1020)

    return intrinsic_matrix, extrinsic_matrix, near_plane_distance, far_plane_distance, h_fov, v_fov, image_size, distortion_coefficients


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




#plot_two_frustums(frustum_1.frustum_corners, frustum_2.frustum_corners)

#print(frustum_1.distortion_coeffs)
#print(frustum_1.calculate_new_fov())
#print(frustum_1.calculate_original_fov())
#print(frustum_2.calculate_new_fov())
#print(frustum_2.calculate_original_fov())

#intersection = calculate_frustum_intersection(camera1.frustum_corners, camera2.frustum_corners)


