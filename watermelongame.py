# Simple pygame program

import pygame # Import and initialize the pygame library
import random # Import random for random numbers
import serial # for connection with arduino

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define a Player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("watermelon.png"), (50, 50)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.last_analog = 0
        self.last_seed = "SEEDHIGH"
        self.last_reset = "RESETHIGH"

    def set_last_analog(self, analog):
        self.last_analog = analog
    
    # Move the sprite based on user keypresses
    def update(self, analog_value):
        diff = analog_value - self.last_analog
        if analog_value > (self.last_analog + 50) or analog_value < (self.last_analog - 50):
            self.rect.move_ip(0, (diff/35)*5)
        self.last_analog = analog_value
        
        # Keep player on the screen
        # if self.rect.left < 0:
        #     self.rect.left = 0
        # if self.rect.right > SCREEN_WIDTH:
        #     self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the balloon object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'balloon'
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super(Balloon, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("balloon.png"), (50, 50)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(3, 7)
        self.buff = 0
        self.debuff = 0

        num = random.randint(1,100)
        if num > 90:
            self.buff = 30
        elif num < 10:
            self.debuff = -30

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Seed(pygame.sprite.Sprite):
    def __init__(self):
        super(Seed, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("seeds.png"), (10, 10)).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                player.rect.center[0] + 50,
                player.rect.center[1]
            )
        )
        self.speed = 5
    def update(self):
        self.rect.move_ip(self.speed,0)
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont('comicsansms', 32)

class Score():
    def __init__(self):
        self.score = 0
        self.text = font.render(str(self.score), True, (219, 33, 70), (255, 255, 255))
        self.textRec = self.text.get_rect()
        self.textRec.center = (SCREEN_WIDTH//2, 20)

    def update_score(self, point_type):
        buffs = ""
        if point_type == 1:
            self.score += 10
        elif point_type == -1:
            self.score -= 10
        elif point_type == 0:
            self.score = 0
        elif point_type == 30:
            self.score += 30
            buffs = "     BONUS +30"
        elif point_type == -30:
            self.score += -30
            buffs = "     DEBUFF -30"
        self.text = font.render(str(self.score) + buffs, True, (219, 33, 70), (255, 255, 255))
        return screen.blit(self.text, self.textRec)

# Create a custom event for adding a new balloon
ADDBALLOON = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBALLOON, 400)

ADDSEED = pygame.USEREVENT + 2

# Instantiate player and total
player = Player()
total = Score()

# Create groups to hold balloon sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
balloons = pygame.sprite.Group()
seeds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# EVENT HANDLER: Run until the user asks to quit
running = True
start = 0
while running:
    if start == 0:
        next_line = arduino.readline().decode()
        while (' ' in next_line) or ('SEED' in next_line) or ('RESET' in next_line):
            continue

        # include a print line for both SEEDHIGH and RESETHIGH
        print(arduino.readline().decode())
        print(arduino.readline().decode())
        # print("_-------")
        player.set_last_analog = int(arduino.readline().decode().strip())
        player.rect.top = (float(player.set_last_analog)/6540) * 600
        start = 1
        print("_-----")
    # for each event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
        
        # Did the user click the window close button?
        elif event.type == pygame.QUIT:
            running = False
            start = 0
        
        # Add a new balloon?
        elif event.type == ADDBALLOON:
            # Create the new balloon and add it to sprite groups
            new_balloon = Balloon()
            balloons.add(new_balloon)
            all_sprites.add(new_balloon)

    # Update the player sprite based on potentiometer
    data = arduino.readline().decode().strip()
    # print(data)
    if data == "RESETHIGH":
        continue
    elif data == "RESETLOW":
        for sprite in all_sprites:
            if sprite != player:
                sprite.kill()
        total.update_score(0)
    elif data == "SEEDHIGH":
        player.last_seed = "SEEDHIGH"
    elif data == "SEEDLOW":
        if player.last_seed != "SEEDLOW":
            new_seed = Seed()
            seeds.add(new_seed)
            all_sprites.add(new_seed)
            player.last_seed = "SEEDLOW"
    elif data != "":
        data = int(data)
        player.update(data)

    # Update seed position
    seeds.update()
    # Update balloon position
    balloons.update()

    # Fill the background with tan
    screen.fill((240, 215, 201))
    screen.blit(total.text, total.textRec)

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    # Check if any balloons have collided with the player
    collision = pygame.sprite.spritecollideany(player, balloons)
    if collision:
        if collision.debuff == -30:
            pygame.display.update(total.update_score(-30))
        else:
            pygame.display.update(total.update_score(-1))
        collision.kill()
    
    # Check if any seeds have collided with balloons
    for win in pygame.sprite.groupcollide(seeds, balloons, True, True):
        if win == 30:
            pygame.display.update(total.update_score(30))
        elif win == -30:
            pygame.display.update(total.update_score(-30))
        else:
            total.update_score(1)

    # Flip the display
    pygame.display.flip()

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(45)

# Done! Time to quit.
pygame.quit()