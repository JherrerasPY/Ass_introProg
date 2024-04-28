from emitter import Emitter
from receiver import Receiver
from photon import Photon
from mirror import Mirror

'''
Name:   Javier Herrera Saavedra
SID:    540159552
Unikey: jher0112

BoardDisplayer - A helper class used to display the circuit board.
Each time a component is added to the circuit, this board is updated to 
store the component's symbol in its assigned position on the board.

You are free to add more attributes and methods, as long as you aren't 
modifying the existing scaffold.
'''


class BoardDisplayer:

    def __init__(self, width: int, height: int, colour_frequency_ranges: dict = None):
        '''
        Initialises a BoardDisplayer instance given a width and height 
        which is the size of the circuit board. board should be 
        initialised to the return value of the create_board method.

        width:  int             - the width of this board
        height: int             - the height of this board
        board:  list[list[str]] - a list of list of strings representing the 
                                  circuit board, having the symbol of each 
                                  component and photon in the circuit at its 
                                  assigned position

        Parameters
        ----------
        width  - the width to set this board to
        height - the height to set this board to
        '''
        self.width: int = width
        self.height: int = height
        self.board: list[list[str]] = self.create_board()
        self.colour_frequency_ranges = colour_frequency_ranges

    def create_board(self) -> list[list[str]]:
        '''
        Creates a board of size width x height and returns it.

        Returns
        -------
        Returns a list of list of strings representing an empty circuit 
        board of size width x height.

        Example
        ------- 
        >>> self.width, self.height
        (8, 3)
        >>> create_board() # board split across multiple lines for readability
        [
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        The board above has 3 rows (height), with each row having 8 columns (width).
        Each cell is initialised as a space, which represents an empty cell.
        '''
        self.board = []
        i = 0
        while i < self.height:
            row = self.width * [' ']
            self.board.append(row)
            i += 1
        return self.board

    def change_emitter_format(self, emitter: Emitter, has_emitted: bool) -> None:
        dim = "\033[38;5;245m"
        underline = "\033[4m"
        end_code = "\033[0m"
        emitter_symbol = emitter.get_symbol()
        if not has_emitted:
            emitter_symbol = underline + emitter_symbol + end_code
            self.board[emitter.get_y()][emitter.get_x()] = emitter_symbol
        elif has_emitted:
            emitter_symbol = dim + emitter_symbol + end_code
            self.board[emitter.get_y()][emitter.get_x()] = emitter_symbol

    def change_receiver_format(self, receiver: Receiver, has_activated: bool) -> None:
        dim = "\033[38;5;245m"
        underline = "\033[4m"
        end_code = "\033[0m"
        receiver_symbol = receiver.get_symbol()
        if has_activated:
            receiver_symbol = underline + receiver_symbol + end_code
            self.board[receiver.get_y()][receiver.get_x()] = receiver_symbol
        elif not has_activated:
            receiver_symbol = dim + receiver_symbol + end_code
            self.board[receiver.get_y()][receiver.get_x()] = receiver_symbol

    def add_component_to_board(self, component: Emitter | Receiver | Mirror) -> None:
        '''
        Adds the symbol of the component on the board at its assigned 
        position.

        Parameters
        ----------
        component: the component to add its symbol on the board

        Hint
        ----------
        You shouldn't need to care what type of component you are adding,
        since all components have a symbol, x and y.

        >>> self.board # board split across multiple lines for readability
        [
         [' ', ' ', ' '], 
         [' ', ' ', ' '],
         [' ', ' ', ' ']
        ]
        >>> emitter = Emitter('A', 0, 0)
        >>> receiver = Receiver('R0', 2, 0)
        >>> self.add_component_to_board(emitter)
        >>> self.add_component_to_board(receiver)
        >>> self.board
        [
         ['A', ' ', '0'], 
         [' ', ' ', ' '],
         [' ', ' ', ' ']
        ]      
        '''
        self.board[component.get_y()][component.get_x()
                                      ] = component.get_symbol()

    def add_photon_to_board(self, photon: Photon, show_color: bool = False) -> None:
        # only requires implementation once you reach RUN-MY-CIRCUIT
        '''
        Adds the symbol of the photon on the board at its current position. If
        there already is a component on the board at its position, it should not
        replace it.

        Parameters
        ----------
        photon: the photon to add its symbol on the board
        '''
        # Colour the photon:
        if show_color:
            try:
                photon_frequency = photon.get_frequency()
                color_code = ""
                end_code = "\033[0m"
                if photon_frequency > self.colour_frequency_ranges['violet'][1]:
                    color_code = "\033[35m"
                elif photon_frequency > self.colour_frequency_ranges['blue'][1]:
                    color_code = "\033[34m"
                elif photon_frequency > self.colour_frequency_ranges['cyan'][1]:
                    color_code = "\033[36m"
                elif photon_frequency > self.colour_frequency_ranges['green'][1]:
                    color_code = "\033[32m"
                elif photon_frequency > self.colour_frequency_ranges['yellow'][1]:
                    color_code = "\033[33m"
                elif photon_frequency > self.colour_frequency_ranges['orange'][1]:
                    color_code = "\033[38;5;166m"
                elif photon_frequency > self.colour_frequency_ranges['red'][1]:
                    color_code = "\033[31m"
                else:
                    color_code = "\033[39m"  # NO Change
                # add color
                if self.board[photon.get_y()][photon.get_x()] == ' ':
                    self.board[photon.get_y()][photon.get_x(
                    )] = color_code + photon.get_symbol() + end_code
            except:
                if self.board[photon.get_y()][photon.get_x()] == ' ':
                    self.board[photon.get_y()][photon.get_x()
                                               ] = photon.get_symbol()
        else:  # NO color
            if self.board[photon.get_y()][photon.get_x()] == ' ':
                self.board[photon.get_y()][photon.get_x()
                                           ] = photon.get_symbol()

    def print_board(self) -> None:
        '''
        Prints a formatted board with the border included.

        Example 1
        ---------
        >>> self.board # board split across multiple lines for readability
        [
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], 
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]
        >>> self.print_board()
        +--------+
        |        |         
        |        |
        |        |
        +--------+

        Example 2
        ---------
        >>> self.board # board split across multiple lines for readability
        [
         ['A', ' ', ' ', ' ', ' ', ' ', ' ', '0'], 
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['B', ' ', ' ', ' ', ' ', ' ', ' ', '1']
        ]
        >>> self.print_board()
        +--------+
        |A      0|         
        |        |
        |B      1|
        +--------+

        Example 3
        ---------
        >>> self.board # board split across multiple lines for readability
        [
         ['A', '.', '.', '.', '.', '.', '.', '0'], 
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         ['B', '.', '.', '.', '.', '.', '.', '1']
        ]
        >>> self.print_board()
        +--------+
        |A......0|         
        |        |
        |B......1|
        +--------+
        '''
        top = f"+{self.width*'-'}+"
        board_output = ""
        board_output += top+"\n"
        i = 0
        while i < self.height:
            j = 0
            board_output += "|"
            while j < self.width:
                board_output += self.board[i][j]
                j += 1
            board_output += "|\n"
            i += 1
        board_output += top
        print(board_output)
