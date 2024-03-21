import numpy as np
from Cameras import camera5, camera6, camera7, camera8
import math

camera_used_1 = camera7
camera_used_2 = camera8
def distance_calculation(cam1, cam2):
    T1 = cam1.extrinsic_matrix[:, 3]
    T2 = cam2.extrinsic_matrix[:, 3]

    distance = np.linalg.norm(T1 - T2)

    return distance

def extract_angles_from_extrinsic(extrinsic_matrix):
    """
    Extracts Euler angles from a 3x4 or 4x4 extrinsic matrix.
    Assumes the matrix is in the form [R|t] where R is a 3x3 rotation matrix.

    Parameters:
    - extrinsic_matrix: The extrinsic matrix from which to extract the rotation.

    Returns:
    - A tuple of the extracted yaw, pitch, and roll angles in degrees.
    """

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
    """
    Checks the alignment of two cameras based on their extrinsic matrices.

    Parameters:
    - extrinsic1: The extrinsic matrix of the first camera.
    - extrinsic2: The extrinsic matrix of the second camera.
    - leeway: The allowed difference in the non-primary rotation plane angles.

    Throws:
    - An error if the conditions for proper alignment are not met.
    """
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
def overlap_calculation(distance, cam1_hfov, cam2_hfov, cam1_angle, cam2_angle):
    """
    Conceptually estimate the area of overlap between the fields of view of two cameras,
    including the consideration of the distance between the cameras.

    This function provides a conceptual approach and does not implement detailed geometric calculations.
    """
    # Convert all angles from degrees to radians
    cam1_hfov_rad = math.radians(cam1_hfov)
    cam2_hfov_rad = math.radians(cam2_hfov)
    cam1_angle_rad = math.radians(cam1_angle)
    cam2_angle_rad = math.radians(cam2_angle)

    # Placeholder effective range for overlap calculation
    effective_range = 10

    # Calculate if an overlap is likely based on the distance and the angles
    # This is a placeholder condition; actual condition would require detailed geometry
    if distance < effective_range and abs(cam1_angle_rad - cam2_angle_rad) < (cam1_hfov_rad + cam2_hfov_rad) / 2:
        # Simplified calculation of overlap area, assuming some overlap exists
        # Actual calculation should consider the intersection points and shapes
        overlap_area = min(cam1_hfov_rad, cam2_hfov_rad) * distance  # Placeholder calculation
    else:
        overlap_area = 0  # No overlap

    return overlap_area

def calculate_fov_width_at_distance(hfov, distance):
    """
    Calculate the width of the field of view at a certain distance.
    """
    hfov_rad = math.radians(hfov)
    return 2 * distance * math.tan(hfov_rad / 2)

def calculate_overlap_percentage(distance, cam1_hfov, cam2_hfov, angle1, angle2):
    """
    Calculate the percentage of overlap for each camera's field of view.

    Parameters:
    - distance: Distance between the two cameras.
    - cam1_hfov, cam2_hfov: Horizontal field of view for Camera 1 and Camera 2, in degrees.
    - angle1, angle2: Orientation angles for Camera 1 and Camera 2, in degrees.

    Returns:
    A tuple containing the percentage of overlap for Camera 1 and Camera 2.
    """
    # Calculate FOV widths at the intersection distance
    cam1_fov_width = calculate_fov_width_at_distance(cam1_hfov, distance)
    cam2_fov_width = calculate_fov_width_at_distance(cam2_hfov, distance)

    # Determine the angles relative to the line connecting the cameras
    angle1_rad = math.radians(angle1)
    angle2_rad = math.radians(180 - angle2)  # Assuming angle2 is oriented from the opposite direction

    # Calculate the distance from each camera to the intersection line of the FOVs
    intersection_distance_cam1 = distance * math.tan(angle2_rad)
    intersection_distance_cam2 = distance * math.tan(angle1_rad)

    # Calculate the overlap width based on the intersection distances
    overlap_width = min(intersection_distance_cam1, intersection_distance_cam2)

    # Calculate the percentage of overlap for each camera
    overlap_percentage_cam1 = (overlap_width / cam1_fov_width) * 100
    overlap_percentage_cam2 = (overlap_width / cam2_fov_width) * 100

    return overlap_percentage_cam1, overlap_percentage_cam2




camera_distance = distance_calculation(camera_used_1, camera_used_2)
angle1, angle2 = check_camera_alignment(camera_used_1.extrinsic_matrix, camera_used_2.extrinsic_matrix)
a1, a2 = calculate_overlap_percentage(camera_distance, camera_used_1.HF0V, camera_used_2.HF0V, angle1, angle2)
print(a1, a2)
#camera_system = overlap_calculation(camera5, camera6)
