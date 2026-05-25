import traceback

import sys, os, time
import jieba
from tkinter import font as ft
from pyperclip import copy
from ctypes import windll
dirname = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dirname)

jieba.initialize()

input_text, input_text_1, input_text_2 = '', '', ''
cursor_index = 0
dict_cursor = 0
color_flip = False
font = None
offset = 0
boundaries = {}
selected_text = ''
select_side = ''
select_middle = -1
selecting = False
clicks = [0]
doubleclick_judgement = windll.user32.GetDoubleClickTime() / 1000

def color_converter(color):
    output = '#'
    output += hex(color[0]).replace('0x','').zfill(2)
    output += hex(color[1]).replace('0x','').zfill(2)
    output += hex(color[2]).replace('0x','').zfill(2)
    return output

def input_char(char, ignore_select=False):
    global input_text, select_side, select_middle, selected_text, cursor_index, select_index
    
    if select_side == '':
        input_text = input_text[:cursor_index] + char + input_text[cursor_index:]
        cursor_index += 1
    elif not ignore_select:
        input_text = input_text[:select_index] + char + input_text[select_index + len(selected_text):]
        cursor_index = select_index + 1
        select_side = ''
        select_middle = -1
        selected_text = ''

def get_word_boundaries(text):
    if not text:
        return {0: ''}
    
    breaks_list = jieba.lcut(text, cut_all=False)
    breaks = {}
    index = 0
    for i in breaks_list:
        breaks.update({index: i})
        text = text[len(i)-1:]
        index += len(i)
    breaks.update({index: ''})
    return breaks

def blink(root, canvas, ui_font):
    global color_flip
    
    color_flip = not color_flip
    draw_input(root, canvas, ui_font)
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
        canvas.itemconfig('speech', fill=color_converter(canvas_color))
    else:
        canvas.config(bg=color['root'])
        
        if not canvas.find_withtag('speech'):
            canvas.create_polygon(points, fill=color_converter(canvas_color), smooth=True, tags=['speech'], width=0)
        else:
            canvas.coords('speech', *points)
def on_click(event, root, canvas):
    global cursor_index, selecting, is_shift, select_middle, select_index, select_side, selected_text, selecting, cursor_index_old, clicks, doubleclick, tripleclick, boundaries
    
    clicks.append(time.perf_counter())
    if len(clicks) > 1:
        if len(clicks) >= 3 and all(i < doubleclick_judgement for i in [clicks[-1] - clicks[-2], clicks[-2] - clicks[-3]]):
            tripleclick = True
            clicks = [0]
        elif clicks[-1] - clicks[-2] < doubleclick_judgement:
            doubleclick = True
        else:
            doubleclick = False
            tripleclick = False
        
        
    if input_text != ''.join(list(boundaries.values())):
        boundaries = get_word_boundaries(input_text)
    
    canvas.focus_set()
    selecting = True
    H = canvas.winfo_height()
    is_shift = (event.state & 0x0009) == 0x0009
    
    if input_text or selected_text:
        try:
            if is_shift:
                if not select_middle:
                    select_middle = cursor_index_old
            else:
                selected_text = ''
                select_side = ''
                select_middle = -1
            index = canvas.index('probe', f"@{event.x},{H}")
            cursor_index_old = cursor_index
            cursor_index = max(0, min(index, len(input_text)))
            if doubleclick:
                if not cursor_index in list(boundaries.keys()):
                    boundaries.update({cursor_index: 'cursor'})
                    boundaries = dict(sorted(boundaries.items()))
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                else:
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                selected_text = list(boundaries.values())[dict_cursor-1]
                select_side = 'Right'
                select_middle = list(boundaries.keys())[dict_cursor-1]
                cursor_index = len(''.join(list(boundaries.values())[0:dict_cursor]))
            elif tripleclick:
                selected_text = input_text
                select_side = 'Right',
                cursor_index = len(input_text)
                select_middle = cursor_index
            if is_shift:
                if cursor_index_old < index:
                    if select_side == 'Left':
                        select_middle = cursor_index_old + len(selected_text)
                    selected_text = ''
                    select_side = 'Right'
                    selected_text = input_text[cursor_index_old:index] if not select_middle else input_text[select_middle:index]
                else:
                    if select_side == 'Right':
                        select_middle = cursor_index_old - len(selected_text)
                    selected_text = ''
                    select_side = 'Left'
                    selected_text = input_text[index:cursor_index_old] if not select_middle else input_text[index:select_middle]
        except:
            cursor_index = len(input_text)
    else:
        cursor_index = 0

def on_drag(event, root, canvas, ui_font):
    global cursor_index, selecting, is_shift, select_middle, select_index, select_side, selected_text, selecting, cursor_index_old, doubleclick, boundaries
    
    if input_text != ''.join(list(boundaries.values())):
        boundaries = get_word_boundaries(input_text)
    
    H = canvas.winfo_height()
    if input_text or selected_text:
        try:
            if selecting:
                if not select_middle:
                    select_middle = cursor_index_old
                index = canvas.index('probe', f"@{event.x},{H}")
                if doubleclick:
                    pass
                else:
                    
                    if not cursor_index in list(boundaries.keys()):
                        boundaries.update({cursor_index: 'cursor'})
                        boundaries = dict(sorted(boundaries.items()))
                        dict_cursor = list(boundaries.keys()).index(cursor_index)
                    else:
                        dict_cursor = list(boundaries.keys()).index(cursor_index)
                    selected_text = list(boundaries.values())[dict_cursor-1]
                    select_side = 'Right'
                    select_middle = list(boundaries.keys())[dict_cursor-1]
        except:
            pass
        draw_input(root, canvas, ui_font)
    else:
        cursor_index = 0
    
def on_release():
    global selecting
    
    selecting = False

def draw_input(root, canvas, ui_font):
    global input_text, color_flip, font, offset, select_side, select_index, select_middle, selected_text
    
    if type(selected_text) == list: selected_text = ''.join(selected_text)
    select_index = select_middle if select_side == 'Right' else select_middle - len(selected_text)
    
    if selected_text == '':
        select_side = ''
        select_middle = -1
    if select_side == '':
        input_text_1 = input_text[:cursor_index]
        input_text_2 = input_text[cursor_index:]
    else: 
        input_text_1 = input_text[:select_index]
        input_text_2 = input_text[select_index + len(selected_text):]
    canvas.tag_lower('speech')
    W = canvas.winfo_width()
    H = canvas.winfo_height()
    
    font_size = max(12, root.winfo_width()//60,  root.winfo_height()//20)
    if font == None or font.actual()['size'] != font_size: font = ft.Font(family=ui_font, size=font_size)

    
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
    global input_text, input_text_1, input_text_2, cursor_index, boundaries, selected_text, select_side, select_middle, is_shift, dict_cursor
    
    is_ctrl = (event.state & 0x0004) != 0
    is_shift = (event.state & 0x0009) == 0x0009
    
    match event.keysym:
        case 'Enter':
            # Ignore
            pass
        case 'BackSpace':
            if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
            # Selecting
            if select_side != '':
                input_text = input_text[:select_index] + input_text[select_index + len(selected_text):]
                cursor_index = select_index
                selected_text = ''
                select_side = ''
                select_middle = -1
            # Ctrl
            elif is_ctrl:
                if not cursor_index in list(boundaries.keys()):
                    boundaries.update({cursor_index: 'cursor'})
                    boundaries = dict(sorted(boundaries.items()))
                dict_cursor = list(boundaries.keys()).index(cursor_index)
                print(list(boundaries.values())[dict_cursor-2:dict_cursor])
                if list(boundaries.values())[dict_cursor-2:dict_cursor] == [' ', ' ']:
                    while True:
                        if dict_cursor > 0 : dict_cursor -= 1
                        if list(boundaries.values())[dict_cursor] == ' ' and dict_cursor > 0:
                            continue
                        else:
                            break
                else:
                    while True:
                        if dict_cursor > 0: dict_cursor -= 1
                        if list(boundaries.values())[dict_cursor] != ' ' and dict_cursor > 0:
                            continue
                        else:
                            break
                input_text = input_text[:list(boundaries.keys())[dict_cursor]] + input_text[cursor_index:]
            # Normal
            else:
                if not cursor_index == 0:
                    input_text = input_text[:cursor_index-1] + input_text[cursor_index:]
                    cursor_index -= 1
        case 'Delete':
            if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
            # Selecting
            if select_side != '':
                input_text = input_text[:select_index] + input_text[select_index + len(selected_text):]
                cursor_index = select_index
                selected_text = ''
                select_side = ''
                select_middle = -1
            # Ctrl
            elif is_ctrl:
                if not cursor_index in list(boundaries.keys()):
                    boundaries.update({cursor_index: 'cursor'})
                    boundaries = dict(sorted(boundaries.items()))
                dict_cursor = list(boundaries.keys()).index(cursor_index)
                if list(boundaries.values())[dict_cursor:dict_cursor+2] == [' ', ' ']:
                    while True:
                        if dict_cursor < len(boundaries) - 1: dict_cursor += 1
                        if list(boundaries.values())[dict_cursor] == ' ' and dict_cursor < len(boundaries) - 1:
                            continue
                        else:
                            break
                else:
                    while True:
                        if dict_cursor < len(boundaries) - 1: dict_cursor += 1
                        if list(boundaries.values())[dict_cursor] != ' ' and dict_cursor < len(boundaries) - 1:
                            continue
                        else:
                            break
                input_text = input_text[:cursor_index] + input_text[list(boundaries.keys())[dict_cursor]:]
            # Normal
            else:
                if not cursor_index == len(input_text):
                    input_text = input_text[:cursor_index] + input_text[cursor_index+1:]
        case 'Right':
            if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
            if not cursor_index == len(input_text):
            # Ctrl-Shift
                if is_ctrl and  is_shift:
                    # if not cursor_index in list(boundaries.keys()):
                    #     boundaries.update({cursor_index: 'cursor'})
                    #     boundaries = dict(sorted(boundaries.items()))
                    # dict_cursor = list(boundaries.keys()).index(cursor_index)
                    # if dict_cursor < len(boundaries):
                    #     if list(boundaries.values())[dict_cursor] not in [' ', ''] :
                    #         while list(boundaries.values())[dict_cursor] not in [' ', '']:
                    #             dict_cursor += 1
                    #     else:
                    #         while list(boundaries.values())[dict_cursor] in [' ', '']:
                    #             dict_cursor += 1
                    #             if list(boundaries.values())[dict_cursor] in [' ', '']:
                    #                 dict_cursor += 1
                    #                 continue
                    #             else:
                    #                 break
                    #     dict_cursor += 1
                    # if select_side == '': select_side = 'Right'
                    # cursor_index = list(boundaries.keys())[dict_cursor]
                    # if type(selected_text) == str: selected_text = []
                    # if select_side == 'Right':
                    #     selected_text.append(input_text[select_middle:cursor_index])
                    #     print(input_text[select_middle])
                    #     print(selected_text)
                    
                        
                    cursor_index = list(boundaries.keys())[dict_cursor]
                    
                    print(selected_text)
                    if selected_text == '':
                        select_side = 'Middle'
            # Ctrl
                elif not is_shift and is_ctrl:
                    boundaries.update({cursor_index: 'cursor'})
                    boundaries = dict(sorted(boundaries.items()))
                dict_cursor = list(boundaries.keys()).index(cursor_index)
                if dict_cursor < len(boundaries):
                    if list(boundaries.values())[dict_cursor] not in [' ', ''] :
                        while list(boundaries.values())[dict_cursor] not in [' ', '']:
                            dict_cursor += 1
                    else:
                        while list(boundaries.values())[dict_cursor] in [' ', '']:
                            dict_cursor += 1
                            if list(boundaries.values())[dict_cursor] in [' ', '']:
                                dict_cursor += 1
                                continue
                            else:
                                break
                        dict_cursor += 1
                    cursor_index = list(boundaries.keys())[dict_cursor]
            # Shift
                elif not is_ctrl and is_shift:
                    if select_side != 'Left':
                        selected_text += input_text[cursor_index]
                        if select_middle == -1:
                            select_middle = cursor_index
                        cursor_index += 1
                        select_side = 'Right'
                    else:
                        selected_text = selected_text[1:]
                        cursor_index += 1
                        if selected_text == '':
                            select_side = 'Middle'
                else:
                    cursor_index += 1
            # Normal
                if not is_shift and not is_ctrl:
                    selected_text = ''
                    select_middle = -1
                    select_side = ''
        case 'Left':
            if input_text != ''.join(list(boundaries.values())): boundaries = get_word_boundaries(input_text)
            if not cursor_index <= 0:
            # Ctrl-Shift
                if is_ctrl and  is_shift:
                    if not cursor_index in list(boundaries.keys()):
                        boundaries.update({cursor_index: 'cursor'})
                        boundaries = dict(sorted(boundaries.items()))
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                    if select_middle == -1: select_middle = cursor_index
                    dict_cursor -= 1
                    if dict_cursor > 0:
                        while list(boundaries.values())[dict_cursor-1] not in [' ', '']:
                            dict_cursor -= 1
                    cursor_index = list(boundaries.keys())[dict_cursor]
                    cursor_index = list(boundaries.keys())[dict_cursor]
                    selected_text = input_text[cursor_index:select_middle]
                    print(selected_text)
                    if selected_text == '':
                        select_side = 'Middle'
                            
            # Ctrl
                if not is_shift and is_ctrl:
                    if not cursor_index in list(boundaries.keys()):
                        boundaries.update({cursor_index: 'cursor'})
                        boundaries = dict(sorted(boundaries.items()))
                    dict_cursor = list(boundaries.keys()).index(cursor_index)
                    dict_cursor -= 1
                    while dict_cursor > 0:
                        dict_cursor -= 1
                        if list(boundaries.values())[dict_cursor] not in [' ', '']:
                            continue
                        else:
                            break
                    cursor_index = list(boundaries.keys())[dict_cursor]
            # Shift
                elif not is_ctrl and is_shift:
                    if select_side != 'Right':
                        selected_text = input_text[cursor_index-1] + selected_text
                        if select_middle == -1:
                            select_middle = cursor_index
                        cursor_index -= 1
                        select_side = 'Left'
                    else:
                        selected_text = selected_text[:-1]
                        cursor_index -= 1
                        if selected_text == '':
                            select_side = 'Middle'
                else:
                    cursor_index -= 1
            # Normal
                if not is_shift and not is_ctrl:
                    selected_text = ''
                    select_middle = -1
                    select_side = ''
        case 'End':
            # Shift
            if is_shift:
                select_side = 'Right'
                if select_middle == -1:
                    selected_text = input_text[cursor_index:]
                    select_middle = cursor_index
                else: selected_text = input_text[select_middle:]
                cursor_index = len(input_text)
            # Normal
            else:
                cursor_index = len(input_text)
                selected_text = ''
                select_middle = -1
                select_side = ''
        case 'Home':
            # Shift
            if is_shift:
                select_side = 'Left'
                if select_middle == -1:
                    selected_text = input_text[:cursor_index]
                    select_middle = cursor_index
                else: selected_text = input_text[:select_middle]
                cursor_index = 0
            # Normal
            else:
                cursor_index = 0
                selected_text = ''
                select_middle = -1
                select_side = ''
        case 'v':
            # Ctrl
            if is_ctrl:
                input_char(str(root.clipboard_get()).replace('\n', ' '))
                cursor_index += len(str(root.clipboard_get()).replace('\n', ' '))
            # Normal
            else:
                input_char(event.char)
        case 'c':
            # Ctrl
            if is_ctrl and selected_text != '':
                copy(selected_text)
            # Normal
            else:
                input_char(event.char, ignore_select=True)
        case 'x':
            # Ctrl
            if is_ctrl and selected_text != '':
                copy(selected_text)
                input_char('')
            # Normal
            else:
                input_char(event.char)
        case 'a':
            # Ctrl
            if is_ctrl:
                selected_text = input_text
                select_side = 'Right',
                cursor_index = len(input_text)
                select_middle = cursor_index
            # Normal
            else:
                input_char(event.char)
        case _ if event.char != '' and event.char.isprintable():
            # Normal
            input_char(event.char)