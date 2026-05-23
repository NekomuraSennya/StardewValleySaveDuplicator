import sys, os, time
import jieba
from tkinter import font as ft
from pyperclip import copy
dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dirname)
from color_converter import color_converter as ccv

jieba.initialize()

input_text, input_text_1, input_text_2 = '', '', ''
cursor_index = 0
color_flip = False
font = None
offset = 0
boundaries = {}
selected_text = ''
select_side = ''
select_middle = 0

def input_char(char):
    global input_text, select_side, select_middle, selected_text, cursor_index, select_index
    
    
    
    if select_side == '':
        input_text = input_text[:cursor_index] + char + input_text[cursor_index:]
        cursor_index += 1
    else:
        input_text = input_text[:select_index] + char + input_text[select_index + len(selected_text):]
        cursor_index = select_index + 1
        select_side = ''
        select_middle = 0
        selected_text = ''

def get_word_boundaries(text):
    if not text:
        return [0]
    
    breaks_list = jieba.lcut_for_search(text)
    breaks = {}
    index = 0
    for i in breaks_list:
        breaks.update({index: i})
        text = text[len(i)-1:]
        index += len(i)
    breaks.update({index: ''})
    return breaks

def blink(root, canvas):
    global color_flip
    color_flip = not color_flip
    draw_input(root, canvas)
    root.after(500, lambda: blink(root, canvas))

def draw_speech(event, canvas, color, canvas_color, is_empty_warning=False):
    
    x1 = 0
    y1 = 0
    x2 = event.width
    y2 = event.height
    r = 20 * (event.height/1080+1) - 12
    points = [
        x1+r, y1, x2-r,y1, 
        x2,y1+r, x2,y2-r, x2-r,y2, x1+r,y2, x1,y2-r, x1,y1+r
        ]
    if is_empty_warning:
        canvas.itemconfig('speech', fill=ccv(canvas_color))
    else:
        canvas.config(bg=color['root'])
        
        if not canvas.find_withtag('speech'):
            canvas.create_polygon(points, fill=ccv(canvas_color), smooth=True, tags=['speech'], width=0)
        else:
            canvas.coords('speech', *points)
        
        
def on_click(event, root, canvas):
    global cursor_index
    canvas.focus_set()
    
    H = canvas.winfo_height()
    
    if input_text:
        try:
            idx = canvas.index('probe', f"@{event.x-offset},{H//2}")
            if idx > cursor_index:
                idx -= 1
            cursor_index = max(0, min(idx, len(input_text)))
        except:
            cursor_index = len(input_text)
    else:
        cursor_index = 0
        
    draw_input(root, canvas)
# def on_drag(event, root, canvas):
#     # TODO: 拖動選取功能

def draw_input(root, canvas):
    global input_text, color_flip, font, offset, select_side
    
    canvas.tag_lower('speech')
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    
    font_size = max(12, root.winfo_width()//60,  root.winfo_height()//20)
    if font == None or font.actual()['size'] != font_size: font = ft.Font(family='jf open 粉圓 2.1', size=font_size)

    
    x1 = 10
    x2 = 10 + font.measure(input_text_1)
    x_cursor = 10 + font.measure(input_text[:cursor_index]) - 2
    x3 = 10 + font.measure(input_text_1 + selected_text)
    if not canvas.find_withtag('text'):
        canvas.create_rectangle(
            x2, H-H//4, x3, H//4,
            width = 0,
            fill = '#0000ff',
            tags = ['select']
        )
        canvas.create_text(
            x1, H//2,
            text = input_text_1,
            font = font,
            fill = '#000000',
            anchor = 'w',
            tags = ['text', 'text1']
        )
        canvas.create_text(
            x_cursor, H//2,
            text = '|',
            font = font,
            fill = '#000000',
            anchor = 'w',
            tags = ['text', 'cursor']
        )
        canvas.create_text(
            x2, H//2,
            text = selected_text,
            font = font,
            fill = '#ffffff',
            anchor = 'w',
            tags = ['text', 'text_select']
        )
        canvas.create_text(
            x3, H//2,
            text = input_text_2,
            font = font,
            fill = '#000000',
            anchor = 'w',
            tags = ['text', 'text2']
        )
        canvas.create_text(
            x1, H//2,
            text = input_text[:cursor_index] + input_text[cursor_index:],
            font= font,
            anchor = 'w',
            state = 'hidden',
            tags = ['text', 'probe']
        )
    else:
        if x_cursor + offset > W:
            offset = (W - 20) - x_cursor
        elif x_cursor + offset < x1:
            offset = x1 - x_cursor
        x1 += offset; x_cursor += offset; x2 += offset; x3 += offset
        
        canvas.coords('select', x2, H-H//4, x3, H//4)
        
        canvas.itemconfig('text1', text=input_text_1, font=font)
        canvas.coords('text1', x1, H//2)
        
        canvas.itemconfig('cursor', text='|', font=font, fill='#000000' if not color_flip else '#f7edc6')
        canvas.coords('cursor', x_cursor, H//2)
        
        canvas.itemconfig('text_select', text=selected_text, font=font)
        canvas.coords('text_select', x2, H//2,)
        
        canvas.itemconfig('text2', text=input_text_2, font=font)
        canvas.coords('text2', x3, H//2)
        
        canvas.itemconfig('probe', text=input_text[:cursor_index]+input_text[cursor_index:], font=font)
        canvas.coords('probe', x1, H//2)
    if canvas.find_withtag('speech'):
        if select_side == '':
            canvas.tag_lower('select', 'speech')
        else:
            canvas.tag_raise('select', 'speech')
        

def on_key(event, root):
    global input_text, input_text_1, input_text_2, cursor_index, boundaries, selected_text, select_side, select_middle, select_index
    
    is_ctrl = (event.state & 0x0004) != 0
    is_shift = (event.state & 0x0009) == 0x0009
    
    match event.keysym:
        case 'BackSpace':
            if select_index != '':
                input_text = input_text[:select_index] + input_text[select_index + len(selected_text):]
                cursor_index = select_index
                selected_text = ''
                select_side = ''
                select_middle = 0
            elif is_ctrl:
                if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
                if not cursor_index in list(boundaries.keys()):
                    list(boundaries.keys()).append(cursor_index)
                list(boundaries.keys()).sort()
                if not cursor_index == 0:
                    input_text = input_text[:list(boundaries.keys())[list(boundaries.keys()).index(cursor_index)-1]] + input_text[cursor_index:]
                    cursor_index = list(boundaries.keys())[list(boundaries.keys()).index(cursor_index)-1]
            else:
                if not cursor_index == 0:
                    input_text = input_text[:cursor_index-1] + input_text[cursor_index:]
                    cursor_index -= 1
        case 'Delete':
            if select_index != '':
                input_text = input_text[:select_index] + input_text[select_index + len(selected_text):]
                cursor_index = select_index
                selected_text = ''
                select_side = ''
                select_middle = 0
            elif is_ctrl:
                if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
                if not cursor_index in list(boundaries.keys()):
                    list(boundaries.keys()).append(cursor_index)
                list(boundaries.keys()).sort()
                if not cursor_index == len(input_text):
                    input_text = input_text[:cursor_index] + input_text[list(boundaries.keys())[list(boundaries.keys()).index(cursor_index)+1]:]
                    cursor_index = list(boundaries.keys())[list(boundaries.keys()).index(cursor_index)]
            else:
                if not cursor_index == len(input_text):
                    input_text = input_text[:cursor_index] + input_text[cursor_index+1:]
                    cursor_index += 1
        case 'Right':
            if not cursor_index == len(input_text):
                if is_ctrl:
                    if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
                    if not cursor_index in list(boundaries.keys()):
                        boundaries.update({cursor_index: 'cursor'})
                        boundaries = dict(sorted(boundaries.items()))
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                    dict_cursor += 1
                    if len(boundaries) - dict_cursor == 1:
                        while list(boundaries.values())[dict_cursor] not in [' ', ''] and list(boundaries.values())[dict_cursor+1] in [' ', ''] :
                            dict_cursor += 1
                        if all((list(boundaries.values())[i] not in [' ', ''] for i in [dict_cursor, dict_cursor+1])):
                            dict_cursor += 1
                    cursor_index = list(boundaries.keys())[dict_cursor]
                elif is_shift:
                    if select_side != 'Left':
                        selected_text += input_text[cursor_index]
                        if select_middle == 0: select_middle = cursor_index
                        cursor_index += 1
                        select_side = 'Right'
                    else:
                        selected_text = selected_text[1:]
                        cursor_index += 1
                        if selected_text == '': select_side = 'Middle'
                else:
                    cursor_index += 1
                if not is_shift:
                    selected_text = ''
                    select_middle = 0
                    select_side = ''
        case 'Left':
            if not cursor_index <= 0:
                if is_ctrl:
                    if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
                    if not cursor_index in list(boundaries.keys()):
                        boundaries.update({cursor_index: 'cursor'})
                        boundaries = dict(sorted(boundaries.items()))
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                    dict_cursor -= 1
                    while list(boundaries.values())[dict_cursor] in [' ', '']:
                        dict_cursor -= 1
                    cursor_index = list(boundaries.keys())[dict_cursor]
                elif is_shift:
                    if select_side != 'Right':
                        selected_text = input_text[cursor_index-1] + selected_text
                        if select_middle == 0: select_middle = cursor_index
                        cursor_index -= 1
                        select_side = 'Left'
                    else:
                        selected_text = selected_text[:-1]
                        cursor_index -= 1
                        if selected_text == '': select_side = 'Middle'
                else:
                    cursor_index -= 1
                if not is_shift:
                    selected_text = ''
                    select_middle = 0
                    select_side = ''
        case 'End':
            if is_shift:
                select_side = 'Right'
                if select_middle == 0:
                    selected_text = input_text[cursor_index:]
                    select_middle = cursor_index
                else: selected_text = input_text[select_middle:]
                cursor_index = len(input_text)
            else:
                cursor_index = len(input_text)
                selected_text = ''
                select_middle = 0
                select_side = ''
        case 'Home':
            if is_shift:
                select_side = 'Left'
                if select_middle == 0:
                    selected_text = input_text[:cursor_index]
                    select_middle = cursor_index
                else: selected_text = input_text[:select_middle]
                cursor_index = 0
            else:
                cursor_index = 0
                selected_text = ''
                select_middle = 0
                select_side = ''
        case 'v':
            if is_ctrl:
                input_text = input_text[:cursor_index] + root.clipboard_get() + input_text[cursor_index:]
                cursor_index += len(root.clipboard_get())
            else:
                input_char(event.char)
        case 'c':
            if is_ctrl and selected_text != '':
                copy(selected_text)
            else:
                input_char(event.char)
        case 'a':
            if is_ctrl:
                selected_text = input_text
                select_side = 'Right',
                cursor_index = len(input_text)
                select_middle = cursor_index
            else:
                input_char(event.char)
        case _ if event.char != '' and event.char.isprintable():
            input_char(event.char)
    
    select_index = select_middle if select_side == 'Right' else select_middle - len(selected_text)
    if selected_text == '': select_side, select_middle = '', 0
    if select_side == '': input_text_1, input_text_2 = input_text[:cursor_index], input_text[cursor_index:]
    else: input_text_1, input_text_2 = input_text[:select_index], input_text[select_index + len(selected_text):]