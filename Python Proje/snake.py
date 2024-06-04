
#2121221014-2121221011
#https://youtu.be/2Bp-gO7TAFc?si=4F-ZE4OSCJt25KG_

import pygame # type: ignore
import math
import random
import time
import sys

# CONSTANTS
WIDTH = 640
HEIGHT = 640
PIXELS = 32
SQUARES = int(WIDTH / PIXELS)
GAME_DURATION = 30 

# COLORS
BG1 = (255,255,224)
BG2 = (255 ,250, 205)
RED = (255, 0, 0)
BLUE = (0, 0, 50)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self, head_image):
        self.head_image = pygame.image.load(head_image)
        self.head_image = pygame.transform.scale(self.head_image, (PIXELS, PIXELS))
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.body_color = 50
        self.state = "STOP"  

    def move_head(self):
        if self.state == "UP":
            self.headY -= PIXELS
        elif self.state == "DOWN":
            self.headY += PIXELS
        elif self.state == "RIGHT":
            self.headX += PIXELS
        elif self.state == "LEFT":
            self.headX -= PIXELS

    def move_body(self):
        if len(self.bodies) > 0:
            for i in range(len(self.bodies) - 1, -1, -1):
                if i == 0:
                    self.bodies[0].posX = self.headX
                    self.bodies[0].posY = self.headY
                else:
                    self.bodies[i].posX = self.bodies[i - 1].posX
                    self.bodies[i].posY = self.bodies[i - 1].posY

    def add_body(self):
        self.body_color += 10
        body = Body((0, 0, self.body_color), self.headX, self.headY)
        self.bodies.append(body)

    def delete_body(self):
        if len(self.bodies) > 0:
            del self.bodies[-1] 

    def draw(self, surface):
        surface.blit(self.head_image, (self.headX, self.headY))
        if len(self.bodies) > 0:
            for body in self.bodies:
                body.draw(surface)

    def die(self):
        self.headX = random.randrange(0, WIDTH, PIXELS)
        self.headY = random.randrange(0, HEIGHT, PIXELS)
        self.bodies = []
        self.body_color = 50
        self.state = "STOP"

class Body:
    def __init__(self, color, posX, posY):
        self.color = color
        self.posX = posX
        self.posY = posY

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.posX, self.posY, PIXELS, PIXELS))

class Apple:
    def __init__(self):
        self.apple_image = pygame.image.load("apple.png")
        self.apple_image = pygame.transform.scale(self.apple_image, (32, 32))
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)

    def draw(self, surface):
        surface.blit(self.apple_image, (self.posX, self.posY))

class Punish:
    def __init__(self):
        self.punish_image = pygame.image.load("1AzaltanElma.png")
        self.punish_image = pygame.transform.scale(self.punish_image, (32, 32))
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)  
        self.posY = random.randrange(0, HEIGHT, PIXELS)  

    def draw(self, surface):
        surface.blit(self.punish_image, (self.posX, self.posY))

class Obstacle:
    def __init__(self):
        self.obstacle_image = pygame.image.load("olduren.png")
        self.obstacle_image = pygame.transform.scale(self.obstacle_image, (32, 32))
        self.visible = False 
        self.spawn_timer = 0  
        self.spawn_interval = random.randint(5, 15)  
        self.visible_time = 25  
        self.spawn()

    def spawn(self):
        self.posX = random.randrange(0, WIDTH, PIXELS)
        self.posY = random.randrange(0, HEIGHT, PIXELS)
        self.visible = True 
        self.spawn_timer = 0 

    def draw(self, surface):
        if self.visible:
            surface.blit(self.obstacle_image, (self.posX, self.posY))

    def update(self):
        if not self.visible:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn()
        else:
            self.spawn_timer += 1
            if self.spawn_timer >= self.visible_time:
                self.visible = False
                self.spawn_timer = 0 
                self.spawn_interval = random.randint(5, 15)  
                self.visible_time = 25 

class Background:
    def draw(self, surface):
        surface.fill(BG1)
        counter = 0
        for row in range(SQUARES):
            for col in range(SQUARES):
                if counter % 2 == 0:
                    pygame.draw.rect(surface, BG2, (col * PIXELS, row * PIXELS, PIXELS, PIXELS))
                if col != SQUARES - 1:
                    counter += 1

class Collision:
    def between_snake_and_apple(self, snake, apple):
        distance = math.sqrt(math.pow((snake.headX - apple.posX), 2) + math.pow((snake.headY - apple.posY), 2))
        return distance < PIXELS

    def between_snake_and_punish(self, snake, punish):
        distance = math.sqrt(math.pow((snake.headX - punish.posX), 2) + math.pow((snake.headY - punish.posY), 2))
        return distance < PIXELS

    def between_snake_and_obstacle(self, snake, obstacle):
        distance = math.sqrt(math.pow((snake.headX - obstacle.posX), 2) + math.pow((snake.headY - obstacle.posY), 2))
        if distance < PIXELS:
            return True
        return False

    def between_snake_and_walls(self, snake):
        if snake.headX < 0 or snake.headX > WIDTH - PIXELS or snake.headY < 0 or snake.headY > HEIGHT - PIXELS:
            return True
        return False

    def between_head_and_body(self, snake):
        for body in snake.bodies:
            distance = math.sqrt(math.pow((snake.headX - body.posX), 2) + math.pow((snake.headY - body.posY), 2))
            if distance < PIXELS:
                return True
        return False

class Score:
    def __init__(self):
        self.points = 0
        self.font = pygame.font.SysFont('monospace', 30, bold=False)
        self.start_time = time.time()

    def increase(self):
        self.points += 10

    def decrease(self):
        self.points -= 2

    def reset(self):
        self.points = 0
        self.start_time = time.time()

    def show(self, surface):
        elapsed_time = time.time() - self.start_time
        lbl_score = self.font.render('Score: ' + str(self.points), 1, BLACK)
        lbl_time = self.font.render('Time: ' + str(int(GAME_DURATION - elapsed_time)), 1, BLACK)
        surface.blit(lbl_score, (5, 5))
        surface.blit(lbl_time, (5, 40))

def start_screen(screen):
    font = pygame.font.SysFont('monospace', 50, bold=True)
    start_text = font.render('Start Game', True, (0,0,0))
    start_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill(BG1)
    screen.blit(start_text, start_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    return
                               
def select_snake_head(screen):
    font = pygame.font.SysFont('monospace', 40, bold=True)
    select_text = font.render('Select Snake Head', True, (0,0,0))
    select_rect = select_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    
    head_image_size = PIXELS * 3
    margin = 20  

 
    head1_image = pygame.image.load("blue.jpg")
    head1_image = pygame.transform.scale(head1_image, (head_image_size, head_image_size))
    head1_rect = head1_image.get_rect(center=(WIDTH // 2 - head_image_size - margin // 2, HEIGHT // 2))

    head2_image = pygame.image.load("pink.jpg")
    head2_image = pygame.transform.scale(head2_image, (head_image_size, head_image_size))
    head2_rect = head2_image.get_rect(center=(WIDTH // 2 + head_image_size + margin // 2, HEIGHT // 2))

    head3_image = pygame.image.load("green.jpg")
    head3_image = pygame.transform.scale(head3_image, (head_image_size, head_image_size))
    head3_rect = head3_image.get_rect(center=(WIDTH // 2 - head_image_size - margin // 2, HEIGHT // 2 + head_image_size + margin))

    head4_image = pygame.image.load("yellow.jpg")
    head4_image = pygame.transform.scale(head4_image, (head_image_size, head_image_size))
    head4_rect = head4_image.get_rect(center=(WIDTH // 2 + head_image_size + margin // 2, HEIGHT // 2 + head_image_size + margin))


    screen.fill(BG1)
    screen.blit(select_text, select_rect)
    screen.blit(head1_image, head1_rect)
    screen.blit(head2_image, head2_rect)
    screen.blit(head3_image, head3_rect)
    screen.blit(head4_image, head4_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if head1_rect.collidepoint(mouse_pos):
                    return "blue.jpg"
                elif head2_rect.collidepoint(mouse_pos):
                    return "pink.jpg"
                elif head3_rect.collidepoint(mouse_pos):
                    return "green.jpg"
                elif head4_rect.collidepoint(mouse_pos):
                    return "yellow.jpg"

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SNAKE")

    start_screen(screen) 

    chosen_head_image = select_snake_head(screen) 

    font = pygame.font.SysFont('monospace', 50, bold=True)

    snake = Snake(chosen_head_image)
    apple = Apple()
    punish = Punish()
    background = Background()
    collision = Collision()
    score = Score()
    obstacle = Obstacle()

    running = True
    while running:
        background.draw(screen)
        snake.draw(screen)
        apple.draw(screen)
        score.show(screen)
        punish.draw(screen)
        obstacle.draw(screen)
        obstacle.update() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if snake.state != "DOWN":
                        snake.state = "UP"

                if event.key == pygame.K_DOWN:
                    if snake.state != "UP":
                        snake.state = "DOWN"

                if event.key == pygame.K_RIGHT:
                    if snake.state != "LEFT":
                        snake.state = "RIGHT"

                if event.key == pygame.K_LEFT:
                    if snake.state != "RIGHT":
                        snake.state = "LEFT"

                if event.key == pygame.K_p:
                    snake.state = "STOP"

        if collision.between_snake_and_apple(snake, apple):
            apple.spawn()
            snake.add_body()
            score.increase()

        if collision.between_snake_and_punish(snake, punish):
            punish.spawn()
            snake.delete_body()
            score.decrease()

        if snake.state != "STOP":
            snake.move_body()
            snake.move_head()

        if collision.between_snake_and_walls(snake) or collision.between_head_and_body(snake) or collision.between_snake_and_obstacle(snake, obstacle):
            score.reset()
            game_over_text = font.render('Game Over! You lost.', 1, BLACK)
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.update()
            pygame.time.delay(2000) 
            running = False

        elapsed_time = time.time() - score.start_time 
        if elapsed_time >= GAME_DURATION and score.points < 30:
            game_over_text = font.render('Game Over! You lost.', 1, BLACK)
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.update()
            pygame.time.delay(2000)  
            running = False

        
        if elapsed_time >= GAME_DURATION and score.points >= 30:
            win_text = font.render('You Win!', 1, BLACK)
            screen.blit(win_text, win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
            pygame.display.update()
            pygame.time.delay(2000)  
            running = False

        pygame.time.delay(150)
        pygame.display.update()

    
    restart_text = font.render('Restart', True, (255, 255, 255), BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))
    screen.blit(restart_text, restart_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse_pos):
                    main()

        pygame.time.delay(100)

main()
