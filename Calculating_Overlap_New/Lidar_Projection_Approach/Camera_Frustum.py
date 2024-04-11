import numpy as np
from math import atan, degrees
import cv2

class CameraFrustum:
    def __init__(self, intrinsic_matrix, extrinsic_matrix, near_plane, far_plane, image_size, h_fov, v_fov, distortion_coeffs):
        self.intrinsic_matrix = intrinsic_matrix
        self.extrinsic_matrix = extrinsic_matrix
        self.near_plane = near_plane
        self.far_plane = far_plane
        self.image_width, self.image_height = image_size
        self.h_fov = h_fov
        self.v_fov = v_fov
        self.distortion_coeffs = distortion_coeffs
        self.frustum_corners = self.calculate_frustum_corners()

    def calculate_frustum_corners(self):
        aspect_ratio = self.image_width / self.image_height
        h_fov_rad = np.radians(self.h_fov)
        v_fov_rad = np.radians(self.v_fov)

        # Calculate the half-widths and half-heights at the near and far planes
        near_half_height = np.tan(v_fov_rad / 2) * self.near_plane
        near_half_width = aspect_ratio * near_half_height
        far_half_height = np.tan(v_fov_rad / 2) * self.far_plane
        far_half_width = aspect_ratio * far_half_height

        # Define the 8 corners of the frustum
        near_top_left = np.array([-near_half_width, near_half_height, -self.near_plane])
        near_top_right = np.array([near_half_width, near_half_height, -self.near_plane])
        near_bottom_left = np.array([-near_half_width, -near_half_height, -self.near_plane])
        near_bottom_right = np.array([near_half_width, -near_half_height, -self.near_plane])
        far_top_left = np.array([-far_half_width, far_half_height, -self.far_plane])
        far_top_right = np.array([far_half_width, far_half_height, -self.far_plane])
        far_bottom_left = np.array([-far_half_width, -far_half_height, -self.far_plane])
        far_bottom_right = np.array([far_half_width, -far_half_height, -self.far_plane])

        # Combine all corners into one array
        frustum_corners = np.array([
            near_top_left, near_top_right, near_bottom_right, near_bottom_left,
            far_top_left, far_top_right, far_bottom_right, far_bottom_left
        ])

        return frustum_corners

    def position_and_orient_frustum(self):
        # Extract rotation and translation from the extrinsic matrix
        rotation_matrix = self.extrinsic_matrix[:3, :3]
        translation_vector = self.extrinsic_matrix[:3, 3]

        # Initialize a transformed corners array
        transformed_corners = np.zeros_like(self.frustum_corners)

        # Apply rotation and translation to each corner
        for i, corner in enumerate(self.frustum_corners):
            transformed_corner = np.dot(rotation_matrix, corner) + translation_vector
            transformed_corners[i] = transformed_corner

        self.frustum_corners = transformed_corners

    def calculate_original_fov(self):
        # Calculate the horizontal and vertical FOVs from the intrinsic matrix
        f_x = self.intrinsic_matrix[0, 0]  # Focal length in x (pixel units)
        f_y = self.intrinsic_matrix[1, 1]  # Focal length in y (pixel units)

        h_fov = 2 * degrees(atan(self.image_width / (2 * f_x)))
        v_fov = 2 * degrees(atan(self.image_height / (2 * f_y)))

        return h_fov, v_fov

    def calculate_new_fov(self):
        # Calculate the optimal new camera matrix for the undistorted image
        new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(self.intrinsic_matrix, self.distortion_coeffs,
                                                             (self.image_width, self.image_height), 1)

        # Calculate new FOVs based on the new camera matrix
        new_h_fov = 2 * degrees(atan(self.image_width / (2 * new_camera_matrix[0, 0])))
        new_v_fov = 2 * degrees(atan(self.image_height / (2 * new_camera_matrix[1, 1])))

        return new_h_fov, new_v_fov
