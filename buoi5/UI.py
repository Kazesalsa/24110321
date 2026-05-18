import tkinter as tk
import random

state = list(range(9))
while True:
    random.shuffle(state)

root = tk.Tk()
root.title("8 Puzzle")
buttons = []

def cập_nhật_giao_diện():
    for i, so in enumerate(state):
        buttons[i].config(text=str(so) if so != 0 else "")
    if state == [1, 2, 3, 4, 5, 6, 7, 8, 0]:
        root.title("Bạn đã thắng!")

def bam_nut(vt):
    trong = state.index(0)
    if abs(vt // 3 - trong // 3) + abs(vt % 3 - trong % 3) == 1:
        state[trong], state[vt] = state[vt], state[trong]
        cập_nhật_giao_diện()

for i in range(9):
    btn = tk.Button(root, font=("Arial", 20), width=5, height=2, command=lambda x=i: bam_nut(x))
    btn.grid(row=i//3, column=i%3)
    buttons.append(btn)

cập_nhật_giao_diện()
root.mainloop()