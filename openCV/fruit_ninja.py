import pygame
import random
import sys

# Khởi tạo
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FRUIT NINJA - CHƠI BẰNG TAY")

# Màu sắc & Font
WHITE, RED, GREEN, BLACK = (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0)
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)

class Fruit:
    def __init__(self):
        self.x = random.randint(100, WIDTH - 100)
        self.y = HEIGHT
        self.speed_y = random.randint(-18, -13)
        self.speed_x = random.randint(-3, 3)
        self.radius = 35
        self.color = random.choice([RED, (255, 165, 0), GREEN]) # Đỏ, Cam, Xanh
        self.active = True

    def update(self):
        self.speed_y += 0.45 # Trọng lực
        self.x += self.speed_x
        self.y += self.speed_y
        return self.y <= HEIGHT + 50

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

def main_game():
    score = 0
    lives = 3
    fruits = []
    spawn_timer = 0
    clock = pygame.time.Clock()
    
    while lives > 0:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        # Tạo quả
        spawn_timer += 1
        if spawn_timer > 35:
            fruits.append(Fruit())
            spawn_timer = 0

        # Xử lý chém (chuột)
        m_pos = pygame.mouse.get_pos()
        m_pressed = pygame.mouse.get_pressed()[0]

        for f in fruits[:]:
            if not f.update():
                if f.active: lives -= 1 # Rơi mất mạng
                fruits.remove(f)
                continue
            
            # Kiểm tra va chạm
            dist = ((m_pos[0]-f.x)**2 + (m_pos[1]-f.y)**2)**0.5
            if dist < f.radius and m_pressed:
                f.active = False # Chém trúng
                score += 1
            f.draw()

        # UI
        screen.blit(font.render(f"Score: {score}", True, WHITE), (20, 20))
        screen.blit(font.render(f"Lives: {lives}", True, RED), (WIDTH-150, 20))
        pygame.display.flip()
        clock.tick(60)

    # Game Over
    screen.fill(BLACK)
    screen.blit(big_font.render("GAME OVER", True, RED), (WIDTH//2-160, HEIGHT//2-50))
    screen.blit(font.render(f"Score: {score} - Restarting...", True, WHITE), (WIDTH//2-130, HEIGHT//2+40))
    pygame.display.flip()
    pygame.time.delay(3000)
    main_game() # Đệ quy để lặp vô tận

if __name__ == "__main__":
    main_game()