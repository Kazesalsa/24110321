import heapq
import time
from .common import PuzzleState, manhattan_distance, get_board_tuple

def solve_a_star(start_board, goal_board):
    start_state = PuzzleState(start_board)
    start_state.h = manhattan_distance(start_board, goal_board)
    start_state.f = start_state.g + start_state.h
    
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()
    
    nodes_expanded = 0
    start_time = time.time()
    
    while open_set:
        current_state = heapq.heappop(open_set)
        
        if current_state.board == goal_board:
            return current_state, nodes_expanded, time.time() - start_time
            
        board_tuple = get_board_tuple(current_state.board)
        if board_tuple in closed_set:
            continue
            
        closed_set.add(board_tuple)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if get_board_tuple(neighbor.board) in closed_set:
                continue
                
            neighbor.h = manhattan_distance(neighbor.board, goal_board)
            neighbor.f = neighbor.g + neighbor.h
            heapq.heappush(open_set, neighbor)
            
    return None, nodes_expanded, time.time() - start_time

def solve_best_first(start_board, goal_board):
    """Greedy Best-First Search (chỉ dùng h, không quan tâm g)"""
    start_state = PuzzleState(start_board)
    start_state.h = manhattan_distance(start_board, goal_board)
    start_state.f = start_state.h
    
    open_set = []
    heapq.heappush(open_set, start_state)
    closed_set = set()
    
    nodes_expanded = 0
    start_time = time.time()
    
    while open_set:
        current_state = heapq.heappop(open_set)
        
        if current_state.board == goal_board:
            return current_state, nodes_expanded, time.time() - start_time
            
        board_tuple = get_board_tuple(current_state.board)
        if board_tuple in closed_set:
            continue
            
        closed_set.add(board_tuple)
        nodes_expanded += 1
        
        for neighbor in current_state.get_neighbors():
            if get_board_tuple(neighbor.board) in closed_set:
                continue
                
            neighbor.h = manhattan_distance(neighbor.board, goal_board)
            neighbor.f = neighbor.h # Chỉ dùng heuristic
            heapq.heappush(open_set, neighbor)
            
    return None, nodes_expanded, time.time() - start_time
