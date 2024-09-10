import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 512, 700
BOARD_SIZE = 512
SQUARE_SIZE = BOARD_SIZE // 8
FPS = 60
LABEL_OFFSET = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# Load images
blue_square = pygame.image.load('green_square.png')
white_square = pygame.image.load('white_square.png')

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Square Trainer")

def get_square_name(row, col: int):
    return f"{chr(97 + col)}{8 - row}"

def get_square_position(square_name: str) -> tuple:
    col = ord(square_name[0]) - 97
    row = 8 - int(square_name[1])
    return row, col

class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = LIGHT_BLUE if self.active else BLACK
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen = screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

class ChessTrainer:
    def __init__(self, sequence_length=10, time_limit=3, max_errors=3):
        self.sequence_length = sequence_length
        self.time_limit = time_limit
        self.max_errors = max_errors
        self.current_sequence = []
        self.current_index = 0
        self.score = 0
        self.errors = 0
        self.start_time = 0

    def generate_sequence(self):
        self.current_sequence = [get_square_name(random.randint(0, 7), random.randint(0, 7)) 
                                 for _ in range(self.sequence_length)]
        self.current_index = 0
        self.start_time = time.time()

    def check_click(self, pos: tuple) -> str:
        x, y = pos
        clicked_row, clicked_col = (y - (HEIGHT - BOARD_SIZE)) // SQUARE_SIZE, x // SQUARE_SIZE
        clicked_square = get_square_name(clicked_row, clicked_col)
        
        if clicked_square == self.current_sequence[self.current_index]:
            self.score += 1
            self.current_index += 1
            self.start_time = time.time()
            if self.current_index >= len(self.current_sequence):
                return "SEQUENCE_COMPLETE"
        else:
            self.errors += 1
            if self.errors >= self.max_errors:
                return "GAME_OVER"
        
        return "CONTINUE"

    def draw(self, screen: pygame.Surface):
        # Draw chessboard
        for row in range(8):
            for col in range(8):
                x, y = col * SQUARE_SIZE, row * SQUARE_SIZE + (HEIGHT - BOARD_SIZE)
                if (row + col) % 2 == 0:
                    screen.blit(white_square, (x, y))
                else:
                    screen.blit(blue_square, (x, y))

        # Draw labels
        font = pygame.font.Font(None, 24)
        for i in range(8):
            # Draw letter labels (a-h)
            letter = chr(97 + i)
            text = font.render(letter, True, BLACK)
            screen.blit(text, (i * SQUARE_SIZE + SQUARE_SIZE // 2 - text.get_width() // 2, HEIGHT - LABEL_OFFSET - text.get_height()))
            
            # Draw number labels (1-8)
            number = str(8 - i)
            text = font.render(number, True, BLACK)
            screen.blit(text, (LABEL_OFFSET, i * SQUARE_SIZE + (HEIGHT - BOARD_SIZE) + SQUARE_SIZE // 2 - text.get_height() // 2))

        # Draw stats
        font = pygame.font.Font(None, 36)
        stats = [
            f"Target: {self.current_sequence[self.current_index]}",
            f"Score: {self.score}",
            f"Errors: {self.errors}/{self.max_errors}",
            f"Time: {max(0, self.time_limit - (time.time() - self.start_time)):.1f}"
        ]
        for i, stat in enumerate(stats):
            text = font.render(stat, True, BLACK)
            screen.blit(text, (10, 10 + i * 40))

def draw_game_over(screen: pygame.Surface, score: int):
    screen.fill(GRAY)
    font = pygame.font.Font(None, 64)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 3 - text.get_height() // 2))
    
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - score_text.get_height() // 2))
    
    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press SPACE to restart", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 2 * HEIGHT // 3 - restart_text.get_height() // 2))

def draw_start_menu(screen, time_input, lives_input):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 64)
    title = font.render("Chess Square Trainer", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

    font = pygame.font.Font(None, 36)
    time_text = font.render("Time per square (seconds):", True, BLACK)
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 200))

    lives_text = font.render("Number of lives:", True, BLACK)
    screen.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, 300))

    start_text = font.render("Press ENTER to start", True, BLACK)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 500))

    time_input.draw(screen)
    lives_input.draw(screen)

def main():
    clock = pygame.time.Clock()
    time_input = InputBox(WIDTH // 2 - 100, 250, 200, 32, '3')
    lives_input = InputBox(WIDTH // 2 - 100, 350, 200, 32, '3')

    running = True
    in_start_menu = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if in_start_menu:
                time_input.handle_event(event)
                lives_input.handle_event(event)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    try:
                        time_limit = float(time_input.text)
                        max_errors = int(lives_input.text)
                        trainer = ChessTrainer(time_limit=time_limit, max_errors=max_errors)
                        trainer.generate_sequence()
                        in_start_menu = False
                    except ValueError:
                        print("Invalid input. Please enter valid numbers.")
            elif not game_over:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = trainer.check_click(event.pos)
                    if result == "SEQUENCE_COMPLETE":
                        print("Sequence complete! Generating new sequence.")
                        trainer.generate_sequence()
                    elif result == "GAME_OVER":
                        game_over = True
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    in_start_menu = True
                    game_over = False

        screen.fill(WHITE)
        
        if in_start_menu:
            draw_start_menu(screen, time_input, lives_input)
        elif not game_over:
            trainer.draw(screen)
            
            if time.time() - trainer.start_time > trainer.time_limit:
                trainer.errors += 1
                if trainer.errors >= trainer.max_errors:
                    game_over = True
                else:
                    trainer.current_index += 1
                    if trainer.current_index >= len(trainer.current_sequence):
                        print("Sequence complete! Generating new sequence.")
                        trainer.generate_sequence()
                    else:
                        trainer.start_time = time.time()
        else:
            draw_game_over(screen, trainer.score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()