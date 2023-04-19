import pygame
from pygame.math import Vector2
import sys
import random



pygame.init()
window = pygame.display.set_mode((700, 400))
pygame.display.set_caption("Snake Game")
snake_speed = 150


bg_image = pygame.image.load("bg\\background.jpg")
start_button_image1 = pygame.image.load("buttons\\start_button.jpg")
start_button_image = pygame.transform.scale(start_button_image1,(50,50))
quit_button_image1 = pygame.image.load("buttons\\quit_button.jpg")
quit_button_image = pygame.transform.scale(quit_button_image1, (50,50))

# Create button rects
start_button_rect = pygame.Rect(290, 175, start_button_image.get_width(), start_button_image.get_height())
quit_button_rect = pygame.Rect(395, 175, quit_button_image.get_width(), quit_button_image.get_height())

# Loop to display the menu
menu_running = True
while menu_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on a button
            if start_button_rect.collidepoint(event.pos):
                # Transition to the game screen
                menu_running = False
            elif quit_button_rect.collidepoint(event.pos):
                # Quit the game
                menu_running = False
                pygame.quit()

    # Draw the menu
    window.blit(bg_image, (0, 0))

    # Draw the buttons
    window.blit(start_button_image, start_button_rect)
    window.blit(quit_button_image, quit_button_rect)

    # Update the display
    pygame.display.flip()



class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.tail = False


        self.head_up = pygame.image.load("snake\\head_up.png").convert_alpha()
        self.head_down = pygame.image.load("snake\\head_down.png").convert_alpha()
        self.head_right = pygame.image.load("snake\\head_right.png").convert_alpha()
        self.head_left = pygame.image.load("snake\\head_left.png").convert_alpha()

        self.leftdown = pygame.image.load("snake\\leftdown.png").convert_alpha()
        self.downright = pygame.image.load("snake\\downright.png").convert_alpha()
        self.rightup = pygame.image.load("snake\\rightup.png").convert_alpha()
        self.upleft = pygame.image.load("snake\\upleft.png").convert_alpha()

        self.tailright = pygame.image.load("snake\\tailright.png").convert_alpha()
        self.taildown = pygame.image.load("snake\\taildown.png").convert_alpha()
        self.tailup = pygame.image.load("snake\\tailup.png").convert_alpha()
        self.tailleft = pygame.image.load("snake\\tailleft.png").convert_alpha()

        self.benddown = pygame.image.load("snake\\benddown.png").convert_alpha()
        self.bendL = pygame.image.load("snake\\bendL.png").convert_alpha()
        self.bendR = pygame.image.load("snake\\bendR.png").convert_alpha()
        self.bendup = pygame.image.load("snake\\bendup.png").convert_alpha()

    def draw_snake(self):
        self.graphics_update_head()

        for index, block in enumerate(self.body):
            xpos = int(block.x * cellsize)
            ypos = int(block.y * cellsize)
            block__rect = pygame.Rect(xpos, ypos, cellsize, cellsize)
            if index == 0:
                screen.blit(self.head, block__rect)
            else:
                pygame.draw.rect(screen, (150, 100, 150), block__rect)

    def graphics_update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def move_snake(self):

        if self.tail == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.tail = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def addbl(self):
        self.tail = True




class Fruit:
    def __init__(self):
        self.randoms()


    def drawfruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cellsize), int(self.pos.y * cellsize), cellsize, cellsize)
        screen.blit(goodapple, fruit_rect)

    def randoms(self):
        self.x = random.randint(0, cellnum - 1)
        self.y = random.randint(0, cellnum - 1)
        self.pos = Vector2(self.x, self.y)


class BoostFruit:
    def __init__(self):
        self.randoms()

    def drawfruit(self):
        boostfruitrect = pygame.Rect(int(self.pos.x * cellsize), int(self.pos.y * cellsize), cellsize, cellsize)
        screen.blit(chilli, boostfruitrect)

    def randoms(self):
        self.x = random.randint(0, cellnum - 1)
        self.y = random.randint(0, cellnum - 1)
        self.pos = Vector2(self.x, self.y)




class MAIN:
    def __init__(self):
        self.fruit = Fruit()
        self.bfruit = BoostFruit()
        self.body = Snake()
        self.increasespeed()


    def update(self):
        self.body.move_snake()
        self.collision()
        self.lose()

    def increasespeed(self):

        self.speed = snake_speed + 50

    def draw(self):
        self.drawgrass()
        self.bfruit.drawfruit()
        self.fruit.drawfruit()
        self.body.draw_snake()
        self.drawscore()

    def collision(self):
        if self.fruit.pos == self.body.body[0]:
            self.fruit.randoms()
            self.body.addbl()
        if self.bfruit.pos == self.body.body[0]:
            self.bfruit.randoms()
            self.body.addbl()
            self.increasespeed()


    def lose(self):
        if not 0 <= self.body.body[0].x < cellnum or not 0 <= self.body.body[0].y < cellnum:
            self.gameover()
        for block in self.body.body[1:]:
            if block == self.body.body[0]:
                self.gameover()

    def gameover(self):
        pygame.quit()
        sys.exit()

    def drawscore(self):
        score = str(len(self.body.body) - 3)
        scr_surface = score_font.render(score, True, (0, 0, 0))
        scorex = (cellnum * cellsize) - 60
        scorey = (cellnum * cellsize) - 40
        score_rect = scr_surface.get_rect(center=(scorex, scorey))
        screen.blit(scr_surface, score_rect)

    def drawgrass(self):
        grass_color = (136, 204, 0)
        for row in range(cellnum):
            if row % 2 == 0:
                for col in range(cellnum):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cellsize, row * cellsize, cellsize, cellsize)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cellnum):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cellsize, row * cellsize, cellsize, cellsize)
                        pygame.draw.rect(screen, grass_color, grass_rect)


pygame.init()
cellsize = 30
cellnum = 20
screen = pygame.display.set_mode((cellsize * cellnum, cellsize * cellnum))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, snake_speed)
pygame.display.set_caption('Snak gem')
score_font = pygame.font.Font("Font/phantomstorm.ttf", 25)

maing = MAIN()
apple = pygame.image.load("apple/apple4.png")
headup = pygame.image.load("snake/head_up.png")
goodapple = pygame.transform.scale(apple, (30, 30))
hedup1 = pygame.transform.scale(headup, (30, 30))
chilli1 = pygame.image.load("apple\\Chillie.png")
chilli = pygame.transform.scale(chilli1,(30,30))

# Loop to run the game


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            maing.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if maing.body.direction.y != 1:
                    maing.body.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if maing.body.direction.y != -1:
                    maing.body.direction = Vector2(0, +1)
            if event.key == pygame.K_LEFT:
                if maing.body.direction.x != 1:
                    maing.body.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT:
                if maing.body.direction.x != -1:
                    maing.body.direction = Vector2(+1, 0)

    screen.fill((153, 230, 0))
    maing.draw()
    pygame.display.update()
    clock.tick(120)