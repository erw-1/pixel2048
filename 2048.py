import pygame
import random

# Constants
GRID_SIZE = 4
TILE_SIZE = 12
GRID_WIDTH = GRID_SIZE * TILE_SIZE
GRID_HEIGHT = GRID_SIZE * TILE_SIZE
TXT_WIDTH = 120
WIDTH = GRID_WIDTH + TXT_WIDTH
HEIGHT = GRID_HEIGHT

# Colors
WHITE = (255, 255, 255)
GREY = (60, 60, 60)
RED = (255, 60, 60)

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

# Class to manage the game
class Game2048:
    current_biggest_tile = 0  # Define current_biggest_tile as a class attribute

    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Initialize game variables and data structures
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_over = False
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

        # Initialize Pygame window
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
        pygame.display.set_caption("2048 Game")

        # Initialize the font for rendering text
        self.font = pygame.font.Font(None, 15)

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            with open("highscore.txt", "w") as file:
                file.write("0")
            return 0

    def is_game_over(self):
        if any(0 in row for row in self.board):
            return False

        for row in self.board:
            for i in range(GRID_SIZE - 1):
                if row[i] == row[i + 1]:
                    return False

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.board[j][i] == self.board[j + 1][i]:
                    return False

        return True

    def add_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def slide_row(self, row):
        new_row = [tile for tile in row if tile != 0]
        while len(new_row) < GRID_SIZE:
            new_row.append(0)
        return new_row

    def merge_row(self, row):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
                if row[i] > Game2048.current_biggest_tile:
                    Game2048.current_biggest_tile = row[i]  # Update class attribute

        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as file:
                file.write(str(self.high_score))

        return row

    def move_board(self, direction):
        if direction == "left":
            return [self.merge_row(self.slide_row(row)) for row in self.board]
        elif direction == "right":
            return [row[::-1] for row in [self.merge_row(self.slide_row(row[::-1])) for row in self.board]]
        elif direction == "up":
            board = [list(col) for col in zip(*self.board)]
            board = [self.merge_row(self.slide_row(row)) for row in board]
            return [list(col) for col in zip(*board)]
        elif direction == "down":
            board = [list(col) for col in zip(*self.board)]
            board = [row[::-1] for row in [self.merge_row(self.slide_row(row[::-1])) for row in board]]
            return [list(col) for col in zip(*board)]
        return self.board

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.board = self.move_board("left")
                self.add_tile()
            elif event.key == pygame.K_RIGHT:
                self.board = self.move_board("right")
                self.add_tile()
            elif event.key == pygame.K_UP:
                self.board = self.move_board("up")
                self.add_tile()
            elif event.key == pygame.K_DOWN:
                self.board = self.move_board("down")
                self.add_tile()
            if self.is_game_over():
                self.game_over = True

    def draw_info(self):
        y_position = 1
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (GRID_WIDTH + 10, y_position)
        self.window.blit(score_text, score_rect)
        y_position += 10

        biggest_tile_text = self.font.render(f"Max tile: {Game2048.current_biggest_tile}", True, WHITE)
        biggest_tile_rect = biggest_tile_text.get_rect()
        biggest_tile_rect.topleft = (GRID_WIDTH + 10, y_position)
        self.window.blit(biggest_tile_text, biggest_tile_rect)
        y_position += 10

        high_score_text = self.font.render(f"Highest: {self.high_score}", True, WHITE)
        high_score_rect = high_score_text.get_rect()
        high_score_rect.topleft = (GRID_WIDTH + 10, y_position)
        self.window.blit(high_score_text, high_score_rect)
        y_position += 10

        if self.game_over:
            game_over_text = self.font.render("Game Over", True, RED)
            game_over_rect = game_over_text.get_rect()
            game_over_rect.topleft = (GRID_WIDTH + 10, y_position)
            self.window.blit(game_over_text, game_over_rect)
            y_position += 10

    def draw_board(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color = TILE_COLORS.get(value, (0, 0, 0))
                pygame.draw.rect(self.window, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def render(self):
        self.window.fill(GREY)
        self.draw_board()
        self.draw_info()
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if not self.game_over:
                    self.handle_event(event)
            self.render()
        pygame.quit()

if __name__ == "__main__":
    game = Game2048()
    game.run()