import pygame
import sys
from button import Button
from cards import Card
from deck import deck
from event import EventHandler
from screen_transition import fade_transition
from asset_loader import *
from asset_loader import BLOCK_SFX, PLAYER_DAMAGED_SFX, BATTLE_LOOP_OST, GAME_OVER_SFX  # Import sound effects and battle soundtrack
import random
from newcardhud import NewCardHud
import copy

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BOTTOM_PANEL = 200
FPS = 60
KNIGHT_HEADSHOT_CENTER = 242
lombardic_narrow_font = get_font(27) # font for text (health, mana, etc.)

event_handler = EventHandler()
event_handler.game_deck.initialize_deck()
event_handler.game_deck.shuffle_indeck()

# Add a global variable to track the current stage
current_stage = 1

# Add a flag to track whether the reward screen has been shown
reward_screen_shown = False

# Add configurations for the new stages
STAGE_CONFIGS = {
    1: {
        "backgrounds": ["background_battle_cave_red", "background_battle_cave_blue"],
        "enemies": ["slime", "goblin"],
        "waves": 1
    },
    2: {
        "backgrounds": ["background_battle_forest", "background_battle_forest_alternate"],
        "enemies": ["slime_alternate", "goblin"],
        "waves": 1
    },
    3: {
        "backgrounds": ["background_battle_ruins"],
        "enemies": ["ghost", "skeleton"],
        "waves": 1
    },
    4: {
        "backgrounds": ["background_battle_dungeon"],
        "enemies": ["ghost_alternate", "eyeball"],
        "waves": 1
    },
    5: {
        "backgrounds": ["background_castle_entrance", "background_castle_hall"],
        "enemies": ["skeleton_alternate", "skeleton_alternate"],
        "waves": 1
    },
    "boss": {
        "backgrounds": ["background_castle_ramparts"],
        "enemies": ["knight"],
        "waves": 1
    }
}

# Add configuration for stage 6 (boss stage)
STAGE_CONFIGS[6] = {
    "backgrounds": ["background_battle_ramparts"],
    "enemies": ["knight"],
    "waves": 1
}

def get_stage_background(stage):
    """Randomly select a background for the given stage."""
    if stage not in STAGE_CONFIGS:
        raise ValueError(f"Invalid stage: {stage}. Stage not found in STAGE_CONFIGS.")
    return random.choice(STAGE_CONFIGS[stage]["backgrounds"])

def get_stage_enemies(stage):
    """Randomly select enemies for the given stage."""
    enemy_pool = STAGE_CONFIGS[stage]["enemies"]
    # Ensure the number of enemies requested does not exceed the size of the enemy pool
    if len(enemy_pool) < 2:
        return enemy_pool  # Return all available enemies if fewer than 2
    return random.sample(enemy_pool, 2)  # Select 2 enemies otherwise

def transition_to_next_stage(screen):
    """Handle the transition to the next stage."""
    global current_stage
    fade_transition(screen, 500, mode="to_black")  # Reduced from 1000ms to 500ms (50% faster)
    # Filter only integer keys from STAGE_CONFIGS to find the maximum stage
    max_stage = max(key for key in STAGE_CONFIGS.keys() if isinstance(key, int))
    if current_stage < max_stage:  # Ensure current_stage does not exceed the max stage
        current_stage += 1
        fade_transition(screen, 500, mode="out_of_black")  # Reduced from 1000ms to 500ms (50% faster)
    else:
        print(f"[DEBUG] Current stage {current_stage} is the last stage. Transitioning to victory screen.")
        handle_victory(screen)  # Call handle_victory when the last stage is completed

class Player():
    def __init__(self, x, y, name, max_hp, max_mana, cards, defense, block=0):
        self.x = x
        self.y = y
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.block = block
        self.max_mana = max_mana
        self.mana = max_mana
        self.cards = cards
        self.defence = defense

        self.potions = type("Potions", (object, ), {})()
        self.potions.health_potion_uses = 0
        self.potions.mana_potion_uses = 0

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

    def bloodletting(self):
        """Deals 3 damage to the player, respecting block."""
        print("[DEBUG] Bloodletting activated.")  # Debug: Track bloodletting activation
        damage = 3
        if self.block > 0:
            blocked_damage = min(damage, self.block)
            self.block -= blocked_damage
            damage -= blocked_damage
            print(f"[DEBUG] {blocked_damage} damage blocked by knight's block.")  # Debug: Log blocked damage
        else:
            print("[DEBUG] No block available to absorb damage.")  # Debug: Log no block
        self.hp = max(self.hp - damage, 0)  # Ensure HP does not go below 0
        print(f"[DEBUG] Knight takes {damage} unblocked damage from bloodletting. Current HP: {self.hp}.")  # Debug: Log unblocdked damage

    def initialize_potions(self):
        health_potion = pygame.image.load(f".assets/Potions/potion_health_{self.potions.health_potion_uses}.png")
        mana_potion = pygame.image.load(f".assets/Potions/potion_mana_{self.potions.mana_potion_uses}.png")
        self.potions.health_potion = pygame.transform.scale(health_potion, (120, 120))
        self.potions.mana_potion = pygame.transform.scale(mana_potion, (120, 120))


    def use_potion(self, potions, current_player, key_pressed):
        if(self.potions.health_potion_uses < 9 and key_pressed == 1 and self.hp < self.max_hp):
            self.hp = min(self.hp + 10, self.max_hp)  # Heal the player
            self.potions.health_potion_uses += 1
            HEALTH_POTION_SFX.play()  
            print(f"[DEBUG] Health potion used. Current HP: {current_player.hp}.")  # Debug: Log health potion use
        else:
            print("[DEBUG] No health potions left.")  # Debug: Log no potions left
        
        if(self.potions.mana_potion_uses < 8 and key_pressed == 2 and self.mana < self.max_mana):
            self.mana = min(self.mana + 3, self.max_mana)  
            self.potions.mana_potion_uses += 1  
            MANA_POTION_SFX.play()
            print(f"[DEBUG] Mana potion used. Current Mana: {self.mana}.")  # Debug: Log mana potion use
        else:
            print("[DEBUG] No mana potions left.")  # Debug: Log no potions left

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

        self.block = 0
        self.block_turns = 0
        self.intent = random.randint(8,12)

        # Updated to manually copy each surface instead of using deepcopy
        self.animation_frames = [frame.copy() for frame in self.assets[self.name]]  # Manually copy each surface
        self.image = pygame.transform.scale(self.animation_frames[0], (350, 350))  # Initialize with the first frame
        self.defeated_animation_frames = ENEMY_DEFEATED_ANIMATION
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.frame_index = 0
        self.animation_speed = random.randint(40, 80)  # Slowed down animation speed
        self.defeated = False
        self.defeated_frame_index = 0
        self.defeated_animation_speed = 120
        self.defeated_last_update = pygame.time.get_ticks()  # Track last update time

    def draw_intent(self, screen):
        intent_x = self.rect.centerx
        intent_y = self.rect.centery - 60
        screen.blit(ENEMY_INTENT_SWORD, (intent_x - 25, intent_y - 250))

        intent_text = get_font(36).render(f"{self.intent}", True, "WHITE")
        intent_text_rect = intent_text.get_rect(center=(intent_x- 25, intent_y - 220))
        screen.blit(intent_text, intent_text_rect)

    def animate(self):
        if self.defeated:
            current_time = pygame.time.get_ticks()
            if current_time - self.defeated_last_update >= self.defeated_animation_speed:
                self.defeated_last_update = current_time
                if self.defeated_frame_index < len(self.defeated_animation_frames):
                    self.image = pygame.transform.scale(self.defeated_animation_frames[self.defeated_frame_index], (350, 350))
                    self.defeated_frame_index += 1
            return

        if pygame.time.get_ticks() % self.animation_speed == 0:
            previous_frame_index = self.frame_index
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            if self.frame_index != previous_frame_index:
                self.image = pygame.transform.scale(self.animation_frames[self.frame_index], (350, 350))
    
    def draw(self):
        if not self.defeated or self.defeated_frame_index < len(self.defeated_animation_frames):
            SCREEN.blit(self.image, self.rect)

    def attack_player(self, player):
        """Handles enemy attack animations and damage to the player."""
        # print(f"[DEBUG] {self.name.capitalize()} attack_player called")  # Debug: Track calls to attack_player

        for frame in ENEMY_ATTACK_CLAW:
            # Display attack animation on top of the knight's rect
            SCREEN.blit(frame, (player.rect.x + 70, player.rect.y + 150))  # Adjust position as needed
            pygame.display.update()
            pygame.time.delay(10)  # Delay between frames

        # Calculate damage to player
        damage = self.intent
        blocked_damage = 0

        if player.block > 0:
            blocked_damage = min(damage, player.block)
            player.block -= blocked_damage
            damage -= blocked_damage

        player.hp = max(player.hp - damage, 0)  # Ensure HP does not go below 0

        # Play sound effects based on damage
        if blocked_damage > 0 and damage == 0:
            BLOCK_SFX.play()  # Play block sound if all damage is blocked
        if damage > 0:
            PLAYER_DAMAGED_SFX.play()  # Play damaged sound if health is reduced

        # Consolidated debug message
        if blocked_damage > 0:
            print(f"{self.name.capitalize()} deals {blocked_damage} block damage. {self.name.capitalize()} deals {damage} damage to the Knight.")
        else:
            print(f"{self.name.capitalize()} deals {damage} damage to the Knight.")

    def block_player(self, current_monster):
        current_monster.block += self.intent
        self.block_turns = 2 

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


def handle_victory(screen):
    """Handles the victory screen after defeating the boss."""
    # Stop the battle soundtrack
    BATTLE_LOOP_OST.stop()

    # Play victory sound effect once
    VICTORY_SFX.play()

    # Fade to black
    fade_transition(screen, 1000, mode="to_black")

    # Render "VICTORY" and "YOU HAVE ACHIEVED APOTHEOSIS" text
    victory_font = get_font(100)
    subtext_font = get_font(50)
    victory_text = victory_font.render("VICTORY!", True, DARK_GOLD)
    subtext_text = subtext_font.render("YOU HAVE ACHIEVED", True, DARK_GOLD)
    subtext_text_2 = subtext_font.render("APOTHEOSIS", True, DARK_GOLD)

    # Create a button to return to the main menu
    victory_button = Button(None, (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150), "MAIN MENU", get_font(50), "White", "Red")

    while True:
        screen.fill("black")  # Clear the screen first

        # Draw the victory text
        screen.blit(victory_text, (SCREEN_WIDTH // 2 - victory_text.get_width() // 2, 200))
        screen.blit(subtext_text, (SCREEN_WIDTH // 2 - subtext_text.get_width() // 2, 350))
        screen.blit(subtext_text_2, (SCREEN_WIDTH // 2 - subtext_text_2.get_width() // 2, 420))

        # Draw the "MAIN MENU" button
        victory_button.update(screen)
        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if victory_button.checkForInput(pygame.mouse.get_pos()):
                    return "main_menu"  # Return to the main menu state
                
# Update the play function to use stage progression
def play(screen):
    global current_stage
    global reward_screen_shown

    if current_stage not in STAGE_CONFIGS:
        print(f"[DEBUG] Invalid current_stage: {current_stage}. Defaulting to stage 1.")
        current_stage = 1  # Reset to stage 1 if invalid

    # Initialize skip_default_health_bars to False by default
    skip_default_health_bars = False

    # Store the selected background for the current stage
    selected_background = None

    # Load initial stage configuration
    background_image = get_stage_background(current_stage)
    if current_stage == 1:
        current_monsters = [
            Enemy((SCREEN_WIDTH // 2) + 350, SCREEN_HEIGHT // 2, "slime", (16, 20), 0, 1, ENEMY_ASSETS)
        ]
    elif current_stage == 2:
        current_monsters = [
            Enemy(200, 260, name, (20, 24), 0, 1, ENEMY_ASSETS)
            for name in get_stage_enemies(current_stage)
        ]
    elif current_stage == 3:
        background_image = background_battle_ruins
        current_monsters = [
            Enemy(200, 260, "ghost", (15, 20), 0, 1, ENEMY_ASSETS),
            Enemy(200, 260, "skeleton", (35, 40), 0, 1, ENEMY_ASSETS)
        ]
    elif current_stage == 4:
        background_image = background_battle_dungeon
        current_monsters = [
            Enemy(200, 260, "ghost_alternate", (30, 40), 0, 1, ENEMY_ASSETS),
            Enemy(200, 260, "eyeball", (20, 25), 0, 1, ENEMY_ASSETS)
        ]
    elif current_stage == 5:
        if selected_background is None:
            selected_background = random.choice([background_battle_castle_halls, background_battle_castle_halls_alternate])
        background_image = selected_background
        current_monsters = [
            Enemy(200, 260, "skeleton_alternate", (40, 50), 0, 1, ENEMY_ASSETS),
            Enemy(200, 260, "skeleton_alternate", (40, 50), 0, 1, ENEMY_ASSETS)
        ]
    elif current_stage == 6:
        background_image = background_battle_ramparts
        knight_enemy = Enemy((SCREEN_WIDTH // 2) + 500, SCREEN_HEIGHT // 2, "knight", (120, 120), 0, 2, ENEMY_ASSETS)
        current_monsters = [knight_enemy]
        # Create health bar with adjusted position (moved left by 20 more units)
        monster_health_bars = [
            HealthBar((SCREEN_WIDTH // 2) + 500 - 75, (SCREEN_HEIGHT // 2) - 250, knight_enemy.hp, knight_enemy.max_hp)
        ]
        # Skip the normal health bar creation later for stage 6
        skip_default_health_bars = True
    else:
        skip_default_health_bars = False

    # Adjust positions for the two monsters to space them out more
    if len(current_monsters) > 1:
        current_monsters[0].rect.center = ((SCREEN_WIDTH // 2) + 350, SCREEN_HEIGHT // 2)
        current_monsters[1].rect.center = ((SCREEN_WIDTH // 2) + 750, SCREEN_HEIGHT // 2)

    # Update health bars for both monsters
    if not skip_default_health_bars:
        monster_health_bars = [
            HealthBar((SCREEN_WIDTH // 2) + 350 - 75, (SCREEN_HEIGHT // 2) - 250, current_monsters[0].hp, current_monsters[0].max_hp)
        ]
        if len(current_monsters) > 1:
            monster_health_bars.append(
                HealthBar((SCREEN_WIDTH // 2) + 750 - 75, (SCREEN_HEIGHT // 2) - 250, current_monsters[1].hp, current_monsters[1].max_hp)
            )

    # Ensure the game fades out from black when entering a new stage
    fade_transition(screen, 500, mode="out_of_black")  # Reduced from 1000ms to 500ms (50% faster)

    # Ensure the knight object is initialized before resetting mana
    if 'knight' not in locals():
        knight = Player(0, 0, "knight", 90, 3, 5, 0, 4)  # Initialize knight if not already defined

    knight.mana = knight.max_mana  # Reset mana

    while event_handler.game_deck.in_deck:
        card = event_handler.game_deck.in_deck.pop()
        event_handler.game_deck.out_of_deck.append(card)
    event_handler.game_deck.shuffle_indeck()  # Shuffle and draw a new hand

    # Ensure only one music loop plays at a time
    if not BATTLE_LOOP_OST.get_num_channels():
        BATTLE_LOOP_OST.play(loops=-1)

    headshot_image = pygame.transform.scale(PLAYER_KNIGHT_HEADSHOT, (150, 150))
    headshot_rect = headshot_image.get_rect()
    headshot_rect.midbottom = ((SCREEN_WIDTH // 4) + 45, SCREEN_HEIGHT - BOTTOM_PANEL + 200)

    knight = Player(0, 0, "knight", 90, 3, 5, 0, 4)  # player stats

    # Add offsets for the knight's position
    knight_offset_x = -500
    knight_offset_y = 0
    knight.rect.center = ((SCREEN_WIDTH // 2) + knight_offset_x, (SCREEN_HEIGHT // 2) + knight_offset_y)

    # Add a health bar above the knight
    knight_health_bar = HealthBar(knight.rect.centerx - 100, knight.rect.top - 50, knight.hp, knight.max_hp)

    # Move the player HP bar down by 20 units
    player_health_bar = HealthBar(150, SCREEN_HEIGHT - BOTTOM_PANEL + 145, knight.hp, knight.max_hp)
    player_mana_bar = ManaBar(150, SCREEN_HEIGHT - BOTTOM_PANEL + 170, knight.mana, knight.max_mana)
    clock = pygame.time.Clock()

    PLAY_BACK = Button(pygame.Rect(1, 1, 200, 80), (90, 60), "BACK", get_font(75), "White", "Red", 10)

    # Dynamically calculate the size of the text
    end_turn_text = "END TURN [E]"
    end_turn_font = get_font(75)
    end_turn_surface = end_turn_font.render(end_turn_text, True, "White")
    end_turn_rect = end_turn_surface.get_rect()
    
    # Create a button rectangle that matches the text size
    END_TURN = Button(
        pygame.Rect(
            SCREEN_WIDTH - 500, 5, 
            end_turn_rect.width + 20,  # Add padding to width
            end_turn_rect.height + 10  # Add padding to height
        ),
        (90, 60), 
        end_turn_text, 
        end_turn_font, 
        "White", 
        "Red", 
        10
    )
    
    new_card_hud = NewCardHud()


    running = True
    while running:
        screen.fill("black")
        clock.tick(FPS)

        # Replace the ruins background with a random choice between the cave backgrounds for stage 1
        if current_stage == 1:
            if selected_background is None:
                selected_background = random.choice([background_battle_cave_red, background_battle_cave_blue])
            background_image = selected_background
        elif current_stage == 2:
            if selected_background is None:
                selected_background = random.choice([background_battle_forest, background_battle_forest_alternate])
            background_image = selected_background
        elif current_stage == 4:
            background_image = background_battle_dungeon
        elif current_stage == 5:
            if selected_background is None:
                selected_background = random.choice([background_battle_castle_halls, background_battle_castle_halls_alternate])
            background_image = selected_background
        else:
            background_image = BATTLE_BACKGROUND_RUINS

        SCREEN.blit(background_image, (0, 0))
        # screen.blit(headshot_image, headshot_rect)  # draw headshot

        # deck initialization

        player_health_bar.draw_health(knight.hp)
        player_mana_bar.draw_mana(knight.mana)
        knight.draw()
        knight.animate()

        # Draw the knight's health bar and add text for HP
        knight_health_bar.draw_health(knight.hp)
        draw_text(f'{knight.hp} / {knight.max_hp}', lombardic_narrow_font, 'WHITE', knight_health_bar.x + 27, knight_health_bar.y - 5)

        # Replace the yellow circle with the mana_count image
        mana_count_image = pygame.image.load(".assets/Players/Player_Knight/mana_count.png")
        mana_count_image = pygame.transform.scale(mana_count_image, (80, 80))

        # Use a larger font size for the mana text
        mana_font = get_font(60)

        # Draw the mana_count image independently
        mana_count_position = (knight.rect.centerx - 30, knight.rect.top - 100)
        SCREEN.blit(mana_count_image, (knight.rect.centerx + 80, knight.rect.top - 80))

        # Draw the mana text independently
        mana_text_x_offset = 105
        mana_text_y_offset = 25
        draw_text(f'{knight.mana}', mana_font, 'BLUE', knight.rect.centerx + mana_text_x_offset, knight.rect.top - 100 + mana_text_y_offset)

        # Draw and animate both monsters
        for i, monster in enumerate(current_monsters):
            monster.draw()
            monster.animate()
            if monster_health_bars[i]:
                monster_health_bars[i].draw_health(monster.hp)
            current_monsters[i].draw_intent(screen)  # Draw intent for each monster
        
        

        # Updated logic to handle defeated animations and health bar updates for individual enemies
        for i, monster in enumerate(current_monsters):
            if monster.hp <= 0 and not monster.defeated:
                monster.defeated = True  # Trigger defeated animation
                monster.defeated_frame_index = 0  # Reset animation frame index

            if monster.defeated and monster.defeated_frame_index >= len(monster.defeated_animation_frames):
                current_monsters[i] = None  # Remove defeated monster
                monster_health_bars[i] = None  # Remove corresponding health bar

        # Filter out None values to clean up the lists
        current_monsters = [m for m in current_monsters if m is not None]
        monster_health_bars = [hb for hb in monster_health_bars if hb is not None]

        # If all monsters are defeated, activate the reward screen (except for stage 6)
        if not current_monsters and not reward_screen_shown and current_stage < 6:
            new_card_hud.activate()
            reward_screen_shown = True

        # Transition to the next stage after claiming rewards or directly for stage 6
        if new_card_hud.active == False and not current_monsters:
            reward_screen_shown = False  # Reset the flag
            if current_stage < len(STAGE_CONFIGS):
                transition_to_next_stage(screen)
                return play(screen)  # Restart play for the next stage
            else:
                print("All stages completed!")
                return "main_menu"  # Return to main menu after all stages

        draw_panel(knight, current_monsters)  # Update panel with the current monsters

        if knight.hp <= 0:
            BATTLE_LOOP_OST.stop()  # Stop the battle soundtrack
            return handle_player_death(screen)

        event_handler.game_deck.draw_deck(screen)       

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        # Updated button logic to visually disable buttons during the reward screen
        if new_card_hud.active:
            new_card_hud.draw_hud(screen, event_handler)  # Draw the reward screen
            pygame.display.flip()  # Update the display

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for card in new_card_hud.hud_deck:
                        if card.rect.collidepoint(mouse_pos):
                            event_handler.game_deck.out_of_deck.append(card)  # Add selected card to the deck
                            new_card_hud.active = False  # Close the reward screen
                            break
                    if new_card_hud.active and new_card_hud.skip_button_rect.collidepoint(mouse_pos):
                        new_card_hud.active = False  # Close the reward screen if skip is clicked
            continue  # Skip further updates for this frame

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        END_TURN.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(screen)
        END_TURN.update(screen)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                BATTLE_LOOP_OST.stop()  # Stop the battle soundtrack
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:  # 
                    # print("[E] key pressed to end turn")
                    end_turn(knight, current_monsters)
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    BATTLE_LOOP_OST.stop()  # Stop the battle soundtrack
                    return "main_menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(f"Mouse Position: {PLAY_MOUSE_POS}")  # Debug: Print mouse position
                # print(f"BACK Button Rect: {PLAY_BACK.rect}")  # Debug: Print BACK button rect
                # print(f"END TURN Button Rect: {END_TURN.rect}")  # Debug: Print END TURN button rect

                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    print("BACK button clicked")  # Debug: Confirm button click
                    running = False
                    BATTLE_LOOP_OST.stop()  # Stop the battle soundtrack
                    return "main_menu"

                if END_TURN.checkForInput(PLAY_MOUSE_POS):
                    print("END TURN button clicked")  # Debug: Confirm button click
                    end_turn(knight, current_monsters)

        # Pass the shared event list to EventHandler
        event_handler.check_events(knight, current_monsters, events, screen, new_card_hud)  # Pass screen as an argument

        # Ensure the transparent overlay and HUD are drawn last
        if new_card_hud.active:
            new_card_hud.draw_hud(screen, event_handler)  # Pass event_handler to draw_hud

        pygame.display.flip()

# Define a helper function to handle end turn logic
def end_turn(knight, current_monsters):
    """Handles the end of the player's turn, including resetting mana, shuffling cards, and enemy attack."""
    # print("[DEBUG] end_turn called")  # Debug: Track calls to end_turn

    knight.mana = knight.max_mana  # Reset mana

    # Move all remaining cards in the current hand to the discard pile
    while event_handler.game_deck.in_deck:
        card = event_handler.game_deck.in_deck.pop()
        event_handler.game_deck.out_of_deck.append(card)

    # Reset card positions in the panel
    for index, card in enumerate(event_handler.game_deck.out_of_deck):
        card.rect.topleft = (150 + index * 160, SCREEN_HEIGHT - BOTTOM_PANEL + 20)  # Adjust card positions

    # Shuffle and draw a new hand (limit to 5 cards)
    event_handler.game_deck.shuffle_indeck()

    # Enemy attacks the player at the end of the turn
    for monster in current_monsters:
        if monster.hp > 0:
            monster.intent = random.randint(8, 12) 
            random_action = random.randint(1, 2)  
            if random_action == 1:
                monster.attack_player(knight)  
            elif random_action == 2:
                monster.block_player(monster) 
        if monster.block_turns > 0:
            monster.block_turns -= 1
        if monster.block_turns == 0:
            monster.block = 0

    # Reset block to 0 at the end of the turn
    knight.block = 0

def handle_player_death(screen):
    """Handles player death by playing a death animation, fading to black, and presenting a button to return to the main menu."""

    # Play game over sound effect once
    GAME_OVER_SFX.play()

    # Play player death animation
    for index, frame in enumerate(death_knight_frames):  # Use frames from asset_loader.py
        screen.fill("black")  # Clear the screen
        y_offset = 120 if index >= 4 else 0  # Lower frames 4-7 by 120 units
        SCREEN.blit(frame, ((SCREEN_WIDTH // 2) - 600, (SCREEN_HEIGHT // 2) - 100 + y_offset))  # Adjusted position
        pygame.display.update()
        pygame.time.delay(150)  # Delay between frames

    # Pause on the last frame
    pygame.time.delay(1000)

    # Fade to black
    fade_transition(screen, 1000, mode="to_black")

    # Render "GAME OVER" as a non-clickable button
    GAME_OVER_BUTTON = Button(None, (SCREEN_WIDTH // 2, 200), "GAME OVER", get_font(100), "Red", "Red")

    # Create a button to return to the main menu
    death_button = Button(None, (SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 400), "MAIN MENU", get_font(50), "White", "Red")

    while True:
        screen.fill("black")  # Clear the screen first
        GAME_OVER_BUTTON.update(screen)  # Render "GAME OVER" text after clearing the screen
        death_button.update(screen)  # Render the "MAIN MENU" button
        pygame.display.update()  # Update the display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if death_button.checkForInput(pygame.mouse.get_pos()):
                    return "main_menu"  # Return to the main menu state

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    SCREEN.blit(img, (x, y))

def draw_bg():
    SCREEN.blit(BATTLE_BACKGROUND_RUINS, (0, 0))

def draw_panel(knight, current_monsters):
    """Draws the player and monster stats panel."""
    # Dynamically calculate monster locations based on their rect positions
    monster_locations = [
        (monster.rect.centerx - 75, monster.rect.top - 50) for monster in current_monsters if monster
    ]

    # Draw rectangle panel
    SCREEN.blit(PLAYER_STATUS_BACKGROUND, (0, SCREEN_HEIGHT - BOTTOM_PANEL))  # blit at (0, y)
    
    # Player stats - using simpler text implementation instead of drawing bars directly
    draw_text(f'Knight HP: {knight.hp}', lombardic_narrow_font, 'RED', 160, SCREEN_HEIGHT - BOTTOM_PANEL + 60)
    draw_text(f'Mana: {knight.mana}', lombardic_narrow_font, 'BLUE', 150, SCREEN_HEIGHT - BOTTOM_PANEL + 130)

    # Enemy stats
    for i, monster in enumerate(current_monsters):
        if monster and monster.hp > 0:  # Ensure monster is not None
            draw_text(f'{monster.hp} / {monster.max_hp}', lombardic_narrow_font, 'WHITE', monster_locations[i][0] + 25, monster_locations[i][1] - 30)
            draw_text(f'Block: {monster.block}', lombardic_narrow_font, 'WHITE', monster_locations[i][0] + 100, monster_locations[i][1] - 1)

    # draw potions
    try:
        health_potion = pygame.image.load(f".assets/Potions/potion_health_{knight.potions.health_potion_uses}.png")
    except FileNotFoundError:
        health_potion = pygame.image.load(f".assets/Potions/potion_health_8.png")
    try:
        mana_potion = pygame.image.load(f".assets/Potions/potion_mana_{knight.potions.mana_potion_uses}.png")
    except FileNotFoundError:
        mana_potion = pygame.image.load(f".assets/Potions/potion_mana_7.png")


    health_potion = pygame.transform.scale(health_potion, (120, 120))
    mana_potion = pygame.transform.scale(mana_potion, (120, 120))

    SCREEN.blit(health_potion, (SCREEN_WIDTH // 4 - 120, SCREEN_HEIGHT - BOTTOM_PANEL + 50))  # health potion
    SCREEN.blit(mana_potion, (SCREEN_WIDTH // 4, SCREEN_HEIGHT - BOTTOM_PANEL + 50))  # mana potion