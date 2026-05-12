class PuzzleState:
    def __init__(self, board, parent=None, move="", g=0, h=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.g = g  # Chi phí thực tế từ trạng thái ban đầu (số bước)
        self.h = h  # Chi phí heuristic đến đích (luôn dùng Manhattan theo yêu cầu)
        self.f = self.g + self.h # Tổng chi phí

    def __lt__(self, other):
        return self.f < other.f

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j
        return -1, -1

    def get_neighbors(self):
        neighbors = []
        x, y = self.get_blank_pos()
        moves = {'Lên': (-1, 0), 'Xuống': (1, 0), 'Trái': (0, -1), 'Phải': (0, 1)}

        for move, (dx, dy) in moves.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
                neighbors.append(PuzzleState(new_board, self, move, self.g + 1))
        return neighbors

def manhattan_distance(board, goal):
    """Luôn sử dụng khoảng cách Manhattan cho tất cả các thuật toán có heuristic"""
    dist = 0
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val != 0:
                for gx in range(3):
                    for gy in range(3):
                        if goal[gx][gy] == val:
                            dist += abs(i - gx) + abs(j - gy)
    return dist

def get_board_tuple(board):
    return tuple(tuple(row) for row in board)

def misplaced_tiles_distance(board, goal):
    """Sử dụng cho so sánh Heuristic (số ô sai vị trí)"""
    dist = 0
    for i in range(3):
        for j in range(3):
            val = board[i][j]
            if val != 0 and val != goal[i][j]:
                dist += 1
    return dist

def reconstruct_path(final_state):
    path = []
    current = final_state
    while current:
        path.append(current.board)
        current = current.parent
    path.reverse()
    return path
