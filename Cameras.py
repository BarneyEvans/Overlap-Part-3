import numpy as np

class Camera:
    def __init__(self, name, intrinsic_matrix, distortion, extrinsic_matrix):
        self.name = name
        self.intrinsic_matrix = intrinsic_matrix
        self.distortion = distortion
        self.extrinsic_matrix = extrinsic_matrix

# Camera 5
camera5 = Camera(
    name="Camera 5",
    intrinsic_matrix=np.array([[956.1788, 0, 942.1158],
                               [0, 957.3191, 534.9691],
                               [0, 0, 1]], dtype="double"),
    distortion=np.array([-0.3223, 0.1121, 0.00013163, -0.0006059, -0.0184], dtype="double"),
    extrinsic_matrix=np.array([[0.6842090902109125, 0.012757768318256146, 0.729174300301576, 0.9349271554284222],
                               [-0.7291952147824502, -0.0037992814583245327, 0.6842951879114569, -1.2496662959908535],
                               [0.011500417867694623, -0.9999113984788539, 0.00670340069892017, -0.9903790922932432],
                               [0, 0, 0, 1]], dtype="double")
)

# Camera 6
camera6 = Camera(
    name="Camera 6",
    intrinsic_matrix=np.array([[960.1722, 0, 930.9725],
                               [0, 961.0462, 527.6315],
                               [0, 0, 1]], dtype="double"),
    distortion=np.array([-0.341, 0.1383, -0.00035166, 0.00023264, -0.0284], dtype="double"),
    extrinsic_matrix=np.array([[-0.525463591505783, 0.0071184770899436756, 0.850786307650613, 0.8263699919401531],
                               [-0.8508081951418305, -8.935304239132691e-05, -0.5254763620711543, 1.6370361027886502],
                               [-0.003664571099697145, -0.9999746593289022, 0.006103410415620236, -0.7769119609339724],
                               [0, 0, 0, 1]], dtype="double")
)

# Camera 7
camera7 = Camera(
    name="Camera 7",
    intrinsic_matrix=np.array([[958.7242, 0, 945.0733],
                               [0, 959.2743, 541.1526],
                               [0, 0, 1]], dtype="double"),
    distortion=np.array([-0.3242, 0.1146, 0.0002508, -0.00031052, -0.0195], dtype="double"),
    extrinsic_matrix=np.array([[-0.5273318034792174, -0.01631569334742189, -0.8495027764462861, -0.8282493982163052],
                               [0.8492717132659491, -0.04032296151382653, -0.5264139206186268, 1.6631609489815502],
                               [-0.025665659657904794, -0.999053480513104, 0.03512003685899612, -0.7729286642791661],
                               [0, 0, 0, 1]], dtype="double")
)

# Camera 8
camera8 = Camera(
    name="Camera 8",
    intrinsic_matrix=np.array([[961.418, 0, 933.048],
                               [0, 961.514, 538.496],
                               [0, 0, 1]], dtype="double"),
    distortion=np.array([-0.3346, 0.1279, 0.0002404, 0.00030117, -0.0239], dtype="double"),
    extrinsic_matrix=np.array([[0.6132847181908445, -0.009673687973318135, -0.789802680544053, -0.9412443183374661],
                               [0.78984828266435, 0.0016348837624844403, 0.6133001039680819, -1.2455806990314335],
                               [-0.004641638261802694, -0.9999518722999012, 0.008643395060306203, -0.9910797743882116],
                               [0, 0, 0, 1]], dtype="double")
)
