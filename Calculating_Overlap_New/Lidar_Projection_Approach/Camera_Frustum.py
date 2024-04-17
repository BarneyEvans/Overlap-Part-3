import numpy as np
from math import atan, degrees
import cv2


class CameraFrustum:
    def __init__(self, intrinsic_matrix, extrinsic_matrix, near_plane, far_plane, image_size, h_fov, v_fov,
                 distortion_coeffs):
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

        near_half_height = np.tan(v_fov_rad / 2) * self.near_plane
        near_half_width = aspect_ratio * near_half_height
        far_half_height = np.tan(v_fov_rad / 2) * self.far_plane
        far_half_width = aspect_ratio * far_half_height

        frustum_corners = np.array([
            [-near_half_width, near_half_height, -self.near_plane],
            [near_half_width, near_half_height, -self.near_plane],
            [near_half_width, -near_half_height, -self.near_plane],
            [-near_half_width, -near_half_height, -self.near_plane],
            [-far_half_width, far_half_height, -self.far_plane],
            [far_half_width, far_half_height, -self.far_plane],
            [far_half_width, -far_half_height, -self.far_plane],
            [-far_half_width, -far_half_height, -self.far_plane]
        ])

        return frustum_corners

    def position_and_orient_frustum(self):
        # Extract rotation and translation from the extrinsic matrix
        rotation_matrix = self.extrinsic_matrix[:3, :3]
        translation_vector = self.extrinsic_matrix[:3, 3]

        # Apply rotation and translation to all corners at once
        self.frustum_corners = np.dot(self.frustum_corners, rotation_matrix.T) + translation_vector

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

    def transform_to_camera_coords(self, points):
        # Convert points from world coordinates to camera coordinates
        homogeneous_points = np.hstack((points, np.ones((points.shape[0], 1))))
        camera_coords = np.dot(self.extrinsic_matrix, homogeneous_points.T).T
        return camera_coords[:, :3]

    def project_to_2d(self, points):
        # Apply the intrinsic matrix to project points to the image plane
        homogeneous_image_points = np.dot(self.intrinsic_matrix, np.hstack((points, np.ones((points.shape[0], 1)))).T)
        # Normalize by the third (z) coordinate to get 2D image coordinates
        image_points = (homogeneous_image_points[:2, :] / homogeneous_image_points[2, :]).T
        return image_points

    def undistort_points(self, points):
        # Correct for lens distortion
        undistorted_points = cv2.undistortPoints(np.expand_dims(points, axis=1), self.intrinsic_matrix,
                                                 self.distortion_coeffs, P=self.intrinsic_matrix)
        return undistorted_points.reshape(-1, 2)

    def project_to_image(self, points, image_path):
        # Load the image
        image = cv2.imread(image_path)

        # Transform the 3D intersection points to camera coordinates
        camera_coords = self.transform_to_camera_coords(points)

        # Project to 2D points on the image plane
        image_points = self.project_to_2d(camera_coords)

        # Correct for lens distortion
        image_points = self.undistort_points(image_points)

        # Draw the points on the image
        for point in image_points:
            if 0 <= point[0] < self.image_width and 0 <= point[1] < self.image_height:
                cv2.circle(image, tuple(point.astype(int)), 3, (0, 255, 0), -1)

        return image
