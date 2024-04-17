import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np


def plot_frustum(frustum_corners):
    print("Frustum Input Coordinate Format:")
    print(frustum_corners)
    print()

    # Define frustum edges for line drawing
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # lower square
        (4, 5), (5, 6), (6, 7), (7, 4),  # upper square
        (0, 4), (1, 5), (2, 6), (3, 7)  # vertical lines
    ]

    # Print the coordinates of the frustum corners
    print("Frustum Corner Coordinates:")
    for i, corner in enumerate(frustum_corners):
        print(f"Corner {i}: {corner}")

    # Print the coordinates of the frustum edges
    print("\nFrustum Edge Coordinates:")
    for edge in edges:
        start, end = frustum_corners[edge[0]], frustum_corners[edge[1]]
        print(f"Edge {edge}: Start {start}, End {end}")

    # Print the frustum face indices
    faces = [
        [0, 1, 2, 3],  # bottom face
        [4, 5, 6, 7],  # top face
        [0, 1, 5, 4],  # side face
        [1, 2, 6, 5],  # side face
        [2, 3, 7, 6],  # side face
        [3, 0, 4, 7]  # side face
    ]

    print("\nFrustum Face Indices:")
    for i, face in enumerate(faces):
        print(f"Face {i}: {face}")

    # Create a 3D plot
    plt.ion()  # Interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Add faces to the plot
    face_collection = Poly3DCollection([frustum_corners[face] for face in faces],
                                       linewidths=1, edgecolors='r', alpha=0.1)

    print("\nFrustum Face Coordinates:")
    for i, face in enumerate(faces):
        # Extract the corner points for the current face
        face_corners = [frustum_corners[idx] for idx in face]
        print(f"Face {i} coordinates: {face_corners}")

    ax.add_collection3d(face_collection)

    # Add edges to the plot
    for edge in edges:
        ax.plot3D(*zip(frustum_corners[edge[0]], frustum_corners[edge[1]]), color='r')

    # Setting plot limits - may need adjustment based on frustum size
    max_extent = np.array([np.ptp(frustum_corners[:, i]) for i in range(3)]).max() / 2
    mid = np.mean(frustum_corners, axis=0)
    ax.set_xlim(mid[0] - max_extent, mid[0] + max_extent)
    ax.set_ylim(mid[1] - max_extent, mid[1] + max_extent)
    ax.set_zlim(mid[2] - max_extent, mid[2] + max_extent)

    # Labels and aspect ratio
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')
    ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio

    # Show the plot
    plt.show()


def plot_two_frustums(frustum_corners_1, frustum_corners_2):
    # Define edges for line drawing
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # lower square
        [4, 5], [5, 6], [6, 7], [7, 4],  # upper square
        [0, 4], [1, 5], [2, 6], [3, 7]  # vertical lines
    ]

    def plot_frustum(ax, frustum_corners, edge_color, face_color):
        faces = [
            [frustum_corners[j] for j in [0, 1, 2, 3]],  # bottom face
            [frustum_corners[j] for j in [4, 5, 6, 7]],  # top face
            [frustum_corners[j] for j in [0, 1, 5, 4]],  # side face
            [frustum_corners[j] for j in [1, 2, 6, 5]],  # side face
            [frustum_corners[j] for j in [2, 3, 7, 6]],  # side face
            [frustum_corners[j] for j in [3, 0, 4, 7]]  # side face
        ]
        # Plot the faces with lighter color
        face_collection = Poly3DCollection(faces, linewidths=1, edgecolors=edge_color, facecolors=face_color,
                                           alpha=0.25)
        ax.add_collection3d(face_collection)

        # Plot the edges with darker color
        for edge in edges:
            ax.plot3D(*zip(frustum_corners[edge[0]], frustum_corners[edge[1]]), color=edge_color)

    # Create a 3D plot
    plt.ion()  # Enable interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the first frustum
    plot_frustum(ax, frustum_corners_1, 'darkblue', 'blue')

    # Plot the second frustum
    plot_frustum(ax, frustum_corners_2, 'darkgreen', 'green')

    max_range = np.array([np.ptp(frustum_corners_1, axis=0), np.ptp(frustum_corners_2, axis=0)]).max() / 2.0
    mid_x = np.mean([frustum_corners_1[:, 0].mean(), frustum_corners_2[:, 0].mean()])
    mid_y = np.mean([frustum_corners_1[:, 1].mean(), frustum_corners_2[:, 1].mean()])
    mid_z = np.mean([frustum_corners_1[:, 2].mean(), frustum_corners_2[:, 2].mean()])
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Show the plot
    plt.show()


def plot_two_frustums_with_intersection_points(frustum_corners_1, frustum_corners_2, intersection_points):
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # lower square
        [4, 5], [5, 6], [6, 7], [7, 4],  # upper square
        [0, 4], [1, 5], [2, 6], [3, 7]  # vertical lines
    ]

    def plot_frustum(ax, frustum_corners, edge_color, face_color):
        faces = [
            [frustum_corners[j] for j in [0, 1, 2, 3]],  # bottom face
            [frustum_corners[j] for j in [4, 5, 6, 7]],  # top face
            [frustum_corners[j] for j in [0, 1, 5, 4]],  # side face
            [frustum_corners[j] for j in [1, 2, 6, 5]],  # side face
            [frustum_corners[j] for j in [2, 3, 7, 6]],  # side face
            [frustum_corners[j] for j in [3, 0, 4, 7]]  # side face
        ]
        face_collection = Poly3DCollection(faces, linewidths=1, edgecolors=edge_color, facecolors=face_color,
                                           alpha=0.25)
        ax.add_collection3d(face_collection)

        for edge in edges:
            ax.plot3D(*zip(frustum_corners[edge[0]], frustum_corners[edge[1]]), color=edge_color)

    plt.ion()  # Enable interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plot_frustum(ax, frustum_corners_1, 'darkblue', 'blue')
    plot_frustum(ax, frustum_corners_2, 'darkgreen', 'green')

    # Plot intersection points
    if intersection_points is not None:
        for point in intersection_points:
            ax.scatter(*point, color='black', s=50)  # s is the size of the point

    ax.set_axis_off()

    max_range = np.array([np.ptp(frustum_corners_1, axis=0), np.ptp(frustum_corners_2, axis=0)]).max() / 2.0
    mid_x = np.mean([frustum_corners_1[:, 0].mean(), frustum_corners_2[:, 0].mean()])
    mid_y = np.mean([frustum_corners_1[:, 1].mean(), frustum_corners_2[:, 1].mean()])
    mid_z = np.mean([frustum_corners_1[:, 2].mean(), frustum_corners_2[:, 2].mean()])
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    plt.show()


def plot_intersection_points(edge_intersections):
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D

    # Assuming 'edge_intersections' contains your intersection points
    # Convert the intersection points to a NumPy array for easier manipulation
    intersection_points = np.array(edge_intersections)

    # Create a new figure for 3D plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract x, y, z coordinates from the intersection points
    x_coords = intersection_points[:, 0]
    y_coords = intersection_points[:, 1]
    z_coords = intersection_points[:, 2]

    # Plot the points
    ax.scatter(x_coords, y_coords, z_coords, c='r', marker='o')

    # Set labels according to the axes
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')

    # Set title
    ax.set_title('3D Plot of Intersection Points')

    # Show the plot
    plt.show()


def plot_planes_and_points(plane_equations_1, plane_equations_2, edge_intersections):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Function to create a plane from a point and a normal vector
    def plane_from_point_and_normal(point, normal, size=1):
        d = -point.dot(normal)
        xx, yy = np.meshgrid(np.linspace(-size, size, 10), np.linspace(-size, size, 10))
        zz = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]
        return xx, yy, zz

    # Plot the planes of the first frustum
    for plane_eq in plane_equations_1:
        point = np.array([0, 0, -plane_eq[3] / plane_eq[2]])  # assuming the plane passes through z=0
        xx, yy, zz = plane_from_point_and_normal(point, plane_eq[:3], size=5)
        ax.plot_surface(xx, yy, zz, alpha=0.3, color='blue')

    # Plot the planes of the second frustum
    for plane_eq in plane_equations_2:
        point = np.array([0, 0, -plane_eq[3] / plane_eq[2]])  # assuming the plane passes through z=0
        xx, yy, zz = plane_from_point_and_normal(point, plane_eq[:3], size=5)
        ax.plot_surface(xx, yy, zz, alpha=0.3, color='red')

    # Plot each intersection point
    for point in edge_intersections:
        ax.scatter(point[0], point[1], point[2], color='r', s=50)  # 'r' is the color red, 's' is the size of the point

    # Set labels
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    # Set title
    ax.set_title('3D Intersection Points and Frustum Planes')

    # Show the plot
    plt.show()

def plot_lines_and_planes(intersection_lines, frustum_planes, ax):
    # Plot each intersection line
    for line_point, line_dir in intersection_lines:
        # Create a line segment centered at the intersection point, extending in both directions
        line_length = 2  # You can adjust this as needed
        line = np.array([line_point - line_dir * line_length / 2, line_point + line_dir * line_length / 2])
        ax.plot3D(*line.T, color='red')

    # Plot each plane as a large, semi-transparent square
    plane_size = 2  # Adjust as necessary
    for plane_eq in frustum_planes:
        point_on_plane = -plane_eq[3] / np.linalg.norm(plane_eq[:3]) * plane_eq[:3]
        d1, d2 = np.eye(3)[np.argsort(np.abs(plane_eq[:3]))[:2]]
        square = np.array([point_on_plane + d1 * plane_size + d2 * plane_size,
                           point_on_plane + d1 * plane_size - d2 * plane_size,
                           point_on_plane - d1 * plane_size - d2 * plane_size,
                           point_on_plane - d1 * plane_size + d2 * plane_size])
        ax.add_collection3d(Poly3DCollection([square], facecolors='cyan', linewidths=0.5, alpha=0.1))

    return ax


frustum_corners1 = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]
])

frustum_corners2 = np.array([
    [0.5, 0.5, -0.5],
    [1.5, 0.5, -0.5],
    [1.5, 1.5, -0.5],
    [0.5, 1.5, -0.5],
    [0.5, 0.5, 0.5],
    [1.5, 0.5, 0.5],
    [1.5, 1.5, 0.5],
    [0.5, 1.5, 0.5]
])

plot_two_frustums(frustum_corners1, frustum_corners2)
