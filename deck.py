from cards import Card
from random import randint
import pygame  
from time import sleep
from asset_loader import *

class deck:
    def __init__(self):
        self.in_deck = []
        self.out_of_deck = []

    # Updated the deck initialization to start with 6 cards: 3x Strike and 3x Defend
    def initialize_deck(self):
        # Ensure only default cards (Strike and Defend) are added to the deck initially
        x = (((800 - (5 * (225 // 2))) // 2))
        y = 1080 - 350
        for i in range(6):
            if i < 3:
                card = Card(
                    "Strike", 1, 6,  # Pass damage value
                    pygame.transform.scale(pygame.image.load(".assets/Cards/card_strike.png"), (225, 225)),
                    x, y
                )
                self.out_of_deck.append(card)
            else:
                card = Card(
                    "Defend", 1, 5,  # Pass damage value
                    pygame.transform.scale(pygame.image.load(".assets/Cards/card_defend.png"), (225, 225)),
                    x, y
                )
                self.out_of_deck.append(card)
    
    
    def shuffle_indeck(self):
        card_counts = {}

        for i in range(5):
            rand_index = randint(0, len(self.out_of_deck) - 1)
            card = self.out_of_deck[rand_index]

            # Count occurrences of each card type in the hand
            card_name = card.name
            if card_name not in card_counts:
                card_counts[card_name] = 0

            # Ensure at most 1 of the new cards and up to 3 of Strike/Defend
            if (card_name in ["Strike", "Defend"] and card_counts[card_name] < 3) or \
               (card_name not in ["Strike", "Defend"] and card_counts[card_name] < 1):
                self.out_of_deck.pop(rand_index)
                self.in_deck.append(card)
                card_counts[card_name] += 1

        x = (1920 // 3) - 36  # Adjust x-coordinate for screen dimensions
        change = 125
        y = 1080 - 350

        for card in self.in_deck:
            card.x = x
            x += change
            card.y = y           
    
    def shuffle_outofdeck(self):
        for i in range(4):
            rand_index = randint(0, len(self.in_deck) - 1)
            card = self.in_deck.pop(rand_index)
            self.out_of_deck.append(card)

    def draw_deck(self, screen):
        for card in self.in_deck:
            screen.blit(card.image, (card.x, card.y))
    
    def draw_card(self):
        card = self.out_of_deck[randint(0, len(self.out_of_deck) - 1)]
        self.out_of_deck.remove(card)
        self.in_deck.append(card)
        self.draw_deck
    
    def use_card(self, card, current_player, monster, screen):
        """Use a card to apply its effects to the selected monster or player, with visual effects."""
        # Apply card effects
        if card.name == "Strike":
            current_player.mana -= 1
            damage = card.damage

            blocked_damage = min(damage, monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)

            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()}.")
            
        elif card.name == "Defend":
            current_player.mana -= 1
            current_player.block += card.damage
            print(f"{card.name} adds {card.damage} block to the player.")
            BLOCK_SFX.play()  # Play block sound effect
        elif card.name == "Bloodletting":
            current_player.hp -= 3
            current_player.mana += 2
            print(f"{card.name} deals 3 damage to the player.")
            PLAYER_DAMAGED_SFX.play()
        elif card.name == "Bash":
            current_player.mana -= 2
            damage = card.damage

            blocked_damage = min(damage, monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()}.")
        elif card.name == "Cleave":
            current_player.mana -= 1
            damage = card.damage

            blocked_damage = min(monster.hp, damage - monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()}.")
        elif card.name == "Twin Strike":
            current_player.mana -= 1
            damage = card.damage

            blocked_damage = min(monster.hp, damage - monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()} (first strike).")
            sleep(0.25)  # Simulate delay for the second strike
            monster.hp -= card.damage
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect again
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()} (second strike).")
        elif card.name == "Pommel Strike":
            current_player.mana -= 1
            damage = card.damage

            blocked_damage = min(monster.hp, damage - monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()}.")
            # Generate a new card in the same position as the original card
            new_card = self.out_of_deck.pop(randint(0, len(self.out_of_deck) - 1))
            new_card.x, new_card.y = card.x, card.y
            self.in_deck.append(new_card)
        elif card.name == "Iron Wave":
            current_player.mana -= 1
            damage = card.damage

            blocked_damage = min(monster.hp, damage - monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            current_player.block += card.damage
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()} and adds {card.damage} block to the player.")
        elif card.name == "Bludgeon":
            current_player.mana -= 3
            damage = card.damage

            blocked_damage = min(monster.hp, damage - monster.block)
            monster.block -= blocked_damage
            damage -= blocked_damage

            monster.hp = max(monster.hp - damage, 0)
            
            PLAYER_ATTACK_SFX.play()  # Play player attack sound effect
            self.play_attack_effect(screen, monster)
            print(f"{card.name} deals {card.damage} damage to {monster.name.capitalize()}.")

        # Play monster death sound effect if monster dies
        if monster.hp <= 0:
            MONSTER_DEATH_SFX.play()
            print(f"{monster.name.capitalize()} has been defeated!")


        # Play monster death sound effect if monster dies
        if monster.hp <= 0:
            MONSTER_DEATH_SFX.play()
            print(f"{monster.name.capitalize()} has been defeated!")

    def play_attack_effect(self, screen, monster):
        """Play the attack visual effect on the monster."""
        # Adjustable offsets
        attack_offset_x = 25
        attack_offset_y = 25

        # Scale down and animate player attack frames
        for frame in PLAYER_ATTACK_FRAMES:
            frame_scaled = pygame.transform.scale(frame, (int(frame.get_width() * 0.4), int(frame.get_height() * 0.4)))
            attack_rect = frame_scaled.get_rect(center=(monster.rect.centerx + attack_offset_x, monster.rect.centery + attack_offset_y))
            screen.blit(frame_scaled, attack_rect)
            pygame.display.update()
            pygame.time.delay(50)  # Increased delay to slow down animation by 50%