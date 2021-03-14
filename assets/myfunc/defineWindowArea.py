"""
file with only defineWindowArea function
"""
import curses

def defineWindowArea():
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
    pad_localisation.append(int(curses.LINES*4/5)); y+= int(curses.LINES*4/5) # pylint: disable=no-member
    pad_localisation.append(curses.COLS-1) # pylint: disable=no-member

    rectangle_localisation.append(y+1)
    rectangle_localisation.append(1)
    rectangle_localisation.append(curses.LINES-1) # pylint: disable=no-member
    rectangle_localisation.append(curses.COLS-2) # pylint: disable=no-member

    editwin_localisation.append(y+2)
    editwin_localisation.append(2)
    editwin_localisation.append(curses.LINES-2) # pylint: disable=no-member
    editwin_localisation.append(curses.COLS-3) # pylint: disable=no-member

    return pad_localisation, rectangle_localisation, editwin_localisation


