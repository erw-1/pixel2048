import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
TILE_SIZE = 10  # Increase the tile size for better visibility
GRID_WIDTH = GRID_SIZE * TILE_SIZE
GRID_HEIGHT = GRID_SIZE * TILE_SIZE
SCORE_WIDTH = 100  # Width of the score display area
BIGGEST_TILE_WIDTH = 200  # Width of the biggest tile display area
WIDTH = GRID_WIDTH + SCORE_WIDTH
HEIGHT = GRID_HEIGHT

# Initialize the score
score = 0

# Initialize the game over flag
game_over = False

# Initialize the highest score
high_score = 0

# Load the highest score from the highscore.txt file
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    # If the file doesn't exist, create it and initialize the high score to 0
    with open("highscore.txt", "w") as file:
        file.write("0")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initialize the current biggest tile
current_biggest_tile = 0

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

# Function to check for a game over condition
def is_game_over(board):
    # Check if there are any empty cells
    for row in board:
        if 0 in row:
            return False

    # Check if any adjacent tiles can merge horizontally
    for row in board:
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1]:
                return False

    # Check if any adjacent tiles can merge vertically
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE - 1):
            if board[j][i] == board[j + 1][i]:
                return False

    return True

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

# Function to merge tiles in a row to the left and update the score
def merge_row(row):
    global score, current_biggest_tile, high_score
    for i in range(GRID_SIZE - 1):
        if row[i] == row[i + 1] and row[i] != 0:
            row[i] *= 2
            row[i + 1] = 0
            # Update the score when merging tiles
            score += row[i]
            if row[i] > current_biggest_tile:
                current_biggest_tile = row[i]

    # Update the high score if the current score is higher
    if score > high_score:
        high_score = score
        with open("highscore.txt", "w") as file:
            file.write(str(high_score))

    return row
# Initialize the game with two random tiles
add_tile(board)
add_tile(board)

# Initialize the Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("2048 Game")

# Initialize the font for rendering text
font = pygame.font.Font(None, 15)

# Function to render and display the score, biggest tile, game over, and high score on the game window
def draw_info():
    y_position = 1  # Initial vertical position

    # Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    score_rect = score_text.get_rect()
    score_rect.topleft = (GRID_WIDTH + 10, y_position)  # Adjust the position as needed
    window.blit(score_text, score_rect)

    y_position += 10  # Adjust the vertical position for the next element

    # Biggest Tile
    biggest_tile_text = font.render(f"Max tile: {current_biggest_tile}", True, (0, 0, 0))
    biggest_tile_rect = biggest_tile_text.get_rect()
    biggest_tile_rect.topleft = (GRID_WIDTH + 10, y_position)  # Adjust the position as needed
    window.blit(biggest_tile_text, biggest_tile_rect)

    y_position += 10  # Adjust the vertical position for the next element

    # High Score
    high_score_text = font.render(f"Highest: {high_score}", True, (0, 0, 0))
    high_score_rect = high_score_text.get_rect()
    high_score_rect.topleft = (GRID_WIDTH + 10, y_position)  # Adjust the position as needed
    window.blit(high_score_text, high_score_rect)

    y_position += 10
    # Game Over
    if game_over:
        game_over_text = font.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect()
        game_over_rect.topleft = (GRID_WIDTH + 10, y_position)  # Center the game over message
        window.blit(game_over_text, game_over_rect)
        y_position += 10  # Adjust the vertical position for the next element


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

        if not game_over:
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

            # Check for the game over condition
            if is_game_over(board):
                game_over = True

    window.fill(WHITE)
    draw_board(board)
    draw_info()  # Display the score, biggest tile, game over, and high score closely
    pygame.display.flip()

pygame.quit()