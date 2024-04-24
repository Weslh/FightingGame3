import pygame
import sys
from pygame import mixer
from Characters.warrior import Warrior
from Characters.wizard import Wizard

sys.path.append('characters/warrior.py')
sys.path.append('characters/wizard.py')

mixer.init()
pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FighterGame3")

#set framerate
clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 1000, 600
#define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000
round_over_time = 0  # Initialize round_over_time before the loop

#define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

#load vicory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
character_select_font = pygame.font.Font("assets/fonts/turok.ttf", 36)

#set initial character choices
fighter_1 = None
fighter_2 = None
fighter_1_choice = None
fighter_2_choice = None
character_selection_complete = False
current_player = 1

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def draw_character_selection():
    screen.fill(WHITE)
    warrior_text = character_select_font.render("Warrior", True, BLACK)
    wizard_text = character_select_font.render("Wizard", True, BLACK)
    
    screen.blit(warrior_text, (WIDTH // 4, HEIGHT // 2))
    screen.blit(wizard_text, (3 * WIDTH // 4, HEIGHT // 2))
    
    pygame.display.flip()


while not character_selection_complete:
    draw_character_selection()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if WIDTH // 4 <= x <= WIDTH // 4 + 100 and HEIGHT // 2 <= y <= HEIGHT // 2 + 20:
                if current_player == 1:
                    fighter_1_choice = "Warrior"
                else:
                    fighter_2_choice = "Warrior"
                current_player = 2 if current_player == 1 else 1  # Switch to next player
            elif 3 * WIDTH // 4 <= x <= 3 * WIDTH // 4 + 100 and HEIGHT // 2 <= y <= HEIGHT // 2 + 20:
                if current_player == 1:
                    fighter_1_choice = "Wizard"
                else:
                    fighter_2_choice = "Wizard"
                current_player = 2 if current_player == 1 else 1  # Switch to next player

    # Check if both players have made their choices
    if fighter_1_choice is not None and fighter_2_choice is not None:
        character_selection_complete = True

if fighter_1_choice == "Warrior":
    fighter_1 = Warrior(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
elif fighter_1_choice == "Wizard":
    fighter_1 = Wizard(1, 200, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

if fighter_2_choice == "Warrior":
    fighter_2 = Warrior(2, 700, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
elif fighter_2_choice == "Wizard":
    fighter_2 = Wizard(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

#game loop
run = True
while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    #update countdown
    if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        #display count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
          intro_count -= 1
          last_count_update = pygame.time.get_ticks()

    # Update sprite flipping based on player positions
    if fighter_1.rect.x < fighter_2.rect.x:
        fighter_1.flip = False
        fighter_2.flip = True
    else:
        fighter_1.flip = True
        fighter_2.flip = False

    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # Check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
          score[1] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
          score[0] += 1
          round_over = True
          round_over_time = pygame.time.get_ticks()
    else:

    
        #display victory image
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            if fighter_1_choice == "Warrior":
                fighter_1 = Warrior(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            elif fighter_1_choice == "Wizard":
                fighter_1 = Wizard(1, 200, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

            if fighter_2_choice == "Warrior":
                fighter_2 = Warrior(2, 700, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            elif fighter_2_choice == "Wizard":
                fighter_2 = Wizard(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #update display
    pygame.display.update()

#exit pygame
pygame.quit()