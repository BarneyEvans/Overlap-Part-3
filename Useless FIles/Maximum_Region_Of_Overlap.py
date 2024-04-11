from once import ONCE
import numpy as np

dataset = ONCE(dataset_root=r"C:\Users\evans\OneDrive - University of Southampton\Desktop\Year 3\Year 3 Project\Full_DataSet")

seq_id = "000076"
frame_id = "1616343528200"

frame_anno = dataset.get_frame_anno(seq_id, frame_id)

split_name = dataset._find_split_name(seq_id)
frame_info = getattr(dataset, f'{split_name}_info')[seq_id][frame_id]
camera_calibrations = frame_info['calib']
cams = ["cam07", "cam08"]
extrinsic_matrices = []

for cam_name in cams:
    cam_calib = camera_calibrations[cam_name]
    extrinsic_matrices.append(np.array(cam_calib['cam_to_velo']))

def extract_angles_from_extrinsic(extrinsic_matrix):
    R = extrinsic_matrix[:3, :3]
    sy = np.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)

    singular = sy < 1e-6
    if not singular:
        x = np.arctan2(R[2, 1], R[2, 2])
        y = np.arctan2(-R[2, 0], sy)
        z = np.arctan2(R[1, 0], R[0, 0])
    else:
        x = np.arctan2(-R[1, 2], R[1, 1])
        y = np.arctan2(-R[2, 0], sy)
        z = 0

    return np.rad2deg([x, y, z])


def check_camera_alignment(extrinsic1, extrinsic2, leeway=5.0):
    angles1 = extract_angles_from_extrinsic(extrinsic1)
    angles2 = extract_angles_from_extrinsic(extrinsic2)

    # Check the primary rotation plane (we expect significant difference)
    # Assuming the primary rotation is around the y-axis (yaw)
    primary_plane_idx = 2  # Index 1 for yaw in the angles array
    print(angles1)
    print(angles2)

    if abs(angles1[primary_plane_idx] - angles2[primary_plane_idx]) < leeway:
        print(angles1[primary_plane_idx])
        raise ValueError("Cameras are not significantly rotated in the expected plane.")

    # Check the secondary planes (roll and pitch), where we expect small differences
    for i in [0, 1]:  # Index 0 for roll, Index 2 for pitch in the angles array
        if abs(angles1[i] - angles2[i]) > leeway:
            raise ValueError(f"Cameras have significant rotation differences in the secondary plane: {i}.")

    # If no errors were raised, print the angles for overlap calculation
    print(f"Camera 1 Angles: {angles1}")
    print(f"Camera 2 Angles: {angles2}")
    print("The cameras are aligned correctly for the FOV overlap calculation.")

    # Returning angles for the primary rotation plane for both cameras for further calculations
    return angles1[primary_plane_idx], angles2[primary_plane_idx]


def approximate_overlap(distance, angle1, angle2):
    angle = angle2 - angle1
    area = np.pi * distance * distance
    circle_area = angle / 360
    total_area = area * circle_area
    return total_area

distance = 100  # Replace with actual FOV distance


angle1, angle2 = check_camera_alignment(extrinsic_matrices[0], extrinsic_matrices[1])
overlap_area = approximate_overlap(distance, angle1, angle2)

print(f"Approximate overlap area: {overlap_area}")

