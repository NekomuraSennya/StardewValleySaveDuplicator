def color_converter(color):
    output = '#'
    output += hex(color[0]).replace('0x','').zfill(2)
    output += hex(color[1]).replace('0x','').zfill(2)
    output += hex(color[2]).replace('0x','').zfill(2)
    return output