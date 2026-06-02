from collections import deque
import time
from .common import PuzzleState, get_board_tuple

def solve_bfs(start_board, goal_board):
    start_state = PuzzleState(start_board)
    
    queue = deque([start_state])
    closed_set = set()
    
    nodes_expanded = 0
    start_time = time.time()
    
    while queue:
        current_state = queue.popleft()
        
        if current_state.board == goal_board:
            return current_state, nodes_expanded, time.time() - start_time
            
        board_tuple = get_board_tuple(current_state.board)
        if board_tuple in closed_set:
            continue
            
        closed_set.add(board_tuple)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if get_board_tuple(neighbor.board) not in closed_set:
                queue.append(neighbor)
                
    return None, nodes_expanded, time.time() - start_time

def solve_dfs(start_board, goal_board, depth_limit=30):
    start_state = PuzzleState(start_board)
    
    stack = [start_state]
    closed_set = set()
    
    nodes_expanded = 0
    start_time = time.time()
    
    while stack:
        current_state = stack.pop()
        
        if current_state.board == goal_board:
            return current_state, nodes_expanded, time.time() - start_time
            
        # Dừng nếu vượt quá độ sâu để tránh tìm đường quá dài làm treo UI
        if current_state.g > depth_limit:
            continue
            
        board_tuple = get_board_tuple(current_state.board)
        if board_tuple in closed_set:
            continue
            
        closed_set.add(board_tuple)
        nodes_expanded += 1
        
        # Đưa các trạng thái kề vào stack
        for neighbor in current_state.get_neighbors():
            if get_board_tuple(neighbor.board) not in closed_set:
                stack.append(neighbor)
                
    return None, nodes_expanded, time.time() - start_time

def solve_iddfs(start_board, goal_board, max_depth=30):
    start_time = time.time()
    total_nodes = 0
    
    for depth in range(max_depth):
        solution, nodes, _ = solve_dfs(start_board, goal_board, depth_limit=depth)
        total_nodes += nodes
        if solution is not None:
            return solution, total_nodes, time.time() - start_time
            
    return None, total_nodes, time.time() - start_time
# Cấu hình Depth Limit cho DFS
# Bổ sung thuật toán IDDFS
