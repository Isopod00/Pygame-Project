# Import the necessary modules for this project :)
import pygame
import sys
import random
import time
import pickle
import math

from pygame.locals import *

# Define some common colors for future use
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)

# Game Configuration Settings (Important)
WINDOW_WIDTH = 1024  # Width of the screen in pixels
WINDOW_HEIGHT = 640  # Height of the screen in pixels
FPS = 60  # How many Frames Per Second to render

# Set the initial size of the character and enemy
characterSize = 40
enemySize = 40
# Set the initial score
score = 0
enemiesDefeated = 0
# The enemy starts alive :)
enemyDead = False

# Set the initial scale of the game
scale = 1
scaleIteration = 0

# Initialize the pygame module!
pygame.init()

# Instantiate the game clock object
fpsClock = pygame.time.Clock()
# Set the display mode and size
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption('Square Survival')  # Set the title of the game window
pygame_icon = pygame.image.load('Icon.png')  # Load the game icon
pygame.display.set_icon(pygame_icon)  # Set the game icon


# Save an object to a local file using the pickle module
def save_data(data):
    with open("data.pickle", "wb") as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


# Load a locally saved object using the pickle module
def load_object(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


# Load the highscore from the pickle file
highscore = load_object("data.pickle")


# Method for displaying text on the screen
def display_text(color, font, size, text, reference_point, position):
    # Create the font object
    font = pygame.font.SysFont(font, size)
    # Create the display surface object 'score_surface'
    surface = font.render(text, True, color)
    # Create a rectangular object for the text surface
    rect = surface.get_rect()

    # Set the position of the text
    if reference_point == 'center':
        rect.center = position
    elif reference_point == 'topright':
        rect.topright = position
    elif reference_point == 'topleft':
        rect.topleft = position

    # Use 'blit' to draw the text on screen
    WINDOW.blit(surface, rect)


# Show the current size of the character
def show_character_size(color, font, size):
    # Create the font object 'size_font'
    size_font = pygame.font.SysFont(font, size)
    # Create the display surface object 'size_surface'
    size_surface = size_font.render(f'{characterSize}', True, color)
    # Create a rectangular object for the text surface
    size_rect = size_surface.get_rect()
    # Set the position of the text
    size_rect.center = (characterX + scale * characterSize / 2, characterY + scale * characterSize / 2)

    # Use 'blit' to draw the text on screen
    WINDOW.blit(size_surface, size_rect)


# Show the current size of the enemy
def show_enemy_size(color, font, size):
    # Create the font object 'size_font'
    size_font = pygame.font.SysFont(font, size)
    # Create the display surface object 'size_surface'
    size_surface = size_font.render(f'{enemySize}', True, color)
    # Create a rectangular object for the text surface
    size_rect = size_surface.get_rect()
    # Set the position of the text
    size_rect.center = (enemyX + scale * enemySize / 2, enemyY + scale * enemySize / 2)

    # Use 'blit' to draw the text on screen
    WINDOW.blit(size_surface, size_rect)


# Game Over method
def game_over():
    # Save the new highscore (if applicable) to the pickle file
    if score > highscore:
        save_data(score)

    WINDOW.fill(blue)  # Fill the screen blue and display only the necessary info #
    display_text(white, 'comicsansms', 20, f'Score : {score}', 'topleft', (10, 5))
    display_text(white, 'comicsansms', 20, f'Highscore : {highscore}', 'topright', (WINDOW_WIDTH - 10, 5))
    display_text(white, 'comicsansms', 50, f'Your Final Score is : {score}', 'center',
                 (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))
    pygame.display.flip()

    # Wait for 2 seconds before quitting the program
    time.sleep(2)
    # Deactivate the pygame module
    pygame.quit()
    # Quit the program
    sys.exit()


# Distance Formula method
def distance(x1, x2, y1, y2):
    return math.sqrt((x2 - x1) ** 2) + (math.sqrt((y2 - y1) ** 2))


# Method for displaying the main menu
def main_menu():
    in_menu = True
    loop = 1
    max_loop = 50

    while in_menu:
        WINDOW.fill(blue)  # Fill the background with a specified color
        display_text(red, 'comicsansms', 40, 'Square Survival', 'center', (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))

        if loop < max_loop / 2:
            loop += 1
            display_text(white, 'comicsansms', 35, 'Press Enter/Return to Start!', 'center',
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        elif loop < max_loop:
            loop += 1
        else:
            loop = 1

        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                pygame.quit()
                quit()
            if action.type == pygame.KEYDOWN:
                if action.key == pygame.K_RETURN:
                    in_menu = False
        pygame.display.flip()  # Update the screen
        fpsClock.tick(FPS)  # Tick the game clock forward


# Method for pausing the game
def pause_game():
    paused = True
    loop = 1
    max_loop = 50

    while paused:
        WINDOW.fill(blue)  # Fill the background with a specified color

        if loop < max_loop / 2:
            loop += 1
            display_text(white, 'comicsansms', 35, 'Game Paused, Press Enter/Return to Continue', 'center',
                         (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        elif loop < max_loop:
            loop += 1
        else:
            loop = 1

        for action in pygame.event.get():
            if action.type == pygame.QUIT:
                game_over()
            if action.type == pygame.KEYDOWN:
                if action.key == pygame.K_RETURN:
                    paused = False
        pygame.display.flip()  # Update the screen
        fpsClock.tick(FPS)  # Tick the game clock forward


# HERE IS THE MAIN CODE THAT CONTROLS THE GAME #
main_menu()  # Start the game in the main menu
looping = True  # The game has begun!

# Set the initial x and y position of the character
characterX = 100
characterY = 100
# Set the initial x and y position of the enemy
enemyX = WINDOW_WIDTH - 100
enemyY = WINDOW_HEIGHT - 100
# Set the initial x and y position of the food
foodX = WINDOW_WIDTH / 2
foodY = WINDOW_HEIGHT / 2
food2X = WINDOW_WIDTH / 2
food2Y = WINDOW_HEIGHT / 2

characterSpeed = 5  # Change this to change the speed of the character

# The main game loop
while looping:

    enemySpeed = 1 + enemiesDefeated  # The speed of the enemy increases as the game progresses

    # Quit the application by running the game_over() method
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pause_game()

    # Move the character's position when W,A,S,D (or arrow keys) are pressed
    pressed = pygame.key.get_pressed()
    if pressed[K_RIGHT] or pressed[K_d]:
        characterX = characterX + characterSpeed
    if pressed[K_LEFT] or pressed[K_a]:
        characterX = characterX - characterSpeed
    if pressed[K_DOWN] or pressed[K_s]:
        characterY = characterY + characterSpeed
    if pressed[K_UP] or pressed[K_w]:
        characterY = characterY - characterSpeed

    # Make the character pop out of the other side if it runs into the edge
    if characterY + scale * characterSize > WINDOW_HEIGHT:
        characterY = 0
    elif characterY < 0:
        characterY = WINDOW_HEIGHT - scale * characterSize
    if characterX + scale * characterSize > WINDOW_WIDTH:
        characterX = 0
    elif characterX < 0:
        characterX = WINDOW_WIDTH - scale * characterSize

    # Make the enemy move it's position towards the nearest food
    if enemySize < characterSize * 2:
        if (not enemyDead and distance(enemyX + scale * enemySize / 2, foodX, enemyY + scale * enemySize / 2,
                                       foodY) < distance(enemyX + scale * enemySize / 2, food2X,
                                                         enemyY + scale * enemySize / 2, food2Y)):
            if (enemyX + scale * enemySize / 2 - foodX) < -2:
                enemyX += enemySpeed
            elif (enemyX + scale * enemySize / 2 - foodX) > 2:
                enemyX -= enemySpeed
            if (enemyY + scale * enemySize / 2 - foodY) < -2:
                enemyY += enemySpeed
            elif (enemyY + scale * enemySize / 2 - foodY) > 2:
                enemyY -= enemySpeed
        elif not enemyDead:
            if (enemyX + scale * enemySize / 2 - food2X) < -2:
                enemyX += enemySpeed
            elif (enemyX + scale * enemySize / 2 - food2X) > 2:
                enemyX -= enemySpeed
            if (enemyY + scale * enemySize / 2 - food2Y) < -2:
                enemyY += enemySpeed
            elif (enemyY + scale * enemySize / 2 - food2Y) > 2:
                enemyY -= enemySpeed
    else:  # If the enemy is big enough, seek out the player to eat them
        if enemyX + scale * enemySize / 2 < characterX + scale * characterSize / 2:
            enemyX += enemySpeed
        elif enemyX + scale * enemySize / 2 > characterX + scale * characterSize / 2:
            enemyX -= enemySpeed
        if enemyY + scale * enemySize / 2 < characterY + scale * characterSize / 2:
            enemyY += enemySpeed
        elif enemyY + scale * enemySize / 2 > characterY + scale * characterSize / 2:
            enemyY -= enemySpeed

            # If the character eats the food, increase the score and the size of the character
    if (abs((characterX + (scale * characterSize / 2)) - (foodX + (5 / 2))) <= scale * characterSize / 2 and abs(
            (characterY + (scale * characterSize / 2)) - (foodY + 5 / 2)) <= scale * characterSize / 2):
        characterSize += int(4 * (1 / scale))
        # Randomize the new position of the food
        foodX = random.randint(10, WINDOW_WIDTH - 10)
        foodY = random.randint(10, WINDOW_HEIGHT - 10)
    if (abs((characterX + (scale * characterSize / 2)) - (food2X + (5 / 2))) <= scale * characterSize / 2 and abs(
            (characterY + (scale * characterSize / 2)) - (food2Y + 5 / 2)) <= scale * characterSize / 2):
        characterSize += int(4 * (1 / scale))
        # Randomize the new position of the food
        food2X = random.randint(10, WINDOW_WIDTH - 10)
        food2Y = random.randint(10, WINDOW_HEIGHT - 10)
    # If the enemy eats the food, increase the score and the size of the character
    if (not enemyDead and abs((enemyX + (scale * enemySize / 2)) - (foodX + (5 / 2))) <= scale * enemySize / 2 and abs(
            (enemyY + (scale * enemySize / 2)) - (foodY + 5 / 2)) <= scale * enemySize / 2):
        enemySize += int(4 * (1 / scale))
        # Randomize the new position of the food
        foodX = random.randint(10, WINDOW_WIDTH - 10)
        foodY = random.randint(10, WINDOW_HEIGHT - 10)
    if (not enemyDead and abs((enemyX + (scale * enemySize / 2)) - (food2X + (5 / 2))) <= scale * enemySize / 2 and abs(
            (enemyY + (scale * enemySize / 2)) - (food2Y + 5 / 2)) <= scale * enemySize / 2):
        enemySize += int(4 * (1 / scale))
        # Randomize the new position of the food
        food2X = random.randint(10, WINDOW_WIDTH - 10)
        food2Y = random.randint(10, WINDOW_HEIGHT - 10)

    # EAT
    if characterSize >= enemySize * 2:
        if (not enemyDead and distance(characterX + scale * characterSize / 2, enemyX + scale * enemySize / 2,
                                       characterY + scale * characterSize / 2,
                                       enemyY + scale * enemySize / 2) < scale * characterSize / 2):
            enemyDead = True
            enemiesDefeated += 1
            characterSize += enemySize
    elif not enemyDead and enemySize >= characterSize * 2:
        if (distance(characterX + scale * characterSize / 2, enemyX + scale * enemySize / 2,
                     characterY + scale * characterSize / 2, enemyY + scale * enemySize / 2) < scale * enemySize / 2):
            game_over()

    # There is a chance for the enemy to spawn again after it dies
    if enemyDead and random.randint(1, 120) == 120:
        enemyDead = False
        enemySize = characterSize + random.randint(0, int(10 * (1 / scale)))
        enemyX = random.randint(0, WINDOW_WIDTH) - scale * enemySize / 2
        enemyY = random.randint(0, WINDOW_HEIGHT) - scale * enemySize / 2

    if characterSize >= 400 * 2 ** scaleIteration:
        scale /= 2
        scaleIteration += 1

    character = pygame.Rect(characterX, characterY, characterSize * scale,
                            characterSize * scale)  # Define the character's current position & size
    food = pygame.Rect(foodX, foodY, 10, 10)  # Define the food's current position & size
    food2 = pygame.Rect(food2X, food2Y, 10, 10)  # Define the food's current position & size

    # Render images to the screen here #
    WINDOW.fill(blue)  # Fill the background with a specified color
    pygame.draw.rect(WINDOW, green, food)  # Render the food to the screen
    pygame.draw.rect(WINDOW, green, food2)  # Render the food to the screen

    # Change the order in which they are rendered depending on which is currently bigger
    if characterSize < enemySize:
        pygame.draw.rect(WINDOW, purple, character)  # Render the character to the screen
        show_character_size(white, 'comicsansms', 20)  # Display the current character size
        # Only render the enemy if it hasn't been killed
        if not enemyDead:
            enemy = pygame.Rect(enemyX, enemyY, enemySize * scale,
                                enemySize * scale)  # Define the enemy's current position & size
            pygame.draw.rect(WINDOW, red, enemy)  # Render the enemy to the screen
            show_enemy_size(white, 'comicsansms', 20)  # Display the current enemy size
    else:
        # Only render the enemy if it hasn't been killed
        if not enemyDead:
            enemy = pygame.Rect(enemyX, enemyY, enemySize * scale,
                                enemySize * scale)  # Define the enemy's current position & size
            pygame.draw.rect(WINDOW, red, enemy)  # Render the enemy to the screen
            show_enemy_size(white, 'comicsansms', 20)  # Display the current enemy size
        pygame.draw.rect(WINDOW, purple, character)  # Render the character to the screen
        show_character_size(white, 'comicsansms', 20)  # Display the current character size

    # Update the current score (40 is the initial size, so we subtract that)
    score = characterSize - 40
    # Display the current score
    display_text(white, 'comicsansms', 20, f'Score : {score}', 'topleft', (10, 5))
    # Display the current highscore
    display_text(white, 'comicsansms', 20, f'Highscore : {highscore}', 'topright', (WINDOW_WIDTH - 10, 5))
    # Display the current # of enemies defeated
    display_text(white, 'comicsansms', 20, f'Enemies Defeated : {enemiesDefeated}', 'center', (WINDOW_WIDTH / 2, 20))

    pygame.display.flip()  # Update the screen
    fpsClock.tick(FPS)  # Tick the game clock forward
