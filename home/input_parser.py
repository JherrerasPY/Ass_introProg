from emitter import Emitter
from receiver import Receiver
from mirror import Mirror

'''
Name:   Javier Herrera Saavedra
SID:    540159552
Unikey: jher0112

input_parser - A module that parses the inputs of the program. 
We define parsing as checking the validity of what has been entered 
to determine if it's valid. If it's not valid, an appropriate message 
should be printed. Whenever we retrieve input in the program, we 
should be using functions from this module to validate it.

You are free to add more functions, as long as you aren't modifying the
existing scaffold.
'''
emitter_constraint = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
direction_constraint = ['N', 'E', 'S', 'W']
receiver_constraint = ['R0', 'R1', 'R2',
                       'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9']


def parse_size(user_input: str) -> tuple[int, int] | None:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Checks if user_input is a valid input for the size of the circuit board by
    performing the following checks:
      1)  user_input contains exactly 2 tokens. If there are 2 tokens, we
          interpret the first token as width and the second token as height for
          the remaining checks.
      2)  width is an integer.
      3)  height is an integer.
      4)  width is greater than zero.
      5)  height is greater than zero.

    Parameters
    ----------
    user_input - the user input for the circuit's board size

    Returns
    -------
    If all checks pass, returns a tuple containing the width and height of
    the circuit board.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.

    Example 1:
    >>> size = parse_size('18 0')
    Error: height must be positive
    >>> size
    None

    Example 2:
    >>> size = parse_size('18 6')
    >>> size
    (18, 6)
    '''
    check1 = False
    check2 = False
    check3 = False
    check4 = False
    check5 = False
    # Check1: exactly 2 tokens
    size_list = user_input.split()
    if len(size_list) == 2:
        check1 = True
        # Check2: width is integer
        try:
            width_input = int(size_list[0])
            if isinstance(width_input, int):
                check2 = True
                # Check3: height is integer
                try:
                    height_input = int(size_list[1])
                    if isinstance(height_input, int):
                        check3 = True
                        # Check4: width greater than Zero
                        if width_input > 0:
                            check4 = True
                            # Check5: height greater than Zero
                            if height_input > 0:
                                check5 = True
                            else:
                                print("Error: height must be greater than zero")
                        else:
                            print("Error: width must be greater than zero")
                except:
                    print("Error: height is not an integer")
        except:
            print("Error: width is not an integer")
    else:
        print("Error: <width> <height>")

    # if all test passed
    if check1 and check2 and check3 and check4 and check5:
        return (width_input, height_input)
    return None


def parse_emitter(user_input: str) -> Emitter | None:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Checks if user_input is a valid input for creating an emitter by
    performing the following checks in order for any errors: 
      1)  user_input contains exactly 3 tokens. If there are 3 tokens, we 
          interpret the first token  as symbol, the second token as x and the 
          third token as y for the remaining checks.
      2)  symbol is a character between 'A' to 'J'. 
      3)  x is an integer.
      4)  y is an integer.
      5)  x is greater than 0.
      6)  y is greater than 0

    Parameters
    ----------
    user_input - the user input for creating a new emitter

    Returns
    -------
    If all checks pass, returns a new Emitter instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.
    '''
    check1 = False
    check2 = False
    check3 = False
    check4 = False
    check5 = False
    check6 = False

    # Check1: contains 3 tokens
    emitter_list = user_input.split()
    if len(emitter_list) == 3:
        check1 = True
        # Check2: symbol is character between "A" and "J"
        i = 0
        in_list = False
        while i < len(emitter_constraint):
            if emitter_list[0] == emitter_constraint[i]:
                in_list = True
                break
            i += 1
        if in_list:
            check2 = True
            # Check3: x is an integer
            try:
                x_input = int(emitter_list[1])
                if isinstance(x_input, int):
                    check3 = True
                    # Check4: y is and integer
                    try:
                        y_input = int(emitter_list[2])
                        if isinstance(y_input, int):
                            check4 = True
                            # Check5: x is not negative
                            if x_input >= 0:
                                check5 = True
                                # Check6: y is not negative
                                if y_input >= 0:
                                    check6 = True
                                else:
                                    print("Error: y cannot be negative")
                            else:
                                print("Error: x cannot be negative")
                    except:
                        print("Error: y is not an integer")
            except:
                print("Error: x is not an integer")
        else:
            print("Error: symbol is not between 'A'-'J'")
    else:
        print("Error: <symbol> <x> <y>")

    if check1 and check2 and check3 and check4 and check5 and check6:
        new_emitter = Emitter(emitter_list[0], x_input, y_input)
        return new_emitter
    return None


def parse_receiver(user_input: str) -> Receiver | None:
    # only requires implementation once you reach GET-MY-INPUTS
    '''
    Identical to parse_emitter, with the only differences being
    that the symbol must be between 'R0' to 'R9', and that a new Receiver
    instance is returned if all checks pass.

    Parameters
    ----------
    user_input - the user input for creating a new receiver

    Returns
    -------
    If all checks pass, returns a new Receiver instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''
    check1 = False
    check2 = False
    check3 = False
    check4 = False
    check5 = False
    check6 = False

    # Check1: contains 3 tokens
    receiver_list = user_input.split()
    if len(receiver_list) == 3:
        check1 = True
        # Check2: symbol is character between "R0" and "R9"
        i = 0
        in_list = False
        while i < len(receiver_constraint):
            if receiver_list[0] == receiver_constraint[i]:
                in_list = True
                break
            i += 1
        if in_list:
            check2 = True
            # Check3: x is an integer
            try:
                x_input = int(receiver_list[1])
                if isinstance(x_input, int):
                    check3 = True
                    # Check4: y is and integer
                    try:
                        y_input = int(receiver_list[2])
                        if isinstance(y_input, int):
                            check4 = True
                            # Check5: x is not negative
                            if x_input >= 0:
                                check5 = True
                                # Check6: y is not negative
                                if y_input >= 0:
                                    check6 = True
                                else:
                                    print("Error: y cannot be negative")
                            else:
                                print("Error: x cannot be negative")
                    except:
                        print("Error: y is not an integer")
            except:
                print("Error: x is not an integer")
        else:
            print("Error: symbol is not between R0-R9")
    else:
        print("Error: <symbol> <x> <y>")

    if check1 and check2 and check3 and check4 and check5 and check6:
        new_receiver = Receiver(receiver_list[0], x_input, y_input)
        return new_receiver
    return None


def parse_pulse_sequence(line: str) -> tuple[str, int, str] | None:
    # only requires implementation once you reach RUN-MY-CIRCUIT
    '''
    Checks if line is valid for setting the pulse sequence of an emitter by
    performing the following checks in order for any errors:
      1)  line contains exactly 3 tokens.
          If there are 3 tokens, we interpret the first token as symbol, the
          second token as frequency and the third token as direction for the
          remaining checks.
      2)  symbol is a character between 'A' to 'J'.
      3)  frequency is an integer.
      4)  frequency is greater than zero.
      5)  direction is either 'N', 'E', 'S' or 'W'.

    Parameters
    ----------
    line -- a line from the pulse_sequence.in file

    Returns
    -------
    If all checks pass, returns a tuple containing the specified symbol,
    frequency and direction which can be used for setting the pulse sequence
    of the emitter.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''
    tokens = line.split()
    # Checks
    # check 1: 3 tokens
    if len(tokens) != 3:
        print("Error: <symbol> <frequency> <direction>")
        return
    symbol: str = tokens[0]
    frequency: int = tokens[1]
    direction: str = tokens[2]
    # check 2: symbol character
    sym_character = False
    i = 0
    while i < len(emitter_constraint):
        if symbol == emitter_constraint[i]:
            sym_character = True
            break
        i += 1
    if not sym_character:
        print("Error: symbol is not between 'A'-'J'.")
        return
    # check 3: frequency integer
    try:
        frequency = int(frequency)
    except:
        print("Error: frequency is not an integer.")
        return
    # check 4: frecuency > 0
    if not frequency > 0:
        print("Error: frequency must be greater than zero")
        return
    # check 5: direction in NESW
    dir_character = False
    i = 0
    while i < len(direction_constraint):
        if direction == direction_constraint[i]:
            dir_character = True
            break
        i += 1
    if not dir_character:
        print("Error: direction must be 'N', 'E', 'S' or 'W'")
        return
    return (symbol, frequency, direction)


def parse_mirror(user_input: str) -> Mirror | None:
    # only requires implementation once you reach ADD-MY-MIRRORS
    '''
    Checks if user_input is a valid input for creating a mirror by performing
    the following checks in order for any errors:
      1)  user_input contains exactly 3 tokens. If there are 3 tokens, we
          interpret the first token  as symbol, the second token as x and the
          third token as y for the remaining checks.
      2)  symbol is either '/', '\', '>', '<', '^', or 'v'.
      3)  x is an integer.
      4)  y is an integer.
      5)  x is greater than 0.
      6)  y is greater than 0.

    Parameters
    ----------
    user_input - the user input for creating a mirror

    Returns
    -------
    If all checks pass, returns a new Mirror instance with the specified
    symbol, x and y position set.
    Else, if at any point a check fails, prints an error message stating the cause
    of the error and returns None, skipping any further checks.    
    '''
    user_tokens = user_input.split()
    # Check 1
    if len(user_tokens) != 3:
        print("Error: <symbol> <x> <y>")
        return
    symbol = user_tokens[0]
    x = user_tokens[1]
    y = user_tokens[2]
    # Check 2
    if not (symbol == '/' or symbol == '\\' or symbol == '>' or symbol == '<' or symbol == '^' or symbol == 'v'):
        print("Error: symbol must be '/', '\\', '>', '<', '^' or 'v'")
        return
    # Check 3
    try:
        x = int(x)
    except:
        print("Error: x is not an integer")
        return
    # Check 4
    try:
        y = int(y)
    except:
        print("Error: y is not an integer")
        return
    # Check 5
    if x < 0:
        print("Error: x cannot be negative")
        return
    # Check 6
    if y < 0:
        print("Error: y cannot be negative")
        return
    # All test passed
    new_mirror = Mirror(symbol, x, y)
    return new_mirror
