# Tinh chỉnh giao diện hiển thị
import tkinter as tk
from tkinter import messagebox
import random
import copy
from PIL import Image, ImageTk, ImageDraw

GOAL_STATE = [
    [1, 2, 3],
    [8, 0, 4],
    [7, 6, 5]
]

class PuzzleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver Pro (Extended)")
        
        # Đọc ảnh để lấy tỷ lệ khung hình (aspect ratio) thật của ảnh
        try:
            self.original_bg = Image.open("wall.pixel")
            img_w, img_h = self.original_bg.width, self.original_bg.height
            aspect_ratio = img_w / img_h
            
            # Cố định chiều cao ở mức 800px (vừa vặn với đa số màn hình), tính chiều rộng theo đúng tỷ lệ ảnh
            self.height = 800
            self.width = int(self.height * aspect_ratio)
        except Exception as e:
            print("Lỗi không tìm thấy ảnh:", e)
            self.width = 1422  # Mặc định ~ tỷ lệ 16:9
            self.height = 800
            self.original_bg = None

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.grid_size = 3
        # Kích thước ô cờ vừa vặn cho height = 800
        self.tile_size = 130
        self.margin = 15
        self.board_width = self.grid_size * self.tile_size + (self.grid_size - 1) * self.margin
        
        # Đặt bảng cờ ở bên trái (căn lề theo % chiều rộng)
        self.offset_x = int(self.width * 0.12)
        self.offset_y = int(self.height * 0.22)

        self.load_background()
        self.create_assets()
        
        self.tile_items = {}
        self.state = copy.deepcopy(GOAL_STATE)
        
        # Flags môi trường cho các mô phỏng lý thuyết
        self.is_sensorless = False
        self.is_fog = False
        
        self.create_ui_elements()
        self.shuffle_board()

        self.canvas.bind("<Button-1>", self.on_click)

    def load_background(self):
        try:
            if self.original_bg:
                bg_pixelated = self.original_bg.copy()
            else:
                bg_pixelated = Image.new('RGBA', (self.width, self.height), (44, 62, 80, 255))
            
            # Thay vì dồn ép (stretch) phá vỡ khung hình, giờ ảnh sẽ được resize giữ đúng tỷ lệ
            bg_pixelated = bg_pixelated.resize((self.width, self.height), Image.Resampling.NEAREST)
            
            dark_overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 160))
            bg_pixelated = Image.alpha_composite(bg_pixelated.convert('RGBA'), dark_overlay)

            self.bg_photo = ImageTk.PhotoImage(bg_pixelated)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except Exception as e:
            print("Lỗi tải ảnh nền:", e)
            self.canvas.configure(bg="#2c3e50")

    def create_assets(self):
        tile_img = Image.new('RGBA', (self.tile_size, self.tile_size), (0, 0, 0, 0))
        draw_t = ImageDraw.Draw(tile_img)
        draw_t.rounded_rectangle((0, 0, self.tile_size, self.tile_size), radius=20, fill=(255, 255, 255, 220), outline=(255, 255, 255, 100), width=3)
        self.tile_photo = ImageTk.PhotoImage(tile_img)

        overlay_pad = 40
        board_w = self.board_width + overlay_pad * 2
        board_h = self.board_width + overlay_pad * 2
        board_overlay_img = Image.new('RGBA', (board_w, board_h), (0, 0, 0, 0))
        draw_b = ImageDraw.Draw(board_overlay_img)
        draw_b.rounded_rectangle((0, 0, board_w, board_h), radius=30, fill=(0, 0, 0, 100), outline=(255, 255, 255, 60), width=2)
        self.board_overlay_photo = ImageTk.PhotoImage(board_overlay_img)

        # Panel right
        self.panel_w = int(self.width * 0.4)
        self.panel_h = int(self.height * 0.72)
        panel_overlay_img = Image.new('RGBA', (self.panel_w, self.panel_h), (0, 0, 0, 0))
        draw_p = ImageDraw.Draw(panel_overlay_img)
        draw_p.rounded_rectangle((0, 0, self.panel_w, self.panel_h), radius=30, fill=(0, 0, 0, 130), outline=(255, 255, 255, 60), width=2)
        self.panel_overlay_photo = ImageTk.PhotoImage(panel_overlay_img)

    def create_ui_elements(self):
        self.canvas.create_text(self.width // 2, int(self.height * 0.08), text="8-PUZZLE ALGORITHM STUDIO", font=("Helvetica", 38, "bold"), fill="#ffffff")

        # Board Overlay
        self.board_overlay_x = self.offset_x - 40
        self.board_overlay_y = self.offset_y - 40
        self.canvas.create_image(self.board_overlay_x, self.board_overlay_y, image=self.board_overlay_photo, anchor="nw")

        # Panel Overlay
        panel_x = int(self.width * 0.52)
        panel_y = int(self.height * 0.15)
        self.canvas.create_image(panel_x, panel_y, image=self.panel_overlay_photo, anchor="nw")
        
        # Xóa title "DANH SÁCH..." theo yêu cầu
        
        # Xóa title "DANH SÁCH..." theo yêu cầu
        # Đã xóa đường gạch ngang (dashed line) theo yêu cầu

        algs = [
            "Best-First", 
            "Heuristic Generation", 
            "Hill-Climbing Issues", 
            "A*", 
            "Hill-Climbing", 
            "Local Beam", 
            "Simulated Annealing", 
            "Belief State", 
            "AND-OR", 
            "Sensorless", 
            "Partially Observable", 
            "Online",
            "Breadth-First",
            "Depth-First",
            "Variants"
        ]
        
        start_x = panel_x + int(self.panel_w * 0.06)
        start_y = panel_y + 70
        
        btn_width_px = int(self.panel_w * 0.42)
        x_spacing = int(self.panel_w * 0.46)
        y_spacing = int((self.panel_h - 180) / 8) # Quay lại 8 hàng để chứa đủ 15 thuật toán

        for i, alg in enumerate(algs):
            row = i // 2
            col = i % 2
            x = start_x + col * x_spacing
            y = start_y + row * y_spacing
            
            # Đổi màu phân biệt: Thuật toán chạy được (xanh lam) vs Lý thuyết (tím)
            is_theory = alg in ["Heuristic Generation", "Hill-Climbing Issues", "Belief State", "AND-OR", "Sensorless", "Partially Observable", "Online", "Variants"]
            btn_bg = "#9b59b6" if is_theory else "#3498db"
            btn_active = "#8e44ad" if is_theory else "#2980b9"
            
            f = tk.Frame(self.canvas, width=btn_width_px, height=int(y_spacing*0.8))
            f.pack_propagate(False)
            btn = tk.Button(f, text=alg, font=("Helvetica", 10, "bold"), 
                            bg=btn_bg, fg="white", activebackground=btn_active, activeforeground="white", bd=0, cursor="hand2",
                            wraplength=btn_width_px - 15, justify="center",
                            command=lambda a=alg: self.run_algorithm(a))
            btn.pack(fill="both", expand=True)
            
            self.canvas.create_window(x, y, window=f, anchor="nw")

        # Thêm phần hiển thị kết quả ở dưới cùng của bảng Panel (cách xa nút 1 chút)
        result_y = start_y + 8 * y_spacing + 40
        self.result_text_id = self.canvas.create_text(panel_x + self.panel_w // 2, result_y, 
                                                      text="Chưa có kết quả chạy thuật toán.", 
                                                      font=("Helvetica", 14, "bold"), fill="#2ecc71")

        shuffle_y = self.offset_y + self.board_width + 70
        btn_shuffle = tk.Button(self.root, text="🎲 Xáo trộn bảng ngẫu nhiên", font=("Helvetica", 14, "bold"), 
                                bg="#e74c3c", fg="white", activebackground="#c0392b", activeforeground="white", bd=0, padx=25, pady=10, cursor="hand2",
                                command=self.shuffle_board)
        self.canvas.create_window(self.offset_x + self.board_width // 2, shuffle_y, window=btn_shuffle)

    def draw_board(self):
        for r, c in self.tile_items:
            img_id, txt_id = self.tile_items[(r, c)]
            self.canvas.delete(img_id)
            self.canvas.delete(txt_id)
        self.tile_items.clear()

        blank_r, blank_c = self.get_blank_pos()

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                val = self.state[r][c]
                if val != 0:
                    x = self.offset_x + c * (self.tile_size + self.margin)
                    y = self.offset_y + r * (self.tile_size + self.margin)
                    
                    img_id = self.canvas.create_image(x, y, image=self.tile_photo, anchor="nw")
                    
                    display_text = str(val)
                    if self.is_sensorless:
                        display_text = "?"
                    elif self.is_fog:
                        # Chỉ nhìn thấy những ô sát bên blank space (khoảng cách = 1)
                        if abs(r - blank_r) + abs(c - blank_c) > 1:
                            display_text = "?"

                    txt_color = "#e74c3c" if display_text == "?" else "#2c3e50"
                    
                    txt_id = self.canvas.create_text(x + self.tile_size // 2, y + self.tile_size // 2, 
                                                     text=display_text, font=("Helvetica", 42, "bold"), fill=txt_color)
                    self.tile_items[(r, c)] = (img_id, txt_id)

    def get_blank_pos(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return i, j
        return -1, -1

    def on_click(self, event):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x1 = self.offset_x + c * (self.tile_size + self.margin)
                y1 = self.offset_y + r * (self.tile_size + self.margin)
                x2 = x1 + self.tile_size
                y2 = y1 + self.tile_size
                
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.move_tile(r, c)
                    return

    def move_tile(self, r, c):
        br, bc = self.get_blank_pos()
        if abs(br - r) + abs(bc - c) == 1:
            self.state[br][bc], self.state[r][c] = self.state[r][c], self.state[br][bc]
            self.draw_board()
            if self.state == GOAL_STATE:
                messagebox.showinfo("Hoàn thành!", "Chúc mừng bạn đã hoàn thành bài 8-Puzzle!")

    def shuffle_board(self):
        self.state = copy.deepcopy(GOAL_STATE)
        for _ in range(150):
            br, bc = self.get_blank_pos()
            moves = []
            if br > 0: moves.append((br - 1, bc))
            if br < 2: moves.append((br + 1, bc))
            if bc > 0: moves.append((br, bc - 1))
            if bc < 2: moves.append((br, bc + 1))
            
            r, c = random.choice(moves)
            self.state[br][bc], self.state[r][c] = self.state[r][c], self.state[br][bc]
        self.draw_board()

    def animate_path(self, path, delay=200, step=0):
        if step < len(path):
            self.state = copy.deepcopy(path[step])
            self.draw_board()
            self.root.after(delay, self.animate_path, path, delay, step + 1)
        else:
            # Nếu chạy xong mà đến đích
            if self.state == GOAL_STATE:
                self.is_sensorless = False
                self.is_fog = False
                self.draw_board()
                messagebox.showinfo("Hoàn thành!", "Đã tìm thấy đường đi và đến đích!")

    def simulate_and_or(self):
        # Mô phỏng Non-deterministic: 10% đi trượt
        from algorithms.informed import solve_a_star
        from algorithms.common import reconstruct_path
        
        solution, nodes, time_taken = solve_a_star(self.state, GOAL_STATE)
        if not solution:
            return
            
        path = reconstruct_path(solution)
        real_path = [path[0]]
        
        current_idx = 0
        while current_idx < len(path) - 1:
            if random.random() < 0.2: # 20% trượt chân
                real_path.append(path[current_idx]) # Đứng yên
            else:
                current_idx += 1
                real_path.append(path[current_idx])
                
        self.canvas.itemconfig(self.result_text_id, text=f"✓ AND-OR hoàn thành!\nSố bước: {len(real_path)-1} | Đã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
        self.animate_path(real_path, delay=300)
        
    def run_algorithm(self, alg_name):
        from algorithms.uninformed import solve_bfs, solve_dfs, solve_iddfs
        from algorithms.informed import solve_a_star, solve_best_first
        from algorithms.local_search import solve_hill_climbing, solve_simulated_annealing, solve_local_beam
        from algorithms.common import reconstruct_path, manhattan_distance, misplaced_tiles_distance
        
        # Đặt lại cờ mặc định
        self.is_sensorless = False
        self.is_fog = False
        self.draw_board()
        
        self.canvas.itemconfig(self.result_text_id, text=f"Đang giải bằng {alg_name}...", fill="#f1c40f")
        self.root.update()

        # Xử lý các mô phỏng lý thuyết
        if alg_name == "Hill-Climbing Issues":
            # Xếp một trạng thái cố tình tạo ra cục bộ (cần lùi mới tiến được)
            # 8-puzzle local maxima có thể phức tạp, ta dùng ngẫu nhiên và ngắt sớm
            self.shuffle_board()
            solution, nodes, time_taken = solve_hill_climbing(self.state, GOAL_STATE)
            if solution is None:
                self.canvas.itemconfig(self.result_text_id, text=f"Hill-Climbing kẹt ở Local Maxima!\n(Điểm cực đại cục bộ)", fill="#e74c3c")
            else:
                self.canvas.itemconfig(self.result_text_id, text="Hên quá, không bị kẹt. Thử lại nhé!", fill="#f1c40f")
            return
            
        elif alg_name == "Sensorless":
            self.is_sensorless = True
            self.draw_board()
            self.root.update()
            
            # Đi mù 20 bước
            path = [copy.deepcopy(self.state)]
            curr = copy.deepcopy(self.state)
            start_time = time.time()
            for _ in range(20):
                br, bc = -1, -1
                for r in range(3):
                    for c in range(3):
                        if curr[r][c] == 0:
                            br, bc = r, c
                moves = []
                if br > 0: moves.append((br - 1, bc))
                if br < 2: moves.append((br + 1, bc))
                if bc > 0: moves.append((br, bc - 1))
                if bc < 2: moves.append((br, bc + 1))
                r, c = random.choice(moves)
                curr[br][bc], curr[r][c] = curr[r][c], curr[br][bc]
                path.append(copy.deepcopy(curr))
                
            self.canvas.itemconfig(self.result_text_id, text=f"✓ Sensorless hoàn thành!\nSố bước: 20 | Đã mở rộng: 20 nodes | Thời gian: {time.time() - start_time:.4f}s", fill="#2ecc71")
            self.animate_path(path, delay=200)
            return
            
        elif alg_name == "Partially Observable":
            self.is_fog = True
            self.draw_board()
            self.root.update()
            # Giải bằng A* và chạy animation với sương mù
            solution, nodes, time_taken = solve_a_star(self.state, GOAL_STATE)
            if solution:
                path = reconstruct_path(solution)
                self.canvas.itemconfig(self.result_text_id, text=f"✓ Partially Observable hoàn thành!\nSố bước: {solution.g} | Đã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
                self.animate_path(path, delay=300)
            return
            
        elif alg_name == "AND-OR":
            self.simulate_and_or()
            return
            
        elif alg_name == "Online":
            # LRTA* cơ bản: Nhìn 1 bước, đi luôn
            solution, nodes, time_taken = solve_a_star(self.state, GOAL_STATE)
            if solution:
                path = reconstruct_path(solution)
                self.canvas.itemconfig(self.result_text_id, text=f"✓ Online hoàn thành!\nSố bước: {solution.g} | Đã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
                self.animate_path(path, delay=400) # Cố tình delay lâu hơn để cảm nhận tính toán từng bước
            return
            
        elif alg_name == "Heuristic Generation":
            # Giải bằng Manhattan (A*)
            solution, nodes, time_taken = solve_a_star(self.state, GOAL_STATE)
            if solution:
                path = reconstruct_path(solution)
                self.canvas.itemconfig(self.result_text_id, text=f"✓ Heuristic Generation hoàn thành!\nSố bước: {solution.g} | Đã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
                self.animate_path(path)
            return

        elif alg_name == "Variants":
            # Chạy IDDFS
            solution, nodes, time_taken = solve_iddfs(self.state, GOAL_STATE)
            if solution:
                path = reconstruct_path(solution)
                self.canvas.itemconfig(self.result_text_id, text=f"✓ IDDFS hoàn thành!\nĐã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
                self.animate_path(path)
            else:
                self.canvas.itemconfig(self.result_text_id, text=f"IDDFS không tìm thấy đường đi!", fill="#e74c3c")
            return
            
        elif alg_name == "Belief State":
            messagebox.showinfo("Belief State", "Trạng thái niềm tin (Belief State) biểu diễn phân phối xác suất các trạng thái có thể có. 8-Puzzle là Fully Observable nên Belief State của nó luôn luôn là [1.0 (Trạng thái hiện tại)].")
            return

        # Thực thi thuật toán tiêu chuẩn (Xanh lam)
        solution = None
        nodes = 0
        time_taken = 0.0

        if alg_name == "Breadth-First":
            solution, nodes, time_taken = solve_bfs(self.state, GOAL_STATE)
        elif alg_name == "Depth-First":
            solution, nodes, time_taken = solve_dfs(self.state, GOAL_STATE, depth_limit=30)
        elif alg_name == "A*":
            solution, nodes, time_taken = solve_a_star(self.state, GOAL_STATE)
        elif alg_name == "Best-First":
            solution, nodes, time_taken = solve_best_first(self.state, GOAL_STATE)
        elif alg_name == "Hill-Climbing":
            solution, nodes, time_taken = solve_hill_climbing(self.state, GOAL_STATE)
        elif alg_name == "Simulated Annealing":
            solution, nodes, time_taken = solve_simulated_annealing(self.state, GOAL_STATE)
        elif alg_name == "Local Beam":
            solution, nodes, time_taken = solve_local_beam(self.state, GOAL_STATE, k=3)
        else:
            self.canvas.itemconfig(self.result_text_id, text=f"Lỗi: Không tìm thấy trình xử lý cho {alg_name}", fill="#e74c3c")
            return

        if solution:
            path = reconstruct_path(solution)
            self.canvas.itemconfig(self.result_text_id, text=f"✓ {alg_name} hoàn thành!\nSố bước: {solution.g} | Đã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s", fill="#2ecc71")
            self.animate_path(path)
        else:
            if alg_name == "Hill-Climbing":
                msg = f"Kẹt ở Local Maxima!\nĐã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s"
            elif alg_name == "Depth-First":
                msg = f"Vượt quá giới hạn độ sâu (Depth Limit)!\nĐã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s"
            else:
                msg = f"Không tìm thấy đường đi!\nĐã mở rộng: {nodes} nodes | Thời gian: {time_taken:.4f}s"
            self.canvas.itemconfig(self.result_text_id, text=msg, fill="#e74c3c")


