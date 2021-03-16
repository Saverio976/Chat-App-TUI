"""
file with only defineWindowArea function
"""
import curses

def defineWindowArea(LINES, COLS):
    """
    goal :
        define upper left corner and lower right corner
        of the 3 object (pad, rectangle, editwin)
    arg : no
    return :
        list of 3 list [uly, ulx, lry, lrx]
    """
    pad_localisation = []
    rectangle_localisation = []
    editwin_localisation = []
    y = 0

    pad_localisation.append(1)
    pad_localisation.append(1)
    pad_localisation.append(int(LINES*4/5)); y+= int(LINES*4/5)
    pad_localisation.append(COLS-1)

    rectangle_localisation.append(y+1)
    rectangle_localisation.append(1)
    rectangle_localisation.append(LINES-1)
    rectangle_localisation.append(COLS-2)

    editwin_localisation.append(y+2)
    editwin_localisation.append(2)
    editwin_localisation.append(LINES-2)
    editwin_localisation.append(COLS-3)

    return pad_localisation, rectangle_localisation, editwin_localisation

def define_pad_loc(pad_loc):
    n_line = 100; n_col = pad_loc[3] - pad_loc[1] # n_line and n_col
    uly = pad_loc[0]; ulx = pad_loc[1] # uper-left y and x
    lry = pad_loc[2]; lrx = pad_loc[3] # lower-right y and x
    return n_line, n_col, uly, ulx, lry, lrx