import pygame
import sys
from button import Button
from asset_loader import *
import random
from random import randint

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BOTTOM_PANEL = 200
FPS = 60
KNIGHT_HEADSHOT_CENTER = 242
lombardic_narrow_font = get_font(27) # font for text (health, mana, etc.)


class Player():
    def __init__(self, x, y, name, max_hp, max_mana, cards, potions, defense):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = max_mana
        self.mana = max_mana
        self.cards = cards
        self.start_potions = potions
        self.potions = potions
        self.defence = defense

        self.image = pygame.transform.scale(PLAYER_KNIGHT_ANIMATION[0], (350, 350)) # initial image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y) # initial position

        self.frame_index = 0
        self.animation_speed = 10
        self.animation_frames = PLAYER_KNIGHT_ANIMATION

    def animate(self):
        if pygame.time.get_ticks() % self.animation_speed == 0:
            previous_frame_index = self.frame_index
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            if self.frame_index != previous_frame_index:
                self.image = pygame.transform.scale(self.animation_frames[self.frame_index], (350, 350))

    def draw(self):
        self.rect.center = ((SCREEN_WIDTH // 2) - 500, SCREEN_HEIGHT // 2) # position next to enemy
        SCREEN.blit(self.image, self.rect)

class Enemy():
    def __init__(self, x, y, name, max_hp_range, defence, attack, assets):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = random.randint(*max_hp_range)
        self.hp = self.max_hp
        self.defence = defence
        self.attack = attack
        self.assets = assets
        self.animation_frames = self.assets[self.name]
        # Scale down the images
        self.image = pygame.transform.scale(self.animation_frames[0], (350, 350)) # scale down
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.frame_index = 0
        self.animation_speed = random.randint(20, 50)  # Random animation speed

    def animate(self):
        if pygame.time.get_ticks() % self.animation_speed == 0:
            previous_frame_index = self.frame_index
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            if self.frame_index != previous_frame_index: # only scale if frame changed
                self.image = pygame.transform.scale(self.animation_frames[self.frame_index], (350, 350))
    
    def draw(self):
        # Adjust the position to place the enemy in the middle of the screen
        self.rect.center = ((SCREEN_WIDTH // 2) + 500, SCREEN_HEIGHT // 2)
        SCREEN.blit(self.image, self.rect)

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp
    
    def draw_health(self, hp): #health to drop and need to be updates
        #draw health bar
        #update with new health
        self.hp = hp
        #calculate health percentage
        ratio = self.hp / self.max_hp #to control the green health
        pygame.draw.rect(SCREEN, 'RED', (self.x, self.y, 150, 20))
        pygame.draw.rect(SCREEN, 'GREEN', (self.x, self.y, 150 * ratio, 20))
        
class ManaBar():
    def __init__(self,x,y,mana,max_mana):
        self.x = x
        self. y = y
        self.mana = mana
        self.max_mana = max_mana
    
    def draw_mana(self, mana):
            self.mana = mana
            ratio = self.mana / self.max_mana
            pygame.draw.rect(SCREEN, 'WHITE', (self.x, self.y, 150, 20))
            pygame.draw.rect(SCREEN, 'BLUE', (self.x, self.y, 150 * ratio, 20))

def play(screen):
    headshot_image = pygame.transform.scale(PLAYER_KNIGHT_HEADSHOT, (150, 150))
    headshot_rect = headshot_image.get_rect()
    headshot_rect.midbottom = ((SCREEN_WIDTH // 4) + 45, SCREEN_HEIGHT - BOTTOM_PANEL + 200)

    knight = Player(0, 0, "knight", 120, 3, 5, 0, 4)  # Animated knight

    eyeball = Enemy(200, 260, "eyeball", (2, 10), 0, 1, ENEMY_ASSETS)
    ghost = Enemy(200, 260, "ghost", (2, 10), 0, 1, ENEMY_ASSETS)
    goblin = Enemy(200, 260, "goblin", (2, 10), 0, 1, ENEMY_ASSETS)
    skeleton = Enemy(200, 260, "skeleton", (2, 10), 0, 1, ENEMY_ASSETS)
    slime = Enemy(200, 260, "slime", (2, 10), 0, 1, ENEMY_ASSETS)

    monster_list = [eyeball, ghost, goblin, skeleton, slime]
    current_monster = random.choice(monster_list)

    player_health_bar = HealthBar(150, SCREEN_HEIGHT - BOTTOM_PANEL + 100, knight.hp, knight.max_hp)
    player_mana_bar = ManaBar(150, SCREEN_HEIGHT - BOTTOM_PANEL + 170, knight.mana, knight.max_mana)
    monster_health_bar = HealthBar((SCREEN_WIDTH // 2) + 500 - 75, (SCREEN_HEIGHT // 2) - 250, current_monster.hp, current_monster.max_hp)
    clock = pygame.time.Clock()

    PLAY_BACK = Button(pygame.Rect(1, 1, 200, 80), (90, 60), "BACK", get_font(75), "White", "Red", 10)

    running = True
    while running:
        screen.fill("black")
        clock.tick(FPS)
        draw_bg()
        screen.blit(headshot_image, headshot_rect) # draw headshot

        player_health_bar.draw_health(knight.hp)
        player_mana_bar.draw_mana(knight.mana)
        knight.draw()
        knight.animate()
        current_monster.draw()
        current_monster.animate()
        monster_health_bar.draw_health(current_monster.hp)
        draw_panel(knight, current_monster)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                running = False
                return "main_menu"

        pygame.display.flip()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))

def draw_bg():
    SCREEN.blit(BATTLE_BACKGROUND_RUINS, (0, 0))

def draw_panel(knight, current_monster):
    monster_location = (SCREEN_WIDTH // 2) + 475, (SCREEN_HEIGHT // 2) - 255

    # draw rectangle panel
    SCREEN.blit(PLAYER_STATUS_BACKGROUND, (0, SCREEN_HEIGHT - BOTTOM_PANEL)) # blit at (0, y)
    # player stats
    draw_text(f'Knight HP: {knight.hp}', lombardic_narrow_font, 'RED', 150, SCREEN_HEIGHT - BOTTOM_PANEL + 60)
    # mana
    draw_text(f'Mana: {knight.mana}', lombardic_narrow_font, 'BLUE', 150, SCREEN_HEIGHT - BOTTOM_PANEL + 130)
    # enemy stats
    draw_text(f'{current_monster.hp} / {current_monster.hp}', lombardic_narrow_font, 'RED', monster_location[0], monster_location[1])

    # draw potions
    health_potion = pygame.image.load(".assets/Potions/potion_health_0.png")
    mana_potion = pygame.image.load(".assets/Potions/potion_mana_0.png")

    health_potion = pygame.transform.scale(health_potion, (120, 120))
    mana_potion = pygame.transform.scale(mana_potion, (120, 120))

    SCREEN.blit(health_potion, (SCREEN_WIDTH // 4 - 120, SCREEN_HEIGHT - BOTTOM_PANEL + 50)) # health potion
    SCREEN.blit(mana_potion, (SCREEN_WIDTH // 4, SCREEN_HEIGHT - BOTTOM_PANEL + 50)) # mana potion

    SCREEN.blit(PLAYER_KNIGHT_WEAPON_SHIELD, (SCREEN_WIDTH // 4 + 55, (SCREEN_HEIGHT // 2 + 50)))
    # SCREEN.blit(PLAYER_KNIGHT_WEAPON_SHIELD, (SCREEN_WIDTH // 4 + 55, randint(int(SCREEN_HEIGHT // 2 + 30), int(SCREEN_HEIGHT // 2 + 70)))) # shield vertical animation (WIP) 
    SCREEN.blit(PLAYER_KNIGHT_WEAPON_SWORD, (SCREEN_WIDTH // 4 - 300, SCREEN_HEIGHT // 2 - 320)) # sword