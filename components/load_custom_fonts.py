import ctypes, os

def load_custom_font(path):
    path = f'C:/Users/{os.environ.get("USERNAME")}/AppData/Local/Microsoft/Windows/Fonts/{path}'
    if os.path.exists(path):
        FR_PRIVATE = 0x10
        ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
        print(f'成功載入字體：{os.path.basename(path)}')
        return True
    else:
        print(f"找不到字體檔案：{path}")
        return False