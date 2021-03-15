"""
file with only feditwin function
"""
from curses import newwin
from curses.textpad import Textbox

def feditwin(n_line, n_col, y, x):
    """
    goal :
        create a window to write message in
    arg :
        n_line : number of line
        n_col : number of column
        y : position y of upper-left corner
        x : position x of upper-left corner
    return :
        box object object
    """
    editwin = newwin(n_line, n_col, y, x)
    editwin.keypad(True)
    box = Textbox(editwin)
    box.edit()
    return editwin, box