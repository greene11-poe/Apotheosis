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
BOTTOM_PANEL = 150  # Define the height of the bottom panel
BATTLE_BACKGROUND_RUINS = pygame.image.load(".assets/Play Menu/background_battle_ruins.png")
PLAYER_STATUS_BACKGROUND = pygame.image.load(".assets/Play Menu/background_player_panel.png")
BATTLE_BACKGROUND_RUINS = pygame.transform.scale(BATTLE_BACKGROUND_RUINS, (SCREEN_WIDTH, SCREEN_HEIGHT - BOTTOM_PANEL))  # Adjust scaling to fit above the panel
PLAYER_STATUS_BACKGROUND = pygame.transform.scale(PLAYER_STATUS_BACKGROUND, (SCREEN_WIDTH, int(PLAYER_STATUS_BACKGROUND.get_height() * 1.5))) # Scale to screen width

# Load cave backgrounds for stage 1
background_battle_cave_red = pygame.image.load(".assets/Play Menu/background_battle_cave_red.png")
background_battle_cave_blue = pygame.image.load(".assets/Play Menu/background_battle_cave_blue.png")
background_battle_cave_red = pygame.transform.scale(background_battle_cave_red, (SCREEN_WIDTH, SCREEN_HEIGHT - BOTTOM_PANEL))  # Adjust scaling to fit above the panel
background_battle_cave_blue = pygame.transform.scale(background_battle_cave_blue, (SCREEN_WIDTH, SCREEN_HEIGHT - BOTTOM_PANEL))  # Adjust scaling to fit above the panel

# Load stage 2 backgrounds
background_battle_forest = pygame.image.load(".assets/Play Menu/background_battle_forest.png")
background_battle_forest_alternate = pygame.image.load(".assets/Play Menu/background_battle_forest_alternate.png")

# Load stage 3 background
background_battle_ruins = pygame.image.load(".assets/Play Menu/background_battle_ruins.png")

# Load stage 4 background
background_battle_dungeon = pygame.image.load(".assets/Play Menu/background_battle_dungeon.png")

# Load stage 5 backgrounds
background_battle_castle_halls = pygame.image.load(".assets/Play Menu/background_battle_castle_halls.png")
background_battle_castle_halls_alternate = pygame.image.load(".assets/Play Menu/background_battle_castle_halls_alternate.png")

# Load stage 6 background
background_battle_ramparts = pygame.image.load(".assets/Play Menu/background_battle_ramparts.png")

### PLAYER ASSETS ###
PLAYER_KNIGHT_HEADSHOT = pygame.image.load(".assets/Play Menu/player_knight_headshot.png")
PLAYER_KNIGHT_HEADSHOT = pygame.transform.scale(PLAYER_KNIGHT_HEADSHOT, (150, 150))
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

# Load death animation frames for the knight
death_knight_frames = [
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_0.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_1.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_2.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_3.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_4.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_5.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_6.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player Death/death_knight_7.png"),
]

# Load player attack animation frames
PLAYER_ATTACK_FRAMES = [
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_0.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_1.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_2.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_3.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_4.png"),
    pygame.image.load(".assets/Players/Player_Knight/Player_Attack/player_attack_5.png"),
]

# Load cleave effect
CLEAVE_EFFECT = pygame.image.load(".assets/Cards/Card Art/cleave.png")
CLEAVE_EFFECT = pygame.transform.scale(CLEAVE_EFFECT, (200, 200))  # Scale down for display

### ENEMY ASSETS ###
ENEMY_EYEBALL = []
# Added error handling for loading enemy frames to ensure all enemy types are properly initialized
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Eyeball/enemy_eyeball_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_EYEBALL.append(frame)
    except pygame.error as e:
        print(f"Error loading Eyeball frame {i}: {e}")

ENEMY_GHOST = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Ghost/enemy_ghost_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_GHOST.append(frame)
    except pygame.error as e:
        print(f"Error loading Ghost frame {i}: {e}")

ENEMY_GOBLIN  = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Goblin/enemy_goblin_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_GOBLIN.append(frame)
    except pygame.error as e:
        print(f"Error loading Goblin frame {i}: {e}")

ENEMY_SKELETON = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Skeleton/enemy_skeleton_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_SKELETON.append(frame)
    except pygame.error as e:
        print(f"Error loading Skeleton frame {i}: {e}")

ENEMY_SLIME = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Slime/enemy_slime_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_SLIME.append(frame)
    except pygame.error as e:
        print(f"Error loading Slime frame {i}: {e}")

ENEMY_SLIME_ALTERNATE = []
for i in range(1, 8):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Slime_Alternate/enemy_slime_alternate_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_SLIME_ALTERNATE.append(frame)
    except pygame.error as e:
        print(f"Error loading Slime alternate frame {i}: {e}")

ENEMY_SKELETON_ALTERNATE = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Skeleton_Alternate/enemy_skeleton_alternate_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_SKELETON_ALTERNATE.append(frame)
    except pygame.error as e:
        print(f"Error loading Skeleton alternate frame {i}: {e}")

# Load ghost alternate animation frames
ENEMY_GHOST_ALTERNATE = []
for i in range(1, 10):
    try:
        frame = pygame.image.load(f".assets/Enemies/Enemy_Ghost_Alternate/enemy_ghost_alternate_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_GHOST_ALTERNATE.append(frame)
    except pygame.error as e:
        print(f"Error loading Ghost alternate frame {i}: {e}")

# Load knight animation frames
ENEMY_KNIGHT = []
for i in range(1, 5):  # Changed from range(1, 10) to range(1, 5)
    try:
        frame = pygame.image.load(f".assets\\Enemies\\Enemy_Knight\\enemy_knight_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        ENEMY_KNIGHT.append(frame)
    except pygame.error as e:
        print(f"Error loading Knight frame {i}: {e}")
        # If the frame doesn't exist, break out of the loop to avoid further errors
        break

ENEMY_ASSETS = {
    "eyeball": ENEMY_EYEBALL,
    "ghost": ENEMY_GHOST,
    "goblin": ENEMY_GOBLIN,
    "skeleton": ENEMY_SKELETON,
    "slime": ENEMY_SLIME,
    "slime_alternate": ENEMY_SLIME_ALTERNATE,
    "skeleton_alternate": ENEMY_SKELETON_ALTERNATE,
    "ghost_alternate": ENEMY_GHOST_ALTERNATE,
    "knight": ENEMY_KNIGHT
}
POTENTIAL_ENEMIES = ["eyeball", "ghost", "goblin", "skeleton", "slime", "slime_alternate", "skeleton_alternate", "ghost_alternate", "knight"]

def load_enemy_defeated_animation():
    enemy_defeated_frames = []
    for i in range(8):  # enemy_defeated_0 to enemy_defeated_7
        frame = pygame.image.load(f".assets/Enemies/Enemy_Defeated/enemy_defeated_{i}.png")
        frame = pygame.transform.scale(frame, (int(frame.get_width() * (SCREEN_WIDTH/1920)), int(frame.get_height() * (SCREEN_HEIGHT/1080))))
        enemy_defeated_frames.append(frame)
    return enemy_defeated_frames

ENEMY_DEFEATED_ANIMATION = load_enemy_defeated_animation()

# Load enemy attack animations
ENEMY_ATTACK_CLAW = []
for i in range(7):  # enemy_attack_claw_0 to enemy_attack_claw_6
    frame = pygame.image.load(f".assets/Enemies/Enemy_Attack/enemy_attack_claw_{i}.png")
    frame = pygame.transform.scale(frame, (frame.get_width() // 3, frame.get_height() // 3))
    ENEMY_ATTACK_CLAW.append(frame)

# Initialize the mixer for sound effects
pygame.mixer.init()

# Sound Effects
BLOCK_SFX = pygame.mixer.Sound(".assets/Sound Effects/block_SFX.wav")
GAME_OVER_SFX = pygame.mixer.Sound(".assets/Sound Effects/game_over_SFX.wav")
HEALTH_POTION_SFX = pygame.mixer.Sound(".assets/Sound Effects/health_potion_SFX.wav")
MANA_POTION_SFX = pygame.mixer.Sound(".assets/Sound Effects/mana_potion_SFX.wav")
MONSTER_DEATH_SFX = pygame.mixer.Sound(".assets/Sound Effects/monster_death_SFX.wav")
PLAYER_ATTACK_SFX = pygame.mixer.Sound(".assets/Sound Effects/player_attack_SFX.wav")
PLAYER_DAMAGED_SFX = pygame.mixer.Sound(".assets/Sound Effects/player_damaged_SFX.wav")
VICTORY_SFX = pygame.mixer.Sound(".assets/Sound Effects/victory_SFX.wav")

# Soundtracks
BATTLE_LOOP_OST = pygame.mixer.Sound(".assets/Sound Effects/battle_OST.wav")
MAIN_MENU_OST = pygame.mixer.Sound(".assets/Sound Effects/main_menu_OST.wav")

# Set volume for sound effects
BLOCK_SFX.set_volume(0.4)
GAME_OVER_SFX.set_volume(0.4)
HEALTH_POTION_SFX.set_volume(0.4)
MANA_POTION_SFX.set_volume(0.4)
MONSTER_DEATH_SFX.set_volume(0.2)
PLAYER_ATTACK_SFX.set_volume(0.15)
PLAYER_DAMAGED_SFX.set_volume(0.4)

# Set volume for soundtracks
BATTLE_LOOP_OST.set_volume(0.2)
MAIN_MENU_OST.set_volume(0.2)

ENEMY_INTENT_SWORD = pygame.image.load(".assets/Players/Player_Knight/weapon_sword.png")
ENEMY_INTENT_SWORD = pygame.transform.scale(ENEMY_INTENT_SWORD, (50, 50))

ENEMY_INTENT_SHIELD = pygame.image.load(".assets/Players/Player_Knight/weapon_shield.png")
ENEMY_INTENT_SHIELD = pygame.transform.scale(ENEMY_INTENT_SHIELD, (50, 50))

