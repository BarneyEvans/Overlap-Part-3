import numpy as np

# Coordinates of the first camera
x1, y1, z1 = -0.8282493982163052, 1.6631609489815502, -0.7729286642791661

# Coordinates of the second camera
x2, y2, z2 = -0.9412443183374661, -1.2455806990314335, -0.9910797743882116

# Calculate the Euclidean distance between the two points
distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

print("Distance between the two cameras:", distance)
