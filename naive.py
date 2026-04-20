import pygame
import time

# Define the dimensions of the puzzle
WIDTH = 540
HEIGHT = 600

# Define the dimensions of each cell
CELL_SIZE = 60

# Define the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Define the puzzle and its solution
puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

solution = [
    [4, 8, 6, 7, 2, 1, 3, 5, 9],
    [2, 3, 1, 5, 9, 8, 6, 7, 4],
    [7, 9, 5, 3, 4, 6, 1, 2, 8],
    [1, 2, 4, 8, 6, 5, 7, 9, 3],
    [3, 5, 9, 1, 7, 4, 2, 8, 6],
    [8, 6, 7, 9, 3, 2, 4, 1, 5],
    [6, 4, 8, 2, 5, 9, 7, 3, 1],
    [5, 1, 2, 6, 8, 3, 9, 4, 7],
    [9, 7, 3, 4, 1, 7, 8, 6, 2]
]

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Define a function to draw the puzzle on the screen
def draw_puzzle(puzzle):
    # Clear the screen
    screen.fill(WHITE)
    
    # Draw the grid
    for i in range(10):
        if i % 3 == 0:
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - CELL_SIZE), 4)
        else:
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(screen, GRAY, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT - CELL_SIZE), 2)
    
    # Draw the numbers
    font = pygame.font.SysFont("Arial", 36)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                text = font.render(str(puzzle[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE / 2, i * CELL_SIZE + CELL_SIZE / 2))
                screen.blit(text, text_rect)
    
    # Update the screen
    pygame.display.update()

# Define a function to animate the solution
def animate_solution(puzzle, solution):
    # Draw the initial puzzle
    draw_puzzle(puzzle)
    
    # Wait for a moment before starting
    time.sleep(1)
    
    # Iterate through each cell in the puzzle
    for i in range(9):
        for j in range(9):
            # If the cell is not filled in the initial puzzle
            if puzzle[i][j] == 0:
                # Fill in the cell with the solution value
                puzzle[i][j] = solution[i][j]
                
                # Draw the updated puzzle
                draw_puzzle(puzzle)
                
                # Wait for a moment
                time.sleep(0.2)

# Animate the solution
animate_solution(puzzle, solution)

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()