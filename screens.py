import console_utils as cu
import gamerunner as gr
import gamehandler as gh
import inputs
import time

def menu_screen():
    menu_items = inputs.menu_items[:]
    for name in menu_items:
        print(name)
    inp = input('> ').lower()
    return int(inp)
