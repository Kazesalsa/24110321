import time
import random
import math
from .common import PuzzleState, manhattan_distance, get_board_tuple

def solve_hill_climbing(start_board, goal_board):
    current_state = PuzzleState(start_board)
    current_state.h = manhattan_distance(start_board, goal_board)
    
    nodes_expanded = 0
    start_time = time.time()
    
    while current_state.board != goal_board:
        neighbors = current_state.get_neighbors()
        nodes_expanded += 1
        
        # Đánh giá heuristic bằng Manhattan cho tất cả neighbors
        best_neighbor = None
        best_h = float('inf')
        
        for neighbor in neighbors:
            neighbor.h = manhattan_distance(neighbor.board, goal_board)
            if neighbor.h < best_h:
                best_h = neighbor.h
                best_neighbor = neighbor
                
        # Nếu không có neighbor nào tốt hơn trạng thái hiện tại (hoặc bằng), ta bị kẹt ở cực trị cục bộ
        if best_h >= current_state.h:
            # Gặp Local Maxima (Minima), thoát ra không có kết quả
            return None, nodes_expanded, time.time() - start_time
            
        current_state = best_neighbor
        
    return current_state, nodes_expanded, time.time() - start_time

def solve_simulated_annealing(start_board, goal_board):
    current_state = PuzzleState(start_board)
    current_state.h = manhattan_distance(start_board, goal_board)
    
    nodes_expanded = 0
    start_time = time.time()
    
    T = 100.0  # Nhiệt độ ban đầu
    cooling_rate = 0.99
    
    # Để tránh chạy vĩnh viễn, đặt số vòng lặp tối đa
    for _ in range(50000):
        if current_state.board == goal_board:
            return current_state, nodes_expanded, time.time() - start_time
            
        T *= cooling_rate
        if T < 0.0001:
            break
            
        neighbors = current_state.get_neighbors()
        nodes_expanded += 1
        
        if not neighbors:
            break
            
        # Chọn ngẫu nhiên 1 hàng xóm
        next_state = random.choice(neighbors)
        next_state.h = manhattan_distance(next_state.board, goal_board)
        
        delta_e = next_state.h - current_state.h
        
        # Nếu tốt hơn (delta_e < 0 vì ta muốn h nhỏ)
        if delta_e < 0:
            current_state = next_state
        else:
            # Nếu xấu hơn, chấp nhận với một xác suất
            probability = math.exp(-delta_e / T)
            if random.random() < probability:
                current_state = next_state
                
    return None, nodes_expanded, time.time() - start_time

def solve_local_beam(start_board, goal_board, k=3):
    start_state = PuzzleState(start_board)
    start_state.h = manhattan_distance(start_board, goal_board)
    
    beam = [start_state]
    nodes_expanded = 0
    start_time = time.time()
    
    for _ in range(10000):
        next_beam = []
        for state in beam:
            if state.board == goal_board:
                return state, nodes_expanded, time.time() - start_time
                
            neighbors = state.get_neighbors()
            nodes_expanded += 1
            
            for neighbor in neighbors:
                neighbor.h = manhattan_distance(neighbor.board, goal_board)
                next_beam.append(neighbor)
                
        if not next_beam:
            break
            
        # Sắp xếp và chọn k trạng thái tốt nhất
        next_beam.sort(key=lambda x: x.h)
        beam = next_beam[:k]
        
    return None, nodes_expanded, time.time() - start_time
# Bổ sung cơ chế tản nhiệt độ (Cooling Schedule)
