import copy

'''
Adds a piece to the board. The piece and board
are 2D arrays. 
'''


def add_piece(board, piece, coord):
    off_x, off_y = coord
    for cy, row in enumerate(piece):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] += val
    return board


'''
Removes a piece from the board. The piece and board
are 2D arrays. 
'''


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
            new_board = [[0] * width] + new_board

    return (new_board, rows)


def insert_rows(board, rows):
    new_board = copy.copy(board[len(rows):])
    for h, row in rows:
        new_board.insert(h, row)
    return new_board


'''
Performs a 90 degree rotation on a tetromino piece
'''


def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


'''
Gets the width of this piece
The piece is represented as a 2D array
'''


def getMaxWidth(piece):
    return max([len(x) for x in piece])


'''
Checks if there is a collision between the board and 
a piece
'''


def check_collision(board, piece, offset):
    off_x, off_y = offset
    for cy, row in enumerate(piece):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False
