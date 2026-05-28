from sys import path
from os.path import dirname
path.append(dirname(__file__))
import components.global_vars as gv

def color_converter(color):
    output = '#'
    output += hex(gv.color[0]).replace('0x','').zfill(2)
    output += hex(gv.color[1]).replace('0x','').zfill(2)
    output += hex(gv.color[2]).replace('0x','').zfill(2)
    return output