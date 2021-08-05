"""file with only draw_rectangle function"""

from curses.textpad import rectangle

def draw_rectangle(stdscr, loc, data):
    """
    goal :
        draw a rectangle to fit the zone to write message
    arg :
        stdscr : the screen
        loc : [uly, ulx, lry, lrx]
        data : a message to display at the begining
    return :
        True
    """
    stdscr.addstr(loc[0]-1, loc[1], data)
    rectangle(stdscr, loc[0], loc[1], loc[2], loc[3])
    stdscr.refresh()
    return True