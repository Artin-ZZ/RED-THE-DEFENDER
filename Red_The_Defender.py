import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RED THE DEFENDER")

# Colors
CYAN = (50, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)


# Button class for menu buttons
class Button:
    def __init__(self, text, font, color, x, y, width, height):
        self.text = text
        self.font = font
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        self.draw_text()

    def draw_text(self):
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return (self.x < mouse_pos[0] < self.x + self.width and
                self.y < mouse_pos[1] < self.y + self.height)


# Main menu class
class MainMenu:
    def __init__(self):
        self.play_button = Button("Play", font, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        self.exit_button = Button("Exit", font, RED, WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.is_clicked(mouse_pos):
                    return "play"
                elif self.exit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()

    def draw(self):
        screen.fill(CYAN)
        self.play_button.draw()
        self.exit_button.draw()


# Game class
class Game:
    def __init__(self):
        self.player_width, self.player_height = 50, 50
        self.player_x = (WIDTH - self.player_width) // 2
        self.player_y = HEIGHT - self.player_height - 20
        self.player_speed = 10

        self.bullet_width, self.bullet_height = 10, 20
        self.bullet_speed = 15
        self.bullets = []

        self.enemy_width, self.enemy_height = 50, 50
        self.enemy_speed = 5
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60

        self.score = 0
        self.game_over = False

        self.game_over_label = font.render("Game Over", True, RED)
        self.game_over_rect = self.game_over_label.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    def handle_events(self):
        if not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bullets.append([self.player_x + self.player_width // 2 - self.bullet_width // 2, self.player_y])

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player_x > 0:
                self.player_x -= self.player_speed
            if keys[pygame.K_RIGHT] and self.player_x < WIDTH - self.player_width:
                self.player_x += self.player_speed

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < WIDTH - self.player_width:
            self.player_x += self.player_speed

    def move_bullets(self):
        for bullet in self.bullets:
            bullet[1] -= self.bullet_speed

    def spawn_enemy(self):
        x = random.randint(0, WIDTH - self.enemy_width)
        y = random.randint(-self.enemy_height, -10)
        self.enemies.append([x, y])

    def move_enemies(self):
        if not self.game_over:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_delay:
                self.spawn_enemy()
                self.enemy_spawn_timer = 0

            for enemy in self.enemies:
                enemy[1] += self.enemy_speed

            # Check if any enemy has reached the bottom of the screen
            for enemy in self.enemies:
                if enemy[1] > HEIGHT:
                    self.game_over = True

    def check_collisions(self):
        for bullet in self.bullets:
            for enemy in self.enemies:
                if (bullet[0] + self.bullet_width > enemy[0] and
                    bullet[0] < enemy[0] + self.enemy_width and
                    bullet[1] < enemy[1] + self.enemy_height and
                    bullet[1] + self.bullet_height > enemy[1]):
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    self.score += 1

    def draw(self):
        screen.fill(CYAN)

        for bullet in self.bullets:
            pygame.draw.rect(screen, RED, (bullet[0], bullet[1], self.bullet_width, self.bullet_height))
        for enemy in self.enemies:
            pygame.draw.rect(screen, BLACK, (enemy[0], enemy[1], self.enemy_width, self.enemy_height))
        pygame.draw.rect(screen, RED, (self.player_x, self.player_y, self.player_width, self.player_height))

        self.draw_text(f"Score: {self.score}", font, BLACK, WIDTH // 2, 50)

        if self.game_over:
            screen.blit(self.game_over_label, self.game_over_rect)

    def draw_text(self, text, font, color, x, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)


# Main function
def main():
    main_menu = MainMenu()
    game = Game()
    while True:
        choice = main_menu.handle_events()
        if choice == "play":
            game_loop(game)
        main_menu.draw()  # Draw main menu each frame
        pygame.display.flip()


# Game loop function
def game_loop(game):
    while True:
        game.handle_events()
        game.move_player()
        game.move_bullets()
        game.move_enemies()
        game.check_collisions()
        game.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()