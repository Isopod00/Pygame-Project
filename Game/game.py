## Import the necessary modules for this project :)
import pygame, sys, random, time, pickle, math
from pygame.locals import *

## Define some common colors for future use
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)
orange = (255, 123, 25)
yellow = (255, 255, 0)
purple = (128,0,128)
pink = (250, 213, 229)
brown = (139, 69, 19)

## Game Configuration Settings (Important)
WINDOW_WIDTH = 1024 ## Width of the screen in pixels
WINDOW_HEIGHT = 640 ## Height of the screen in pixels
FPS = 60 ## How many Frames Per Second to render

## Set the initial size of the character and enemt
characterSize = 40
enemySize = 40
## Set the initial score
score = 0
## The enemy starts alive
enemyDead = False

## Initialize the pygame module!
pygame.init()

## Instantiate the game clock object
fpsClock = pygame.time.Clock()
 
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) ## Define the size of the game window
pygame.display.set_caption('Anthony\'s Amazing Game!') ## Set the title of the game window

## Save an object to a local file using the pickle module
def save_object(object):
  with open("data.pickle", "wb") as f:
    pickle.dump(object, f, protocol=pickle.HIGHEST_PROTOCOL)
## Load a locally saved object using the pickle module
def load_object(filename):
  with open(filename, "rb") as f:
    return pickle.load(f)

## Load the highscore from the pickle file
highscore = load_object("data.pickle")

## Method for displaying the score
def show_score(color, font, size):
   
  ## Create the font object 'score_font'
  score_font = pygame.font.SysFont(font, size)
  ## Create the display surface object 'score_surface'
  score_surface = score_font.render(f'Score : {score}', True, color)
  ## Create a rectangular object for the text surface
  score_rect = score_surface.get_rect()
  ## Set the position of the text
  score_rect.topleft = (10, 5)
    
  ## Use 'blit' to draw the text on screen
  WINDOW.blit(score_surface, score_rect)

## Method for displaying the highscore
def show_high_score(color, font, size):
   
  ## Create the font object 'score_font'
  score_font = pygame.font.SysFont(font, size)
  ## Create the display surface object 'score_surface'
  score_surface = score_font.render(f'Highscore : {highscore}', True, color)
  ## Create a rectangular object for the text surface
  score_rect = score_surface.get_rect()
  ## Set the position of the text
  score_rect.topright = (WINDOW_WIDTH-10, 5)
    
  ## Use 'blit' to draw the text on screen
  WINDOW.blit(score_surface, score_rect)

## Show the current size of the character
def show_character_size(color, font, size):

  ## Create the font object 'size_font'
  size_font = pygame.font.SysFont(font, size)
  ## Create the display surface object 'size_surface'
  size_surface = size_font.render(f'{characterSize}', True, color)
  ## Create a rectangular object for the text surface
  size_rect = size_surface.get_rect()
  ## Set the position of the text
  size_rect.center = (characterX + characterSize/2, characterY + characterSize/2)

  ## Use 'blit' to draw the text on screen
  WINDOW.blit(size_surface, size_rect)

## Show the current size of the enemy
def show_enemy_size(color, font, size):

  ## Create the font object 'size_font'
  size_font = pygame.font.SysFont(font, size)
  ## Create the display surface object 'size_surface'
  size_surface = size_font.render(f'{enemySize}', True, color)
  ## Create a rectangular object for the text surface
  size_rect = size_surface.get_rect()
  ## Set the position of the text
  size_rect.center = (enemyX + enemySize/2, enemyY + enemySize/2)

  ## Use 'blit' to draw the text on screen
  WINDOW.blit(size_surface, size_rect)

## Game Over method
def game_over():

  ## Save the new highscore (if applicable) to the pickle file
  if(score > highscore):
    save_object(score)

  ## Create the font object 'my_font'
  my_font = pygame.font.SysFont('comicsansms', 50)
  ## Create a text surface on which text can be drawn
  game_over_surface = my_font.render(f'Your Final Score is : {score}', True, white)
  ## Create a rectangular object for the text surface
  game_over_rect = game_over_surface.get_rect()
  ## Set the position of the text
  game_over_rect.midtop = (WINDOW_WIDTH/2, WINDOW_HEIGHT/4)
    
  ## Use 'blit' to draw the text on screen
  WINDOW.blit(game_over_surface, game_over_rect)
  pygame.display.flip()
    
  ## Wait for 2 seconds before quitting the program
  time.sleep(2)
  ## Deactivate the pygame module
  pygame.quit()
  ## Quit the program
  sys.exit()

## Distance Formula method
def distance(x1,x2,y1,y2):
    return (math.sqrt((x2-x1)**2) + (math.sqrt((y2-y1)**2)))

## HERE IS THE MAIN CODE THAT CONTROLS THE GAME ##
looping = True

## Set the initial x and y position of the character
characterX = 100
characterY = 100
## Set the initial x and y position of the enemy
enemyX = WINDOW_WIDTH - 100
enemyY = WINDOW_HEIGHT - 100
## Set the initial x and y position of the food
foodX = WINDOW_WIDTH / 2
foodY = WINDOW_HEIGHT / 2
food2X = WINDOW_WIDTH / 2
food2Y = WINDOW_HEIGHT / 2

characterSpeed = 5 ## Change this to change the speed of the character
enemySpeed = 2 ## Change this to change the speed of the enemy

## The main game loop
while looping :
  
  ## Quit the application by running the game_over() method
  for event in pygame.event.get() :
    if event.type == QUIT :
      game_over()

  ## Move the character's position when W,A,S,D (or arrow keys) are pressed
  pressed = pygame.key.get_pressed()
  if (pressed[K_RIGHT] or pressed[K_d]) :
    characterX = characterX + characterSpeed
  if (pressed[K_LEFT] or pressed[K_a]) :
    characterX = characterX - characterSpeed
  if (pressed[K_DOWN] or pressed[K_s]) :
    characterY = characterY + characterSpeed
  if (pressed[K_UP] or pressed[K_w]) :
    characterY = characterY - characterSpeed

  ## Make the character pop out of the other side if it runs into the edge
  if (characterY + characterSize > WINDOW_HEIGHT):
    characterY = 0
  elif (characterY < 0):
    characterY = WINDOW_HEIGHT - characterSize
  if (characterX + characterSize > WINDOW_WIDTH):
    characterX = 0
  elif (characterX < 0):
    characterX = WINDOW_WIDTH - characterSize

  ## Make the enemy move it's position towards the nearest food
  if(enemySize < characterSize*2):
    if(not enemyDead and distance(enemyX + enemySize/2, foodX, enemyY + enemySize/2, foodY) < distance(enemyX + enemySize/2, food2X, enemyY + enemySize/2, food2Y)):
      if(enemyX + enemySize/2 < foodX):
        enemyX += enemySpeed
      elif(enemyX + enemySize/2 > foodX):
        enemyX -= enemySpeed
      if(enemyY + enemySize/2 < foodY):
        enemyY += enemySpeed
      elif(enemyY + enemySize/2 > foodY):
        enemyY -= enemySpeed  
    elif(not enemyDead):
      if(enemyX + enemySize/2 < food2X):
        enemyX += enemySpeed
      elif(enemyX + enemySize/2 > food2X):
        enemyX -= enemySpeed
      if(enemyY + enemySize/2 < food2Y):
        enemyY += enemySpeed
      elif(enemyY + enemySize/2 > food2Y):
        enemyY -= enemySpeed  
  else: ## If the enemy is big enough, seek out the player to eat them
    if(enemyX + enemySize/2 < characterX + characterSize/2):
        enemyX += enemySpeed
    elif(enemyX + enemySize/2 > characterX + characterSize/2):
        enemyX -= enemySpeed
    if(enemyY + enemySize/2 < characterY + characterSize/2):
        enemyY += enemySpeed
    elif(enemyY + enemySize/2 > characterY + characterSize/2):
        enemyY -= enemySpeed  

  ## If the character eats the food, increase the score and the size of the character
  if (abs((characterX + (characterSize/2)) - (foodX + (5/2))) <= characterSize/2 and abs((characterY + (characterSize/2)) - (foodY + 5/2)) <= characterSize/2):
    characterSize += 4
    ## Randomize the new position of the food
    foodX = random.randint(10, WINDOW_WIDTH - 10)
    foodY = random.randint(10, WINDOW_HEIGHT - 10)
  if (abs((characterX + (characterSize/2)) - (food2X + (5/2))) <= characterSize/2 and abs((characterY + (characterSize/2)) - (food2Y + 5/2)) <= characterSize/2):
    characterSize += 4
    ## Randomize the new position of the food
    food2X = random.randint(10, WINDOW_WIDTH - 10)
    food2Y = random.randint(10, WINDOW_HEIGHT - 10)
  ## If the enemy eats the food, increase the score and the size of the character
  if (not enemyDead and abs((enemyX + (enemySize/2)) - (foodX + (5/2))) <= enemySize/2 and abs((enemyY + (enemySize/2)) - (foodY + 5/2)) <= enemySize/2):
    enemySize += 4
    ## Randomize the new position of the food
    foodX = random.randint(10, WINDOW_WIDTH - 10)
    foodY = random.randint(10, WINDOW_HEIGHT - 10)
  if (not enemyDead and abs((enemyX + (enemySize/2)) - (food2X + (5/2))) <= enemySize/2 and abs((enemyY + (enemySize/2)) - (food2Y + 5/2)) <= enemySize/2):
    enemySize += 4
    ## Randomize the new position of the food
    food2X = random.randint(10, WINDOW_WIDTH - 10)
    food2Y = random.randint(10, WINDOW_HEIGHT - 10)

  ## EAT EAT EAT EAT EAT EAT EAT 
  if(characterSize >= enemySize*2):
    if(not enemyDead and distance(characterX + characterSize/2, enemyX + enemySize/2, characterY + characterSize/2, enemyY + enemySize/2) < characterSize/2):
      enemyDead = True
      characterSize += enemySize
  elif(not enemyDead and enemySize >= characterSize*2):
    if(distance(characterX + characterSize/2, enemyX + enemySize/2, characterY + characterSize/2, enemyY + enemySize/2) < enemySize/2):
      game_over()

  character = pygame.Rect(characterX, characterY, characterSize, characterSize) ## Define the character's current position & size
  food = pygame.Rect(foodX, foodY, 10, 10) ## Define the food's current position & size
  food2 = pygame.Rect(food2X, food2Y, 10, 10) ## Define the food's current position & size

  ## Render images to the screen here ##
  WINDOW.fill(blue) ## Fill the background with a specified color
  pygame.draw.rect(WINDOW, green, food) ## Render the food to the screen
  pygame.draw.rect(WINDOW, green, food2) ## Render the food to the screen
  pygame.draw.rect(WINDOW, purple, character) ## Render the character to the screen

  ## Only render the enemy if it hasn't been killed
  if (not enemyDead):
    enemy = pygame.Rect(enemyX, enemyY, enemySize, enemySize) ## Define the enemy's current position & size
    pygame.draw.rect(WINDOW, red, enemy) ## Render the enemy to the screen
    show_enemy_size(white, 'comicsansms', 20) ## Display the current enemy size

  score = characterSize - 40 ## Update the current score (40 is the initial size, so we subtract that)

  ## Display the current score
  show_score(white, 'comicsansms', 20)
  ## Display the current highscore
  show_high_score(white, 'comicsansms', 20)
  ## Display the current character size
  show_character_size(white, 'comicsansms', 20)

  pygame.display.flip() ## Update the screen
  fpsClock.tick(FPS) ## Tick the game clock forward