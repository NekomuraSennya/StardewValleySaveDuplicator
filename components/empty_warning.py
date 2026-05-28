from sys import path
from os.path import dirname
path.append(dirname(__file__))
import components.global_vars as gv
import tkinter as tk
from inputting import draw_speech

def empty_warning():
    canvas_color = [247, 0, 0]
    v_event = tk.Event()
    v_event.width = gv.canvas.winfo_width()
    v_event.height = gv.canvas.winfo_height()
    gv.root.after(17, lambda:canvas_change_color())
    def canvas_change_color():
        if canvas_color[1]<237:
            canvas_color[1] += 7
            if canvas_color[1] > 237: canvas_color[1] = 237
        if canvas_color[2]<198:
            canvas_color[2] += 7
            if canvas_color[2] > 198: canvas_color[2] = 198
        if canvas_color == [247, 237, 198]:
            is_empty_warning= False
        else:
            gv.root.after(17, lambda:canvas_change_color())
        draw_speech(v_event, canvas_color, is_empty_warning=True)