"""
file with only feditwin function
"""
from curses import newwin
from curses.textpad import Textbox

def feditwin(editwin_loc):
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
    n_line = editwin_loc[2] - editwin_loc[0] or 1
    n_col = editwin_loc[3] - editwin_loc[1]
    y = editwin_loc[0]; x = editwin_loc[1]

    editwin = newwin(n_line, n_col, y, x)
    editwin.keypad(True)
    box = Textbox(editwin)
    box.edit()
    return editwin, box