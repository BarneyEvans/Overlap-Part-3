from Main import frustum_1, frustum_2
import math
def round_to_5_sigfigs(number):
    if number == 0:
        return 0
    else:
        return round(number, -int(math.floor(math.log10(abs(number))) - 4))

vertices1 = frustum_1.frustum_corners
vertices2 = frustum_2.frustum_corners

print("vertices1 = [")
for vertex in vertices1:
    rounded_vertex = [round_to_5_sigfigs(coord) for coord in vertex]
    print(f"    [{', '.join(str(coord) for coord in rounded_vertex)}],")
print("]")

print("vertices2 = [")
for vertex in vertices2:
    rounded_vertex = [round_to_5_sigfigs(coord) for coord in vertex]
    print(f"    [{', '.join(str(coord) for coord in rounded_vertex)}],")
print("]")
