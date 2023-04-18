
from utils import *


def diag(a,b):
    lis1 = []
    lis2 = []
    j = 0
    for i in range(len(a)):
        x = a[i] + b[i]
        lis1.append(x)
        j = len(a) - i - 1
        x = a[i] + b[j]
        lis2.append(x)
    return [lis1,lis2]




row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units = diag(rows,cols)
unitlist = row_units + column_units + square_units + diagonal_units

# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy."""
    
    # Find all instances of naked twins
    naked_twins = []
    for unit in unitlist:
        # Get boxes with only 2 digits
        two_digit_boxes = [box for box in unit if len(values[box]) == 2]  
        
        # Get potential twins 
        potential_twins = set(two_digit_boxes)        
        # Check if we have 2 boxes with the same digits                              
        for box1 in two_digit_boxes:            
            if two_digit_boxes.count(box1) == 2:
                naked_twins.append((unit, values[box1])) 
                
    # Eliminate the naked twins as possibilities for their peers
    for unit, twin in naked_twins:
        for box in unit:
            if box not in potential_twins:
                for digit in twin:
                    values[box] = values[box].replace(digit, '')
                    # if len(values[box]) == 1:
                    #     history[box] = values[box]  

    return values#,history


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
            # if len(values[peer]) == 1:
            #     history[peer] = values[peer]
    return values#,history
    


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
                #history[dplaces[0]] = digit
    return values#,history
     


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values#,history


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False
            
    if solved(values):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    box,value = choose_min(values)
            
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for i in value:
        new_values = values.copy()
        new_values[box] = i 
        #history[box] = i
        solve = search(new_values)
        if solve :
            return solve


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid) 
    display(result)


    # import PySudoku
    # PySudoku.play(grid2values(diag_sudoku_grid), result,history)

    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
