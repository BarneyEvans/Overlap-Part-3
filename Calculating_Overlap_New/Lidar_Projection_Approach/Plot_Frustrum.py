import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import numpy as np


def plot_frustum(frustum_corners):
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],  # lower square
        [4, 5], [5, 6], [6, 7], [7, 4],  # upper square
        [0, 4], [1, 5], [2, 6], [3, 7]  # vertical lines
    ]

    faces = [
        [frustum_corners[j] for j in [0, 1, 2, 3]],  # bottom face
        [frustum_corners[j] for j in [4, 5, 6, 7]],  # top face
        [frustum_corners[j] for j in [0, 1, 5, 4]],  # side face
        [frustum_corners[j] for j in [1, 2, 6, 5]],  # side face
        [frustum_corners[j] for j in [2, 3, 7, 6]],  # side face
        [frustum_corners[j] for j in [3, 0, 4, 7]]  # side face
    ]

    # Create a 3D plot
    plt.ion()  # Enable interactive mode
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the faces with lighter purple
    face_collection = Poly3DCollection(faces, linewidths=1, edgecolors='darkviolet', facecolors='plum')
    ax.add_collection3d(face_collection)

    # Plot the edges with darker purple
    for edge in edges:
        ax.plot3D(*zip(frustum_corners[edge[0]], frustum_corners[edge[1]]), color='darkviolet')

    # Hide the axes
    ax.set_axis_off()

    # Set the aspect ratio to be equal
    ax.set_box_aspect([np.ptp(i) for i in np.array(frustum_corners).T])  # Ensure frustum_corners is a numpy array

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

    # Hide the axes
    ax.set_axis_off()

    # Set the aspect ratio to be equal
    max_range = np.array([np.ptp(frustum_corners_1, axis=0), np.ptp(frustum_corners_2, axis=0)]).max() / 2.0
    mid_x = (frustum_corners_1[:, 0].max() + frustum_corners_1[:, 0].min()) / 2
    mid_y = (frustum_corners_1[:, 1].max() + frustum_corners_1[:, 1].min()) / 2
    mid_z = (frustum_corners_1[:, 2].max() + frustum_corners_1[:, 2].min()) / 2
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    # Show the plot
    plt.show()