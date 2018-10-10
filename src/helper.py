import copy

def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def getMaxWidth(piece):
    return max([len(x) for x in piece])


def join_matrixes(mat1, mat2, mat2_off):
    result = copy.deepcopy(mat1)
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            if result[cy + off_y - 1][cx + off_x] == 0:
                result[cy + off_y - 1][cx + off_x] += val
    return result


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


