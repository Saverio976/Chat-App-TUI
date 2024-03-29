"""File with only WriteMessage class."""

import curses

class WriteMessage:
    def __init__(self, history_file=False):
        """
        Write data to the pad.

        Parameters
        ----------
        n_line: int
            number of line of the pad
        n_col: int
            number of column of the pad
        uly: int
            upper left y
        ulx: int
            upper lef x
        lry: int
            lower right y
        lrx: int
            lower right x

        Returns
        -------
        :class:WriteMessage
        """
        curses.start_color()
        if curses.has_colors(): # pylint: disable=no-member
            self._curses_color = True
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK) # pylint: disable=no-member
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK) # pylint: disable=no-member
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK) # pylint: disable=no-member
        else:
            self._curses_color = False
        self._history = []; self._is_history_file = history_file

    def update_loc(self, n_line, n_col, uly, ulx, lry, lrx, history_file=False):
        self._max_line = n_line; self._n_col = n_col
        self._uly = uly; self._ulx = ulx
        self._lry = lry; self._lrx = lrx
        self.re_init()

    def re_init(self):
        self._pad = curses.newpad(self._max_line, self._n_col) # pylint: disable=no-member
        self._pad.keypad(True)
        self._pad.refresh(0,0, self._uly,self._ulx, self._lry, self._lrx)
        self._counter = 0; self._y = 0
        for data in self._history:
            data[0](*[data[x] for x in range(1, len(data))], history=False)
            self.pad_refresh()

    def write_new_message(self, author, message, history=True):
        """
        Write a message publish by an user.

        Parameters
        ----------
        author: str
            The author of the message.
        message: str
            The message to write.
        history: [Optional] bool
            Add the message to record history or not.
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()
        list_message = self.split_large_text(f"{author} : {message}")
        for msg in list_message:
            self._pad.addstr(self._counter,0, msg)
            self._counter += 1; self._y += 1
            self.pad_refresh()
        if history:
            self.add_to_history((self.write_new_message, author, message))

    def write_ping_message(self, author, message, history=True):
        """
        Write a ping message publish by an user.

        Parameters
        ----------
        author: str
            The author of the message.
        message: str
            The message to write.
        history: [Optional] bool
            Add the message to record history or not.
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()
        list_message = self.split_large_text(f"!!--> {author} : {message}")
        for msg in list_message:
            if self._curses_color:
                self._pad.addstr(self._counter,0, msg, curses.color_pair(2)) # pylint: disable=no-member
            else:
                self._pad.addstr(self._counter,0, msg)
            self._counter += 1; self._y += 1
            self.pad_refresh()
        if history:
            self.add_to_history((self.write_ping_message, author, message))

    def write_system_message(self, data, history=True):
        """
        Write a system message (in red).

        Parameters
        ----------
        data: str
            The data to write.
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()
        list_message = self.split_large_text(data)
        for msg in list_message:
            if self._curses_color:
                self._pad.addstr(self._counter,0, msg, curses.color_pair(1)) # pylint: disable=no-member
            else:
                self._pad.addstr(self._counter,0, msg)
            self._counter += 1; self._y += 1
            self.pad_refresh()
        if history:
            self.add_to_history((self.write_system_message, data))

    def write_signal_message(self, *args, history=True):
        """
        Write signal message (with green color)

        Parameters
        ----------
        *args : *str
            All arg that you want.
        history: [Optional] bool
            Add the message to record history or not.
        """
        if self._counter >= self._max_line*2/3:
            self.re_init()
        message = " ".join(args)
        list_message = self.split_large_text(message)
        for msg in list_message:
            if self._curses_color:
                self._pad.addstr(self._counter,0, msg, curses.color_pair(3)) # pylint: disable=no-member
            else:
                self._pad.addstr(self._counter,0, msg)
            self._counter += 1; self._y += 1

        self.pad_refresh()
        if history:
            self.add_to_history((self.write_signal_message, *args))

    def write_start_up_message(self, pseudo):
        """
        Write the start up message.

        Parameters
        ----------
        pseudo: str
            The user pseudo.
        """
        pseudo = pseudo[:-10] + "#" + pseudo[-10:]
        self.write_system_message("Connection réalisée avec succès")
        self.write_system_message("Voici ton pseudo : ")
        if self._curses_color:
            self._pad.addstr(1,19, pseudo, curses.color_pair(2)) # pylint: disable=no-member
        else:
            self._pad.addstr(1,19, pseudo)
        self.write_system_message("Voir les différentes commandes possibles : /help")
        self.write_system_message("Voici une liste de racourcis clavier :")
        self.write_system_message("Ctrl+h = Backspace = supprime le caractere arriere")
        self.write_system_message("Ctrl+G = envoyé un message")
        self.write_signal_message("Si vous modifiez la taille de la fenetre, envoyez un message blanc (ctrl+G)")
        self.pad_refresh()

    def PadUP(self, nb):
        """
        Go up in history message.

        Parameters
        ----------
        nb: int
            The number to up.
        """
        if self._y - nb <= 0:
            self._y = (self._lry - self._uly) + 2
        else:
            self._y -= nb
        self.pad_refresh()

    def PadDOWN(self, nb):
        """
        Go down in history message.

        Parameters
        ----------
        nn: int
            The number to down.
        """
        if self._y + nb >= self._counter:
            self._y = self._counter
        else:
            self._y += nb
        self.pad_refresh()

    def pad_refresh(self):
        """Refresh pad screen to be in the right position self._y."""
        if self._y <= (self._lry - self._uly) - 1:
            self._pad.refresh(0,0, self._uly,self._ulx, self._lry,self._lrx)
        else:
            pos_y = self._y - (self._lry - self._uly) + 1
            self._pad.refresh(pos_y,0, self._uly,self._ulx, self._lry,self._lrx)

    def add_to_history(self, data):
        """
        Get a trace of the last message.

        Parameters
        ----------
        data: Any
            Data to record
        """
        if len(self._history) > self._max_line*(1/4):
            del self._history[0]
        self._history.append(data)
        if self._is_history_file:
            with open("assets/document/data/history.txt", "a") as fd:
                fd.write("\n"+" ".join(data[1:]))

    @staticmethod
    def split_large_text(data):
        """
        Split text to fit in the window.

        Parameters
        ----------
        data: str
            The whole data to write.

        Returns
        -------
        list
            List of split message.
        """
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
