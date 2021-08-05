"""File with only feditwin function."""

from curses import newwin
from curses.textpad import Textbox

def feditwin(editwin_loc):
    """
    Create a window to write message in.

    Parameters
    ----------
    editwin_loc: list
        the edit window localisation.

    Returns
    -------
    :class:curses._CursesWindow
        The edit window.
    :class:curses.Textbox
        The textbox to write text in.
    """
    n_line = editwin_loc[2] - editwin_loc[0] or 1
    n_col = editwin_loc[3] - editwin_loc[1]
    y = editwin_loc[0]; x = editwin_loc[1]

    editwin = newwin(n_line, n_col, y, x)
    editwin.keypad(True)
    box = Textbox(editwin)
    box.edit()
    return editwin, box