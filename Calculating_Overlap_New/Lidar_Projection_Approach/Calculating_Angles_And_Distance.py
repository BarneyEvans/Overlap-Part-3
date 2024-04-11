import numpy as np

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

def distance_calculation(cam1, cam2):
    T1 = cam1.extrinsic_matrix[:, 3]
    T2 = cam2.extrinsic_matrix[:, 3]

    distance = np.linalg.norm(T1 - T2)

    return distance