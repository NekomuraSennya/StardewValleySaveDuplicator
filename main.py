import tkinter as tk
from tkinter import ttk, messagebox
import core, json, os
from components import empty_warning, resize
import components.global_vars as gv
from components.color_converter import color_converter as ccv
from components import inputting, speech_resize
from components.load_custom_fonts import load_custom_font



os.chdir(f'C:/Users/{os.environ.get('USERNAME')}/AppData/Roaming/StardewValley/Saves')
project_path = os.path.dirname(os.path.abspath(__file__))

tilte_font_exist = load_custom_font('PopGothicCjkTc-Bold.ttf')
title_font = '大波浪圓體 CJK TC-Bold' if tilte_font_exist else 'Arial'
ui_font_exist = load_custom_font('jf-openhuninn-2.1.ttf')
gv.ui_font = 'jf open 粉圓 2.1' if ui_font_exist else 'Arial'

with open(f'{project_path}/theme.json', 'r') as f:
    with open(f'{project_path}/config.json', 'r') as g:
        config = json.load(g)[f'theme']
    theme = json.load(f)
    key = list(theme.keys())[int(config)]
    gv.color = theme[key]
def copy():
    pass
    if inputting.input_text.strip() == '':
        empty_warning.empty_warning()
        messagebox.showwarning('警告','牧場名稱不能為空')
        return
    core.main(gv.combo_save.get(), inputting.input_text)
    messagebox.showinfo('完成', '存檔複製完畢。')   
    new_saves = core.find_saves()
    print(new_saves)
    gv.combo_save['values'] = new_saves
    
def openfolder():
    os.startfile('./')
    
def change_theme():
    with open(f'{project_path}/config.json', 'r') as f:
        config = json.load(f)
        id = int(config['theme'])
        if id < 2: id += 1
        else: id = 0
    with open(f'{project_path}/theme.json', 'r') as f:
        theme = json.load(f)
        key = list(theme.keys())[id]
        color = theme[key]
    with open(f'{project_path}/config.json', 'w') as f:
        config['theme'] = id
        json.dump(config, f)
    gv.root.config(bg=gv.color['root'])
    title_grid.config(bg=gv.color['root'])
    ui_grid.config(bg=gv.color['root'])
    gv.title1.config(bg=gv.color['root'], fg=gv.color['title1_fg'])
    gv.title2.config(bg=gv.color['root'], fg=gv.color['title2_fg'])
    gv.title3.config(bg=gv.color['root'], fg=gv.color['title3_fg'])
    gv.title4.config(bg=gv.color['root'], fg=gv.color['title4_fg'])
    gv.label_choose.config(bg=gv.color['root'], fg=gv.color['label_choose_fg'])
    gv.label_farm.config(bg=gv.color['root'], fg=gv.color['label_farm_fg'])
    button.config(bg=gv.color['root'], activebackground=gv.color['root'])
    change_theme_button.config(bg='#ffffff')
    folder_button.config(bg=gv.color['root'], image=folder_images[int(gv.color['folder'])], activebackground=gv.color['root'])
    version.config(bg=gv.color['root'])
    gv.canvas.config(bg=gv.color['root'])

day = False
gv.root = tk.Tk()
gv.root.title('星露谷物語存檔複製小工具')
gv.root.geometry('400x300')
gv.root.config(background=gv.color['root'])
gv.root.minsize(300, 300)

style = ttk.Style()
style.theme_use('clam')
style.configure(
    'Stardew.TCombobox',
kground = 'f7edc6',
    arrowcolor = 999481
)
style.map(
    'Stardew.TCombobox',
    fieldbackground=[('readonly', '#f7edc6')],
    foreground = [('readonly', '#0000000')]
    
)

gv.root.grid_columnconfigure(0, weight=1)
gv.root.grid_rowconfigure(0, weight=1)
gv.root.grid_rowconfigure(1, weight=1)

title_grid = tk.Frame(gv.root, bg=gv.color['root'])
title_grid.grid(row=0, column=0, sticky='we')

title_grid.columnconfigure(0, weight=0)
title_grid.columnconfigure(1, weight=1)

title = tk.Frame(title_grid)
title.grid(row=0, column=1, pady=(40, 0))

gv.title1 = tk.Label(title, text='星露谷物語', font=(title_font, 20, 'bold'), bg=gv.color['root'], fg=gv.color['title1_fg'])
gv.title2 = tk.Label(title, text='存檔', font=(title_font, 20, 'bold'), bg=gv.color['root'], fg=gv.color['title2_fg'])
gv.title3 = tk.Label(title, text='複製', font=(title_font, 20, 'bold'), bg=gv.color['root'], fg=gv.color['title3_fg'])
gv.title4 = tk.Label(title, text='小工具', font=(title_font, 20, 'bold'), bg=gv.color['root'], fg=gv.color['title4_fg'])

gv.title1.pack(side='left')
gv.title2.pack(side='left')
gv.title3.pack(side='left')
gv.title4.pack(side='left')

ui_grid = tk.Frame(gv.root, bg=gv.color['root'])
ui_grid.grid(row=1, column=0, sticky='news', )

ui_grid.columnconfigure(0, weight=7)
ui_grid.columnconfigure(1, weight=1)
ui_grid.columnconfigure(2, weight=7)
ui_grid.rowconfigure(2, weight=1)
ui_grid.rowconfigure(3, weight=1)
ui_grid.rowconfigure(4, weight=1)
ui_grid.rowconfigure(5, weight=1)
ui_grid.rowconfigure(6, weight=1)
ui_grid.rowconfigure(7, weight=1)

for i in range(8):
    ui_grid.rowconfigure(i, weight=1)

gv.label_choose = tk.Label(ui_grid, text='請選擇要複製的存檔', font=(gv.ui_font, 10), bg=gv.color['root'], fg=gv.color['label_choose_fg'])
gv.label_choose.grid(row=2, column=1)

gv.combo_save = ttk.Combobox(ui_grid, width=27, values=core.find_saves(), state='readonly', style='Stardew.TCombobox', font=(gv.ui_font, 10, 'bold'))
gv.combo_save.grid(row=3, column=1, sticky='nsew')
try:
    gv.combo_save.current(0)
except Exception:
    pass

gv.label_farm = tk.Label(ui_grid, text='請輸入新農場的名稱', font=(gv.ui_font, 10), bg=gv.color['root'], fg=gv.color['label_farm_fg'])
gv.label_farm.grid(row=4, column=1, sticky='news')

gv.canvas = tk.Canvas(ui_grid, bd=0, height=0, width=0, highlightthickness=False, cursor='xterm')
gv.canvas.grid(row=5, column=1)

button_image = tk.PhotoImage(file=f'{project_path}/assets/button.png')
button_image = button_image.subsample(4,4)
button = tk.Button(ui_grid, command=copy, image=button_image, bg=gv.color['root'], highlightthickness=False, borderwidth=0, activebackground=gv.color['root'])
button.grid(row=6, column=1,pady=20,sticky='news')

theme_image = tk.PhotoImage(file=f'{project_path}/assets/theme.png')
theme_image = theme_image.subsample(4,4)
change_theme_button = tk.Button(gv.root, command=change_theme, image=theme_image, height=20, width=20, bg='#ffffff', overrelief='groove')
change_theme_button.grid(row=0, column=0, sticky='nw', padx=(10,0), pady=(10,0))
folder_image_0 = tk.PhotoImage(file=f'{project_path}/assets/folder_0.png')
folder_image_1 = tk.PhotoImage(file=f'{project_path}/assets/folder_1.png')
folder_image_2 = tk.PhotoImage(file=f'{project_path}/assets/folder_2.png')

folder_images = [folder_image_0, folder_image_1, folder_image_2]
folder_button = tk.Button(ui_grid, command=openfolder, image=folder_images[int(gv.color['folder'])], bg=gv.color['root'], borderwidth=0, highlightthickness=False, activebackground=gv.color['root'])
folder_button.place(relx=1, rely=1, anchor='se')

version = tk.Label(ui_grid, text='v1.0.0.3 by SennyaOwO', font=(gv.ui_font, 8, 'bold'),bg=gv.color['root'],fg='#ffffff')
version.place(anchor='sw',relx=0,rely=1)
gv.root.bind('<Configure>', lambda event: (resize.resize(event)))
gv.canvas.bind('<Button-1>', lambda event: inputting.on_click(event))
gv.canvas.bind('<B1-Motion>', lambda event: inputting.on_drag(event))
gv.canvas.bind('ButtonRelease-1', inputting.on_release())
gv.canvas.bind('<Key>', lambda event: (inputting.on_key(event), inputting.draw_input()))
gv.canvas.bind('<Configure>', lambda event: (speech_resize.on_window_trigger(),
                                        inputting.draw_speech(event, [247, 237, 198], is_empty_warning=False)))
inputting.blink()

gv.root.mainloop()