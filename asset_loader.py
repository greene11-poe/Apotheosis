import pygame
pygame.init()

# Screen setup
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
DARK_GREY = (99, 99, 99)
DARK_GOLD = (182, 143, 64)

# Load font
def get_font(size):
    return pygame.font.Font(".assets/LombardicNarrow-GvWG.ttf", int(size * (SCREEN_WIDTH/1920)))

### MAIN MENU ASSETS ###
MAIN_MENU_BACKGROUND = pygame.image.load(".assets/Main Menu/main_menu_background_castle.png")
MAIN_MENU_BACKGROUND = pygame.transform.scale(MAIN_MENU_BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
# MAP = pygame.image.load(".assets/map_test.png")
# scaled_map = pygame.transform.scale(MAP, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load buttons
PLAY_RECT = pygame.image.load(".assets/Main Menu/rectangle_play.png")
PLAY_RECT = pygame.transform.scale(PLAY_RECT, (int(PLAY_RECT.get_width() * (SCREEN_WIDTH/1920)), int(PLAY_RECT.get_height() * (SCREEN_HEIGHT/1080))))
SETTINGS_RECT = pygame.image.load(".assets/Main Menu/rectangle_settings.png")
SETTINGS_RECT = pygame.transform.scale(SETTINGS_RECT, (int(SETTINGS_RECT.get_width() * (SCREEN_WIDTH/1920)), int(SETTINGS_RECT.get_height() * (SCREEN_HEIGHT/1080))))
QUIT_RECT = pygame.image.load(".assets/Main Menu/rectangle_quit.png")
QUIT_RECT = pygame.transform.scale(QUIT_RECT, (int(QUIT_RECT.get_width() * (SCREEN_WIDTH/1920)), int(QUIT_RECT.get_height() * (SCREEN_HEIGHT/1080))))

# Knight assets
MAINMENUKNIGHT = pygame.image.load(".assets/Main Menu/main_menu_knight.png")
MAINMENUKNIGHT = pygame.transform.scale(MAINMENUKNIGHT, (int(MAINMENUKNIGHT.get_width() * (SCREEN_WIDTH/1920)), int(MAINMENUKNIGHT.get_height() * (SCREEN_HEIGHT/1080))))

# Play menu assets
BATTLE_BACKGROUND_RUINS = pygame.image.load(".assets/Play Menu/background_battle_ruins.png")
PLAYER_STATUS_BACKGROUND = pygame.image.load(".assets/Play Menu/background_player_panel.png")
BATTLE_BACKGROUND_RUINS = pygame.transform.scale(BATTLE_BACKGROUND_RUINS, (SCREEN_WIDTH, int(BATTLE_BACKGROUND_RUINS.get_height() * 1.5))) # Scale to screen width
PLAYER_STATUS_BACKGROUND = pygame.transform.scale(PLAYER_STATUS_BACKGROUND, (SCREEN_WIDTH, int(PLAYER_STATUS_BACKGROUND.get_height() * 1.5))) # Scale to screen width



### PLAYER ASSETS ###
PLAYER_KNIGHT_HEADSHOT = pygame.image.load(".assets/Play Menu/player_knight_headshot.png")

PLAYER_KNIGHT_ANIMATION = [] # includes animation frame by frame
for i in range(1, 6): # from 0 to 5
    frame = pygame.image.load(f".assets/Players/Player_Knight/player_knight_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    PLAYER_KNIGHT_ANIMATION.append(frame)

PLAYER_KNIGHT_WEAPON_SHIELD = pygame.image.load(".assets/Players/Player_Knight/weapon_shield.png")
PLAYER_KNIGHT_WEAPON_SWORD = pygame.image.load(".assets/Players/Player_Knight/weapon_sword.png")
PLAYER_KNIGHT_WEAPON_SHIELD = pygame.transform.scale(PLAYER_KNIGHT_WEAPON_SHIELD, (125, 125))
PLAYER_KNIGHT_WEAPON_SWORD = pygame.transform.scale(PLAYER_KNIGHT_WEAPON_SWORD, (200, 200))
PLAYER_KNIGHT_WEAPON_SWORD = pygame.transform.rotate(PLAYER_KNIGHT_WEAPON_SWORD, -35)  # Rotate clockwise ~35 degrees

### ENEMY ASSETS ###
ENEMY_EYEBALL = []
for i in range(1, 10):
    frame = pygame.image.load(f".assets/Enemies/Enemy_Eyeball/enemy_eyeball_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    ENEMY_EYEBALL.append(frame)

ENEMY_GHOST = []
for i in range(1, 10):
    frame = pygame.image.load(f".assets/Enemies/Enemy_Ghost/enemy_ghost_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    ENEMY_GHOST.append(frame)

ENEMY_GOBLIN  = []
for i in range(1, 10):
    frame = pygame.image.load(f".assets/Enemies/Enemy_Goblin/enemy_goblin_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    ENEMY_GOBLIN.append(frame)

ENEMY_SKELETON = []
for i in range(1, 10):
    frame = pygame.image.load(f".assets/Enemies/Enemy_Skeleton/enemy_skeleton_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    ENEMY_SKELETON.append(frame)

ENEMY_SLIME = []
for i in range(1, 10):
    frame = pygame.image.load(f".assets/Enemies/Enemy_Slime/enemy_slime_{i}.png")
    frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
    ENEMY_SLIME.append(frame)

ENEMY_ASSETS = {
    "eyeball": ENEMY_EYEBALL,
    "ghost": ENEMY_GHOST,
    "goblin": ENEMY_GOBLIN,
    "skeleton": ENEMY_SKELETON,
    "slime": ENEMY_SLIME
}
POTENTIAL_ENEMIES = ["eyeball", "ghost", "goblin", "skeleton", "slime"]
