import pygame
import random
import os

pygame.mixer.init()
pygame.init()

white = (255, 255, 255)
red = (125, 0, 0)
black = (0, 0, 0)

screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))
# Background
bimg = pygame.image.load("D:\Ggame\Images\mbackground.png")
bimg = pygame.transform.scale(bimg, (screen_width, screen_height)).convert_alpha()

pygame.display.update()
pygame.display.set_caption("Snakes")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x , y):
    text_on = font.render(text, True, color)
    gameWindow.blit(text_on, [x, y])

def plot_snk(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])
# Main Menu
def menu():
    exit_game = False
    pygame.mixer.music.load('D:\Ggame\Music\menu.mp3')
    pygame.mixer.music.play()

    while not exit_game:
        gameWindow.fill(black)
        gameWindow.blit(bimg, (0, 0))

        text_screen("Press Return/Enter to continue", (125, 0, 0), 170, screen_height - 50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.unload()
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.unload()
                    gameLoop()
        pygame.display.update()
        clock.tick(60)

# Game Loop
def gameLoop():
    #  Game specific variables
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    snake_size = 20
    v_x = 0
    v_y = 0
    fps = 60
    init_v = 7
    food_x = random.randint(100, screen_width / 1.5)
    food_y = random.randint(100, screen_height / 1.5)
    food_size = 15
    score = 0
    snk_length = 1
    snk_list = []
    pygame.mixer.music.load('D:\Ggame\Music\gback.mp3')
    pygame.mixer.music.play()

    if(not os.path.exists("hiScore.txt")):
        with open("hiScore.txt", "w") as f:
            f.write("0")
    with open("hiScore.txt", "r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("hiScore.txt", "w") as f:
                f.write(str(hiscore))

            gimg = pygame.image.load("D:\Ggame\Images\Game_over.png")
            gimg = pygame.transform.scale(gimg, (screen_width, screen_height)).convert_alpha()

            gameWindow.fill(black)
            gameWindow.blit(gimg, (0, 0))

            #text_screen("GAME OVER :( !!!", red, 275, screen_height / 2 - 100)
            text_screen("Wanna Retry !?! press Return", red, 175, screen_height/2-50)
            text_screen("To Give Up press Space", red, 225, screen_height / 2 )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameLoop()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        v_x = init_v
                        v_y = 0
                    elif event.key == pygame.K_LEFT:
                        v_x = -init_v
                        v_y = 0
                    elif event.key == pygame.K_UP:
                        v_x = 0
                        v_y = -init_v
                    elif event.key == pygame.K_DOWN:
                        v_x = 0
                        v_y = init_v
                    if event.key == pygame.K_q:
                        score += 5
                    if event.key == pygame.K_k:
                        init_v += 1
                    if event.key == pygame.K_l:
                        init_v -= 1

            snake_x += v_x
            snake_y += v_y

            if abs(food_x - snake_x) < 15 and abs(food_y - snake_y) < 15:
                score += 10
                food_x = random.randint(100, screen_width/1.5)
                food_y = random.randint(100, screen_height/1.5)
                snk_length += 5
                init_v += 1

            if score > int(hiscore):
                hiscore = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.unload()
                pygame.mixer.music.load('D:\Ggame\Music\gover.mp3')
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 0 or snake_x  > screen_width or snake_y < 0 or snake_y > screen_height :
                pygame.mixer.music.unload()
                pygame.mixer.music.load('D:\Ggame\Music\gover.mp3')
                pygame.mixer.music.play()
                game_over = True

            gameWindow.fill(black)
            text_screen("Score : "+str(score * 10), red, 5, 5)
            text_screen("High Score : " + str(int(hiscore) * 10), red, 5, 50)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, food_size, food_size])
            plot_snk(gameWindow, red, snk_list, snake_size)
        clock.tick(fps)
        pygame.display.update()

    pygame.quit()
    quit()

menu()


