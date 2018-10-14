import copy

def add_piece(board, piece, coord):
    off_x, off_y = coord
    for cy, row in enumerate(piece):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] += val
    return board


def remove_piece(board, piece, coord):
    off_x, off_y = coord
    for cy, row in enumerate(piece):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] -= val
    return board

def remove_full_rows(board):
    rows = []
    new_board = copy.copy(board)
    height = len(new_board) - 1
    width = len(new_board[0])
    for h in range(height):
        if 0 not in new_board[h]:
            rows.append((h, new_board.pop(h)))
            new_board = [[0]*width] + new_board

    return (new_board, rows)

def insert_rows(board, rows):
    new_board = copy.copy(board[len(rows):])
    for h, row in rows:
        new_board.insert(h, row)
    return new_board

def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def getMaxWidth(piece):
    return max([len(x) for x in piece])


def join_matrixes(mat1, mat2, mat2_off):
    result = copy.copy(mat1)
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


