    # calculate the length of the tour
#     mark = [[0 for i in range(nodeCount)] for i in range(1 << nodeCount)]
#     def generateSubset(seed):
#         subset = list()
#         for i in range(1, nodeCount):
#             if ((seed & (1 << i)) >> i) == 1:
#                 subset.append((seed & ~(1 << i), i))
#         return subset
#     def cost(_id, j):
#         subsets = generateSubset(_id)
#         if mark[_id][j] > 0:
#             return mark[_id][j]
#         if len(subsets) == 0: 
#             return length(points[0], points[j])
#         _min = sys.maxsize
#         id_min = 0
#         eliminated = 0
#         for subset in subsets:
#             subset_value = cost(subset[0], subset[1])
# #            print('{0:b}'.format(subset[0]) + ' ' + str(subset[1]) + ' ' + str(subset_value))
#             if (_min > subset_value + length(points[j], points[subset[1]])):
#                 _min = subset_value + length(points[j], points[subset[1]])
#                 id_min = subset[0]
#                 eliminated = subset[1]
# #                temp = 
#         print('{0:b}'.format(id_min) + ' ' + str(eliminated) + ' ' + str(_min))
#         mark[id_min][eliminated] = _min
#         return _min
#     obj = cost((1 << nodeCount) - 2, 1)
from collections import namedtuple
import math
import random

Point = namedtuple("Point", ['x', 'y'])
Swap = namedtuple("Swapmove", ['i', 'j', 'delta'])
_print = False
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def calculate_obj(solution, points, nodeCount):
    return sum([length(points[solution[i]], points[solution[i+1]]) for i in range(nodeCount - 1)]) + length(points[solution[nodeCount-1]], points[solution[0]])

def readData(file_location):
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split('\n')
    nodeCount = int(lines[0])
    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    return nodeCount, points

def getNeighborhood(nodeCount, k):
    # randomly get k neiborhood from cur_solution
    node = [i for i in range(nodeCount)]
    neiborhood = []
    if k == -1:
        # get all pairs of node
        for i in range(nodeCount):
            for j in range(i+1, nodeCount):
                if i != j:
                    neiborhood.append((i, j))
        random.shuffle(neiborhood)
        print(len(neiborhood))
        return neiborhood
    while(len(neiborhood) < k):
        n1 = random.randint(0, len(node) - 1)
        node.pop(n1)
        n2 = random.randint(0, len(node) - 1)
        node.pop(n2)
        neiborhood.append((n1, n2))
    return neiborhood

def getSwapDelta(i, j, cur_solution, points, nodeCount):
    delta = 0.0
    delta += \
        - getLength(i, i-1, cur_solution, points, nodeCount, i, j) - getLength(i, i+1, cur_solution, points, nodeCount, i, j) \
        - getLength(j, j-1, cur_solution, points, nodeCount, i, j) - getLength(j, j+1, cur_solution, points, nodeCount, i, j) \
        + getLength(j, i-1, cur_solution, points, nodeCount, i, j) + getLength(j, i+1, cur_solution, points, nodeCount, i, j) \
        + getLength(i, j+1, cur_solution, points, nodeCount, i, j) + getLength(i, j-1, cur_solution, points, nodeCount, i, j)
    return delta

def getLength(i, j, cur_solution, points, nodeCount, i0, j0):
    if i == nodeCount:
        i = 0
    if j == nodeCount:
        j = 0
    if i == -1:
        i = nodeCount - 1
    if j == -1:
        j = nodeCount - 1
    if (i == i0 and j == j0) or (i == j0 and j == i0): 
        return 0.0
    return length(points[cur_solution[i]], points[cur_solution[j]])


nodeCount, points = readData("data/tsp_280_1")
# solution = [1 , 2 , 242 , 243 , 244 , 241 , 240 , 239 , 238 , 237 , 236 , 235 , 234 , 233 , 232 , 231 , 246 , 245 , 247 , 250 , 251 , 230 , 229 , 228 , 227 , 226 , 225 , 224 , 223 , 222 , 221 , 220 , 219 , 218 , 217 , 216 , 215 , 214 , 213 , 212 , 211 , 210 , 207 , 206 , 205 , 204 , 203 , 202 , 201 , 198 , 197 , 196 , 195 , 194 , 193 , 192 , 191 , 190 , 189 , 188 , 187 , 186 , 185 , 184 , 183 , 182 , 181 , 176 , 180 , 179 , 150 , 178 , 177 , 151 , 152 , 156 , 153 , 155 , 154 , 129 , 130 , 131 , 20 , 21 , 128 , 127 , 126 , 125 , 124 , 123 , 122 , 121 , 120 , 119 , 157 , 158 , 159 , 160 , 175 , 161 , 162 , 163 , 164 , 165 , 166 , 167 , 168 , 169 , 170 , 172 , 171 , 173 , 174 , 107 , 106 , 105 , 104 , 103 , 102 , 101 , 100 , 99 , 98 , 97 , 96 , 95 , 94 , 93 , 92 , 91 , 90 , 89 , 109 , 108 , 110 , 111 , 112 , 88 , 87 , 113 , 114 , 115 , 117 , 116 , 86 , 85 , 84 , 83 , 82 , 81 , 80 , 79 , 78 , 77 , 76 , 75 , 74 , 73 , 72 , 71 , 70 , 69 , 68 , 67 , 66 , 65 , 64 , 58 , 57 , 56 , 55 , 54 , 53 , 52 , 51 , 50 , 49 , 48 , 47 , 46 , 45 , 44 , 59 , 63 , 62 , 118 , 61 , 60 , 43 , 42 , 41 , 40 , 39 , 38 , 37 , 36 , 35 , 34 , 33 , 32 , 31 , 30 , 29 , 28 , 27 , 26 , 22 , 25 , 23 , 24 , 14 , 15 , 13 , 12 , 11 , 10 , 9 , 8 , 7 , 6 , 5 , 4 , 277 , 276 , 275 , 274 , 273 , 272 , 271 , 16 , 17 , 18 , 19 , 132 , 133 , 134 , 270 , 269 , 135 , 136 , 268 , 267 , 137 , 138 , 139 , 149 , 148 , 147 , 146 , 145 , 199 , 200 , 144 , 143 , 142 , 141 , 140 , 266 , 265 , 264 , 263 , 262 , 261 , 260 , 259 , 258 , 257 , 254 , 253 , 208 , 209 , 252 , 255 , 256 , 249 , 248 , 278 , 279 , 3 , 280]
# solution = [i - 1 for i in solution]
# print(solution)
# solution = [62, 58, 56, 57, 63, 83, 82, 87, 111, 179, 144, 199, 201, 195, 194, 193, 97, 96, 95, 94, 77, 81, 112, 113, 118, 136, 266, 263, 253, 254, 251, 208, 252, 28, 38, 48, 51, 52, 53, 43, 115, 85, 84, 64, 67, 68, 69, 72, 73, 163, 185, 145, 146, 142, 141, 140, 147, 138, 265, 264, 262, 261, 260, 274, 275, 276, 277, 230, 231, 225, 224, 223, 212, 211, 206, 205, 207, 246, 243, 242, 247, 248, 259, 273, 14, 23, 13, 12, 11, 5, 4, 0, 279, 2, 3, 27, 49, 50, 47, 42, 119, 148, 218, 222, 221, 220, 219, 217, 216, 215, 268, 133, 132, 22, 24, 19, 131, 18, 17, 16, 15, 270, 257, 209, 210, 213, 214, 226, 232, 236, 235, 234, 233, 172, 105, 107, 109, 110, 158, 258, 278, 1, 241, 240, 239, 244, 229, 228, 227, 204, 267, 20, 127, 126, 125, 124, 29, 34, 35, 36, 37, 46, 54, 55, 44, 45, 39, 40, 41, 121, 120, 178, 198, 200, 197, 170, 169, 91, 90, 102, 171, 164, 187, 188, 186, 162, 161, 173, 106, 104, 103, 101, 100, 168, 152, 129, 130, 134, 135, 149, 177, 150, 151, 154, 153, 128, 21, 25, 26, 66, 70, 71, 65, 59, 30, 31, 32, 33, 117, 116, 114, 159, 174, 160, 184, 183, 182, 181, 180, 175, 176, 157, 156, 155, 269, 272, 8, 6, 7, 9, 10, 271, 139, 191, 190, 189, 165, 89, 108, 88, 80, 78, 79, 93, 92, 98, 99, 167, 166, 192, 196, 202, 203, 143, 75, 76, 74, 86, 137, 256, 255, 249, 245, 238, 237, 250, 123, 122, 60, 61]
# # for i, j in getNeighborhood(nodeCount, -1):
# #     delta = getSwapDelta(i, j, solution, points, nodeCount)
# #     if delta < 0:
# #         print(i, j, delta)
# print(getSwapDelta(1, 43, solution, points, nodeCount))
# print(calculate_obj(solution, points, nodeCount))
print(length(points[263], points[184]))