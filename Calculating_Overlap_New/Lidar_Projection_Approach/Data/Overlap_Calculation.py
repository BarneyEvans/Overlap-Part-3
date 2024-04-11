import open3d as o3d
import numpy as np

# Vertices for Frustum 1 and Frustum 2
vertices_1 = np.array([
    [-0.66972897, 1.59229844, -0.84808419],
    [-0.81932822, 1.83322913, -0.85536531],
    [-0.81686927, 1.83930624, -0.70479715],
    [-0.66727002, 1.59837555, -0.69751603],
    [157.69217916, -69.19934393, -75.92845449],
    [8.09292598, 171.73134376, -83.20956951],
    [10.55187734, 177.80844995, 67.35858979],
    [160.15113052, -63.12223774, 74.63970481]
])

vertices_2 = np.array([
    [-0.94998467, -1.41882391, -1.0666375],
    [-0.77600136, -1.19475111, -1.06795429],
    [-0.77454343, -1.19499751, -0.91725073],
    [-0.94852674, -1.41907031, -0.91593394],
    [-9.68159896, -174.48879327, -76.54880226],
    [164.30171709, 49.58400574, -77.86559296],
    [165.75964644, 49.33761108, 72.83796369],
    [-8.22366961, -174.73518793, 74.1547544]
])

# Faces for each frustum, assuming that the first 4 vertices form the base and the last 4 form the top
# Each face is defined by indices of the vertices forming its corners
faces = np.array([
    [0, 1, 2], [0, 2, 3],  # Near plane
    [4, 5, 6], [4, 6, 7],  # Far plane
    [0, 3, 7], [0, 7, 4],  # Side faces
    [3, 2, 6], [3, 6, 7],
    [2, 1, 5], [2, 5, 6],
    [1, 0, 4], [1, 4, 5]
])

# Create mesh for Frustum 1
mesh1 = o3d.geometry.TriangleMesh()
mesh1.vertices = o3d.utility.Vector3dVector(vertices_1)
mesh1.triangles = o3d.utility.Vector3iVector(faces)
mesh1.compute_vertex_normals()

# Create mesh for Frustum 2
mesh2 = o3d.geometry.TriangleMesh()
mesh2.vertices = o3d.utility.Vector3dVector(vertices_2)
mesh2.triangles = o3d.utility.Vector3iVector(faces)
mesh2.compute_vertex_normals()

# Compute the intersection of the two frustums (this might be an approximation)
# Open3D does not directly support mesh intersection. You may need to look for additional libraries
# or perform the intersection analysis through external tools or custom code.

# Visualize the meshes (remove the intersection mesh if you're unable to compute it)
o3d.visualization.draw_geometries([mesh1, mesh2])

# If you were able to compute the intersection mesh, you could then calculate its volume like this:
# intersection_volume = intersection_mesh.get_volume()
# print(f"The volume of the intersection is: {intersection_volume}")
