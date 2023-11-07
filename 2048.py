import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 10
WIDTH = GRID_SIZE * TILE_SIZE
HEIGHT = GRID_SIZE * TILE_SIZE

# Colors
WHITE = (255, 255, 255)

# Define custom colors for tiles
TILE_COLORS = {
    0: (192, 192, 192),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 128, 0),
    16: (255, 64, 64),
    32: (255, 0, 0),
    64: (255, 0, 255),
    128: (128, 0, 255),
    256: (0, 0, 255),
    512: (0, 128, 255),
    1024: (0, 192, 192),
    2048: (0, 255, 0),
    4096: (128, 128, 0),
    8192: (0, 128, 0),
    16384: (0, 192, 192),
    32768: (0, 128, 255),
    65536: (128, 0, 255),
    131072: (192, 192, 192)
}

# Initialize the game board
board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Function to add a new tile (2 or 4) to the board
def add_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

# Function to move the board in a given direction (left, right, up, or down)
def move_board(board, direction):
    if direction == "left":
        return [merge_row(slide_row(row)) for row in board]
    elif direction == "right":
        return [row[::-1] for row in [merge_row(slide_row(row[::-1])) for row in board]]
    elif direction == "up":
        board = [list(col) for col in zip(*board)]
        board = [merge_row(slide_row(row)) for row in board]
        return [list(col) for col in zip(*board)]
    elif direction == "down":
        board = [list(col) for col in zip(*board)]
        board = [row[::-1] for row in [merge_row(slide_row(row[::-1])) for row in board]]
        return [list(col) for col in zip(*board)]
    return board

# Function to move tiles in a row to the left
def slide_row(row):
    new_row = [tile for tile in row if tile != 0]
    while len(new_row) < GRID_SIZE:
        new_row.append(0)
    return new_row

# Function to merge tiles in a row to the left
def merge_row(row):
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
    return row

# Initialize the game with two random tiles
add_tile(board)
add_tile(board)

# Initialize the Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("2048 Game")

# Function to draw the game board
def draw_board(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            color = TILE_COLORS.get(value, (0, 0, 0))
            pygame.draw.rect(window, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                board = move_board(board, "left")
                add_tile(board)
            elif event.key == pygame.K_RIGHT:
                board = move_board(board, "right")
                add_tile(board)
            elif event.key == pygame.K_UP:
                board = move_board(board, "up")
                add_tile(board)
            elif event.key == pygame.K_DOWN:
                board = move_board(board, "down")
                add_tile(board)

    window.fill(WHITE)
    draw_board(board)
    pygame.display.flip()

pygame.quit()
