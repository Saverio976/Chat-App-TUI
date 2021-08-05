"""File with only draw_rectangle function."""

from curses.textpad import rectangle

def draw_rectangle(stdscr, loc, data):
    """
    Draw a rectangle to fit the zone to write message.

    Parameters
    ----------
    stdscr: :class:curses.WindowObject
        The screen.
    loc: list
        [uly, ulx, lry, lrx]
    data: str
        A message to display at the begining.

    Returns
    -------
    bool
        True:
    """
    stdscr.addstr(loc[0]-1, loc[1], data)
    rectangle(stdscr, loc[0], loc[1], loc[2], loc[3])
    stdscr.refresh()
    return True