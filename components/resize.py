from sys import path
from os.path import dirname
path.append(dirname(__file__))
import components.global_vars as gv
from tkinter import font
from inputting import draw_input 
import time
def resize(event):
    if event.widget == gv.root:
        
        canvas_new_width = int(event.width/1.25)
        canvas_new_height = int(event.height/8)
        gv.canvas.config(width=gv.canvas_new_width, height=gv.canvas_new_height)

        
        available_width = event.width - 50
        font_size = max(10, event.width // 25)
        test_text = "星露谷物語存檔複製小工具"
        current_font = font.Font(family='大波浪圓體 CJK TC-Bold', size=font_size, weight='bold')
        
        while current_font.measure(test_text) > available_width and font_size > 10:
            font_size -= 1
            current_font.configure(size=font_size)
            print(font_size)
        gv.title1.config(font=current_font)
        gv.title2.config(font=current_font)
        gv.title3.config(font=current_font)
        gv.title4.config(font=current_font)
        
        font_size = max(8, event.width //60)
        gv.label_choose.config(font=( gv.ui_font, font_size, 'bold'))
        gv.label_farm.config(font=( gv.ui_font, font_size, 'bold'))
        
        font_size = max(8, event.width //60)
        gv.combo_save.config(font=( gv.ui_font, font_size, ))
        time.sleep(0)
        gv.root.option_add('*TCombobox*Listbox.font', ( gv.ui_font, font_size, 'bold'))