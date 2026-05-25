import os, sys
sys.path.append(os.path.dirname(__file__))

resize_timer = None

def on_window_trigger(root, canvas):
    global resize_timer
    
    if resize_timer is not None:
        root.after_cancel(resize_timer)
        
    resize_timer = root.after(150, lambda: perform_final_resize(root, canvas))

def perform_final_resize(root, canvas):
    import inputting
    class VirtualEvent:
        def __init__(self, w, h):
            self.width = w
            self.height = h
    v_event = VirtualEvent(canvas.winfo_width(), canvas.winfo_height())
    
    inputting.draw_input(root, canvas)