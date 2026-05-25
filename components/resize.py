import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from tkinter import font
from inputting import draw_input 
import time
def resize(event, root, canvas, title1, title2, title3, title4, label_choose, label_farm, combo_save, ui_font):
    if event.widget == root:
        
        canvas_new_width = int(event.width/1.25)
        canvas_new_height = int(event.height/8)
        canvas.config(width=canvas_new_width, height=canvas_new_height)

        
        available_width = event.width - 50
        font_size = max(10, event.width // 25)
        test_text = "星露谷物語存檔複製小工具"
        current_font = font.Font(family='大波浪圓體 CJK TC-Bold', size=font_size, weight='bold')
        
        while current_font.measure(test_text) > available_width and font_size > 10:
            font_size -= 1
            current_font.configure(size=font_size)
            print(font_size)
        title1.config(font=current_font)
        title2.config(font=current_font)
        title3.config(font=current_font)
        title4.config(font=current_font)
        
        font_size = max(8, event.width //60)
        label_choose.config(font=( ui_font, font_size, 'bold'))
        label_farm.config(font=( ui_font, font_size, 'bold'))
        
        font_size = max(8, event.width //60)
        combo_save.config(font=( ui_font, font_size, ))
        time.sleep(0)
        root.option_add('*TCombobox*Listbox.font', ( ui_font, font_size, 'bold'))