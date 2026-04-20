# Diagonal Sudoku Solver

A constraint-propagation + depth-first search solver for **diagonal Sudoku** puzzles, with an animated `pygame` visualization that replays every deduction the solver makes, in order.

The project began as Udacity's AIND "Solve Sudoku with AI" assignment, but has grown beyond the starter scaffold: the solver tracks an assignment history so the visualizer can replay the solving process step-by-step, picks branching variables using a minimum-remaining-values heuristic, and ships with two visualization front-ends (a polished board renderer and a minimal animation harness).

## What "diagonal Sudoku" means

Standard Sudoku requires the digits 1–9 to appear exactly once in every row, column, and 3×3 box. Diagonal Sudoku adds two more constraints: each of the two main diagonals must also contain 1–9. This makes many "easy" puzzles considerably tighter and gives the constraint-propagation strategies more leverage.

## How it solves

The solver alternates two phases until the puzzle is either solved or proven unsolvable:

### 1. Constraint propagation ([solution.py:98](solution.py#L98))

`reduce_puzzle()` repeatedly applies three strategies until no box changes:

- **Eliminate** ([solution.py:44](solution.py#L44)) — if a box is solved, remove its digit from all of its peers (row, column, 3×3 box, and diagonals if applicable).
- **Only Choice** ([solution.py:71](solution.py#L71)) — if a digit can only legally land in one box of a unit, assign it there.
- **Naked Twins** ([solution.py:16](solution.py#L16)) — if two boxes in a unit share the same exact pair of candidates, no other box in that unit can contain those two digits, so they get stripped from the rest of the unit.

### 2. Depth-first search ([solution.py:125](solution.py#L125))

When propagation stalls, `search()` picks the unsolved box with the **fewest remaining candidates** (a minimum-remaining-values heuristic, implemented in `choose_min()` at [utils.py:111](utils.py#L111)), branches on each candidate, and recursively tries to solve the resulting puzzle. Backtracking happens automatically when a branch leads to a contradiction.

### Units, peers, and the diagonals

The board's structure is built up at module load time in [solution.py:5-13](solution.py#L5-L13). The diagonals are produced by a small helper, `diag()` ([utils.py:98](utils.py#L98)), which generates both main diagonals from the row and column labels and appends them to the standard `unitlist`. From there `extract_units` and `extract_peers` derive the per-box lookup tables the strategies use.

### Solving history

Every assignment is recorded in a `history` dict that flows through every strategy. The visualizer consumes this log to animate the solve in the same order the algorithm discovered each value — rather than just flashing the final answer onto the board.

## Running it

```bash
python solution.py
```

This will solve the built-in diagonal puzzle, print the solved grid to the terminal, and (if `pygame` is installed) launch the animated visualization.

To use a different puzzle, edit `diag_sudoku_grid` at the bottom of [solution.py](solution.py). The grid is an 81-character string read row-major, with `.` for empty cells.

### Tests

```bash
python -m unittest -v
```

The local suite in [tests/test_solution.py](tests/test_solution.py) exercises the diagonal-units setup, the naked-twins reduction, and the end-to-end solve.

## Visualization

Two pygame front-ends ship with the project:

- **[PySudoku.py](PySudoku.py)** — the main visualizer. Renders the puzzle on top of `images/sudoku-board-bare.jpg` and replays the solver's `history` so you can watch each deduction land on the board.
- **[naive.py](naive.py)** — a minimal animation that simply fills cells in row-major order. Useful as a sanity check when `PySudoku.py`'s assets aren't available.

`pygame` is an optional dependency; if it's missing, `solution.py` still solves the puzzle and prints the result — it just skips the animation.

## Project layout

| File | Purpose |
| --- | --- |
| [solution.py](solution.py) | Solver: strategies, propagation loop, search, entry point |
| [utils.py](utils.py) | Board construction, peer/unit extraction, grid I/O, MRV heuristic, history-aware `assign_value` |
| [PySudoku.py](PySudoku.py) | Animated pygame visualizer driven by the solver's history log |
| [SudokuSquare.py](SudokuSquare.py) | Per-cell render primitives used by `PySudoku.py` |
| [GameResources.py](GameResources.py) | Pygame asset loader |
| [naive.py](naive.py) | Minimal alternative visualization |
| [tests/test_solution.py](tests/test_solution.py) | Local unit tests |
| [images/](images/) | Board background and other visual assets |

## Acknowledgements

The original problem statement, starter constraints, and the naked-twins formulation come from Udacity's Artificial Intelligence Nanodegree. Everything in the solver, the history-based replay, the MRV branching, and the visualization wiring is implemented in this repo.
