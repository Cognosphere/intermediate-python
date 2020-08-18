import pygame, sys, time, random

# Game Over
def gameOver():
    text = pygame.font.SysFont('times new roman', 90)
    gameOverSurface = text.render('GAME OVER!', True, red)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (frameSizeX/2, frameSizeY/4)
    gameWindow.fill(black)
    gameWindow.blit(gameOverSurface, gameOverRect)
    showScore(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def showScore(choice, color, font, size):
    scoreFont = pygame.font.SysFont(font, size)
    scoreSurface = scoreFont.render('Score : ' + str(score), True, color)
    scoreRect = scoreSurface.get_rect()
    if choice == 1:
        scoreRect.midtop = (frameSizeX/10, 15)
    else:
        scoreRect.midtop = (frameSizeX/2, frameSizeY/1.25)
    gameWindow.blit(scoreSurface, scoreRect)


# Window size
frameSizeX = 1280
frameSizeY = 720

# Checks for errors encountered
checkErrors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if checkErrors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake')
gameWindow = pygame.display.set_mode((frameSizeX, frameSizeY))


# Setting up colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fpsController = pygame.time.Clock()


# Game variables
snakePos = [100, 50]
snakeBody = [[100, 50], [100-10, 50], [100-(2*10), 50]]

foodPos = [random.randrange(1, (frameSizeX//10)) * 10, random.randrange(1, (frameSizeY//10)) * 10]
foodSpawn = True

direction = 'RIGHT'
changeTo = direction

score = 0


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Insanity  ->  100
difficulty = int(input("Please enter a value 10-100 to set the difficulty: "))


# Main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Whenever a key is pressed down
        elif event.type == pygame.KEYDOWN:
            # W -> Up; S -> Down; A -> Left; D -> Right
            if event.key == pygame.K_UP or event.key == ord('w'):
                changeTo = 'UP'
            if event.key == pygame.K_DOWN or event.key == ord('s'):
                changeTo = 'DOWN'
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                changeTo = 'LEFT'
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                changeTo = 'RIGHT'
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Making sure the snake cannot move in the opposite direction instantaneously
    if changeTo == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if changeTo == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if changeTo == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if changeTo == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snakePos[1] -= 10
    if direction == 'DOWN':
        snakePos[1] += 10
    if direction == 'LEFT':
        snakePos[0] -= 10
    if direction == 'RIGHT':
        snakePos[0] += 10

    # Snake body growing mechanism
    snakeBody.insert(0, list(snakePos))
    if snakePos[0] == foodPos[0] and snakePos[1] == foodPos[1]:
        score += 1
        foodSpawn = False
    else:
        snakeBody.pop()

    # Spawning food on the screen
    if not foodSpawn:
        foodPos = [random.randrange(1, (frameSizeX//10)) * 10, random.randrange(1, (frameSizeY//10)) * 10]
    foodSpawn = True

    # GFX
    gameWindow.fill(black)
    for pos in snakeBody:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(gameWindow, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(gameWindow, white, pygame.Rect(foodPos[0], foodPos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if snakePos[0] < 0 or snakePos[0] > frameSizeX-10:
        gameOver()
    if snakePos[1] < 0 or snakePos[1] > frameSizeY-10:
        gameOver()
    # Touching the snake body
    for block in snakeBody[1:]:
        if snakePos[0] == block[0] and snakePos[1] == block[1]:
            gameOver()

    showScore(1, white, 'consolas', 20)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fpsController.tick(difficulty)
