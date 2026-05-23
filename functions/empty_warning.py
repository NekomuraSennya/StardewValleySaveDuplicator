import tkinter as tk

def empty_warning(root, canvas, color):
    global canvas_color
    canvas_color = [247, 0, 0]
    v_event = tk.Event()
    v_event.width = canvas.winfo_width()
    v_event.height = canvas.winfo_height()
    from functions.inputting import draw_speech
    root.after(17, lambda:canvas_change_color())
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
            root.after(17, lambda:canvas_change_color())
        draw_speech(v_event, canvas, color, canvas_color, is_empty_warning=True)