import numpy as np
from Cameras import camera5, camera6, camera7, camera8
import math
import sympy as sp
from sympy import symbols, cos, sin, solveset, Eq, S


camera_used_1 = camera7
camera_used_2 = camera8
def distance_calculation(cam1, cam2):
    T1 = cam1.extrinsic_matrix[:, 3]
    T2 = cam2.extrinsic_matrix[:, 3]

    distance = np.linalg.norm(T1 - T2)

    return distance

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

def calculate_circle_intersections(distance, radii):
    # Define the symbols
    x, y = sp.symbols('x y')

    # Equations of the circles based on the distance and radii
    circle1 = sp.Eq(x**2 + y**2, radii**2)
    circle2 = sp.Eq((x - distance)**2 + y**2, radii**2)

    # Solve the system of equations
    intersection_points = sp.solve((circle1, circle2), (x, y))

    # Round the coordinates to four significant figures
    intersection_points = [(round(float(sp.re(point[0])), 4), round(float(sp.re(point[1])), 4)) for point in intersection_points]
    return intersection_points[1]


def calculate_arc_radius_intersection(distance_between_centres, sector_A_fov, sector_B_fov,
                                      sector_A_displacement_angle, radii_for_both_sectors, stage):
    # Convert angles to radians
    sector_A_displacement_angle_rad = np.radians(sector_A_displacement_angle)

    # Calculate the radius lines for both sectors
    t = symbols('t', real=True)
    # Line equation from center of Sector A (origin), rotated by sector_A_displacement_angle
    line_A_x = t * cos(sector_A_displacement_angle_rad)
    line_A_y = t * sin(sector_A_displacement_angle_rad)

    if stage == 2:
        distance_between_centres *= -1
    # Equation of the circle for Sector B
    circle_B_eq = Eq((line_A_x - distance_between_centres) ** 2 + line_A_y ** 2, radii_for_both_sectors ** 2)

    # Solve for the intersection parameter t
    # We expect two solutions, but only the positive one is within the range of the sector's radius
    t_solution_set = solveset(circle_B_eq, t, domain=S.Reals)
    t_positive = [sol.evalf() for sol in t_solution_set if sol > 0]

    # There should be only one positive solution within the range of the radius
    if t_positive:
        # Substitute the positive t value back into the line equation to get the intersection point
        t_val = t_positive[0]
        intersection_x = line_A_x.subs(t, t_val)
        intersection_y = line_A_y.subs(t, t_val)
        if stage == 1:
            return intersection_x, intersection_y
        else :
            return intersection_x + 3, intersection_y
    else:
        return None


def calculate_area_between_chord_and_arc(chord_point_A, chord_point_B, center_point, radii):
    # Convert inputs to numpy arrays to ensure compatibility with numpy operations
    chord_point_A = np.array(chord_point_A)
    chord_point_B = np.array(chord_point_B)
    center_point = np.array(center_point)

    # Calculate vectors from the center to each chord point
    vector_A = chord_point_A - center_point
    vector_B = chord_point_B - center_point

    # Calculate the angle between vector_A and vector_B using the dot product formula
    dot_product = np.dot(vector_A, vector_B)
    cos_theta = dot_product / (radii ** 2)
    cos_theta = np.float64(cos_theta)
    theta = np.arccos(cos_theta)  # Central angle in radians

    # Calculate the area of the sector
    sector_area = 0.5 * radii ** 2 * theta

    # Calculate the area of the triangle using the sine of theta (since we have a central angle)
    triangle_area = 0.5 * radii ** 2 * np.sin(theta)

    # Calculate the desired area between the chord and the arc
    area_between_chord_and_arc = sector_area - triangle_area

    return area_between_chord_and_arc


def calculate_triangle_area(A, B, C):
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    # Applying the area formula
    area = 0.5 * abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))

    return area


def overlap_calculation(distance, cam1_hfov, cam2_hfov, cam1_angle, cam2_angle, radii_for_both_sectors):

    centerA = (0,0)
    centerB = (0 + distance,0)

    intersect_circles = calculate_circle_intersections(distance, radii_for_both_sectors)

    inteserctA = calculate_arc_radius_intersection(distance, cam1_hfov, cam2_hfov, cam1_angle, radii_for_both_sectors,1)
    intersectB = calculate_arc_radius_intersection(distance, cam2_hfov, cam1_hfov, cam2_angle, radii_for_both_sectors,2)

    chord_1_area = calculate_area_between_chord_and_arc(inteserctA, intersect_circles, centerB, radii_for_both_sectors)
    chord_2_area = calculate_area_between_chord_and_arc(intersectB, intersect_circles, centerA, radii_for_both_sectors)

    triangular_area_1 = calculate_triangle_area(inteserctA, intersect_circles, centerA)
    triangular_area_2 = calculate_triangle_area(intersectB, intersect_circles, centerB)
    triangular_area_3 = calculate_triangle_area(centerA, intersect_circles, centerB)


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





#angle1, angle2 = check_camera_alignment(camera_used_1.extrinsic_matrix, camera_used_2.extrinsic_matrix)
#a1, a2 = calculate_overlap_percentage(camera_distance, camera_used_1.HF0V, camera_used_2.HF0V, angle1, angle2)
#print(a1, a2)
#camera_system = overlap_calculation(camera5, camera6)
overlap_calculation(3,120,120,60,120, 100)
#print(calculate_arc_radius_intersection(3,120,120,60,100))
