import pygame
import random

# Constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
BOARD_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
BOARD_HEIGHT = SCREEN_HEIGHT // BLOCK_SIZE

# Colors
COLORS = [
    (0, 0, 0),  # black
    (255, 0, 0),  # red
    (0, 255, 0),  # green
    (0, 0, 255),  # blue
    (255, 255, 0),  # yellow
    (0, 255, 255),  # cyan
    (255, 0, 255),  # magenta
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

class Tetris:
    def __init__(self):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.current_piece = self.new_piece()
        self.next_piece = self.new_piece()
        self.score = 0
        self.game_over = False

    def new_piece(self):
        shape = random.choice(SHAPES)
        return {'shape': shape, 'x': BOARD_WIDTH // 2 - len(shape[0]) // 2, 'y': 0}

    def rotate_piece(self):
        self.current_piece['shape'] = [list(row) for row in zip(*self.current_piece['shape'][::-1])]

    def move_piece(self, dx):
        if not self.collision(self.current_piece['shape'], self.current_piece['x'] + dx, self.current_piece['y']):
            self.current_piece['x'] += dx

    def drop_piece(self):
        if not self.collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y'] + 1):
            self.current_piece['y'] += 1
        else:
            self.merge_piece()
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.new_piece()
            if self.collision(self.current_piece['shape'], self.current_piece['x'], self.current_piece['y']):
                self.game_over = True

    def collision(self, shape, offset_x, offset_y):
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block and (x + offset_x < 0 or x + offset_x >= BOARD_WIDTH or y + offset_y >= BOARD_HEIGHT or self.board[y + offset_y][x + offset_x]):
                    return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, block in enumerate(row):
                if block:
                    self.board[y + self.current_piece['y']][x + self.current_piece['x']] = 1

    def clear_lines(self):
        lines_to_clear = [i for i in range(BOARD_HEIGHT) if all(self.board[i])]
        self.score += len(lines_to_clear)
        for i in lines_to_clear:
            del self.board[i]
            self.board.insert(0, [0] * BOARD_WIDTH)

    def get_board(self):
        display_board = [row[:] for row in self.board]
        shape = self.current_piece['shape']
        for y, row in enumerate(shape):
            for x, block in enumerate(row):
                if block:
                    display_board[y + self.current_piece['y']][x + self.current_piece['x']] = 1
        return display_board

def draw_board(screen, board, score):
    screen.fill((0, 0, 0))
    for y, row in enumerate(board):
        for x, block in enumerate(row):
            if block:
                pygame.draw.rect(screen, COLORS[1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

tetris = Tetris()

# Main game loop
while not tetris.game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tetris.game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.move_piece(-1)
            elif event.key == pygame.K_RIGHT:
                tetris.move_piece(1)
            elif event.key == pygame.K_DOWN:
                tetris.drop_piece()
            elif event.key == pygame.K_UP:
                tetris.rotate_piece()

    tetris.drop_piece()
    draw_board(screen, tetris.get_board(), tetris.score)
    clock.tick(5)  # Control the speed of the game

pygame.quit()
