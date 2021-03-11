import curses

class WriteMessage:
    """
    goal :
        write data to the pad
    arg :
        n_line : number of line of the pad
        n_col : number of column of the pad
        uly : upper left y
        ulx : upper lef x
        lry : lower right y
        lrx : lower right x
    """
    def __init__(self, n_line, n_col, uly, ulx, lry, lrx):
        self._max_line = n_line
        self._n_col = n_col
        self._uly = uly
        self._ulx = ulx
        self._lry = lry
        self._lrx = lrx
        self._history = []
        curses.start_color()
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        self.re_init()

    def re_init(self):
        self._pad = curses.newpad(self._max_line, self._n_col)
        self._pad.keypad(True)
        self._pad.refresh(0,0, self._uly,self._ulx, self._lry, self._lrx)
        self._counter = 0
        for data in self._history:
            data[0](*[data[x] for x in range(1, len(data))], False)
            self.pad_refresh()
        
    def write_new_message(self, author, message, history=True):
        """
        goal :
            write a message publish by an user
        arg :
            author : author publisher
            message : the message content
        return :
            None
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()

        list_message = self.split_large_text(f"{author} : {message}")
        for msg in list_message:
            self._pad.addstr(self._counter,0, msg)
            self._counter += 1

        self.pad_refresh()
        if history:
            self.add_to_history((self.write_new_message, author, message))

    def write_ping_message(self, author, message, history=True):
        """
        goal :
            write a ping message publish by an user
        arg :
            author : author publisher
            message : the message content
        return :
            None
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()

        list_message = self.split_large_text(f"!!--> {author} : {message}")
        for msg in list_message:
            if curses.has_colors():
                self._pad.addstr(self._counter,0, msg, curses.color_pair(2))
            else:
                self._pad.addstr(self._counter,0, msg)
            self._counter += 1

        self.pad_refresh()
        if history:
            self.add_to_history((self.write_ping_message, author, message))

    def write_system_message(self, data, history=True):
        """
        goal :
            write a system message (in red)
        arg :
            data : data
        return :
            None
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()

        list_message = self.split_large_text(data)
        for msg in list_message:
            if curses.has_colors():
                self._pad.addstr(self._counter,0, msg, curses.color_pair(1))
            else:
                self._pad.addstr(self._counter,0, msg)
            self._counter += 1
        
        self.pad_refresh()
        if history:
            self.add_to_history((self.write_system_message, data))

    def write_start_up_message(self, pseudo):
        """
        goal :
            write the start up message
        arg :
            pseudo : user pseudo
        return :
            None
        """
        self.write_system_message("Connection réalisée avec succès")
        self.write_system_message("Voici ton pseudo : ")
        if curses.has_colors():
            self._pad.addstr(1,19, pseudo, curses.color_pair(2))
        else:
            self._pad.addstr(1,19, pseudo)
        self.write_system_message("Voir les différentes commandes possibles : /help")
        self.write_system_message("Ecris le message et appui sur Ctrl+G")
        
        self.pad_refresh()

    def pad_refresh(self):
        if self._counter <= self._lry - self._uly -1:
            self._pad.refresh(0,0, self._uly,self._ulx, self._lry, self._lrx)
        else:
            pos_y = self._counter - self._lry - self._uly + 1
            self._pad.refresh(pos_y, 0, self._uly,self._ulx, self._lry, self._lrx)

    def add_to_history(self, data):
        if len(self._history) > 20:
            del self._history[0]
        self._history.append(data)

    def split_large_text(self, data):
        if len(data) >= curses.COLS: # pylint: disable=no-member
            l_data = []
            while len(data) >= curses.COLS: # pylint: disable=no-member
                l_data.append(data[:curses.COLS-1]) # pylint: disable=no-member
                data = data[curses.COLS-1:] # pylint: disable=no-member
            l_data.append(data[:curses.COLS-1]) # pylint: disable=no-member
            data = data[curses.COLS-1:] # pylint: disable=no-member
        else:
            l_data = [data]
        return l_data
