from sys import path
from os.path import dirname
path.append(dirname(__file__))
import components.global_vars as gv

resize_timer = None

def on_window_trigger():
    global resize_timer
    
    if resize_timer is not None:
        gv.root.after_cancel(resize_timer)
        
    resize_timer = gv.root.after(150, lambda: perform_final_resize())

def perform_final_resize():
    import inputting
    class VirtualEvent:
        def __init__(self, w, h):
            self.width = w
            self.height = h
    v_event = VirtualEvent(gv.canvas.winfo_width(), gv.canvas.winfo_height())
    
    inputting.draw_input()