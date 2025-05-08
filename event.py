import pygame as pg
import sys
import time
from deck import deck

double_click_speed = 318 # milliseconds

class EventHandler:
    def __init__(self):
        self.dragging_card = None
        self.game_deck = deck()
        self.cards = self.game_deck.in_deck 
        self.last_click_time = 0  # Track the time of the last click
        self.original_position = None  # Store the original position of the dragged card

    def check_events(self, current_player, current_monster, events, screen, new_card_hud):
        """Handle all events, including double-clicks."""
        # Added a check to disable card operations during the reward screen
        if new_card_hud.active:
            return  # Skip all card-related operations if the reward screen is active
        for event in events:  # Use the shared event list
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Process card-related events only if no button is clicked
                if not any(button.rect.collidepoint(event.pos) for button in self.cards):
                    self.check_mousedown_events(event, new_card_hud)
                    self.double_click(event, current_player, current_monster, screen)  # Pass screen
            elif event.type == pg.MOUSEMOTION:
                self.mouse_motion(event)
            elif event.type == pg.MOUSEBUTTONUP:
                self.check_mouseup_events(event)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    current_player.use_potion(current_player.potions, current_player, 1)  # Pass screen
                elif event.key == pg.K_2:
                    current_player.use_potion(current_player.potions, current_player, 2)  # Pass screen

    def check_mousedown_events(self, event, new_card_hud):
        """Respond to mouse events"""
        if event.button == 1:
            for card in self.cards:
                card_rect = card.image.get_rect(topleft=(card.x, card.y))
                if card_rect.collidepoint(event.pos):
                    self.dragging_card = card
                    self.original_position = (card.x, card.y)  # Save the original position
                    break
            # print("out_of_deck") #debug get rid of this later
            for card in self.game_deck.out_of_deck:
                # print(f"out_of_deck: {card.name}")  #debug get rid of this later
                pass
            if new_card_hud.active:
                for card in new_card_hud.hud_deck:
                    card_rect = card.image.get_rect(topleft=(card.x, card.y))
                    if card_rect.collidepoint(event.pos):
                        self.game_deck.out_of_deck.append(card)
                        print("out_of_deck") #debug get rid of this later
                        for card in self.game_deck.out_of_deck:
                            # print(f"out_of_deck: {card.name}")  #debug get rid of this later
                            pass
                        new_card_hud.active = False

    def check_mouseup_events(self, event):
        """Respond to mouse release"""
        if event.button == 1:
            if self.dragging_card:
                # Snap back to the original position if not played
                self.dragging_card.x, self.dragging_card.y = self.original_position
            self.dragging_card = None
            self.original_position = None

    def mouse_motion(self, event):
        """Respond to mouse motion and move cards while cursor moves"""
        if self.dragging_card:
            card_rect = self.dragging_card.image.get_rect()
            self.dragging_card.x = event.pos[0] - card_rect.width // 2
            self.dragging_card.y = event.pos[1] - card_rect.height // 2

    # Updated double_click method to target the leftmost enemy
    def double_click(self, event, current_player, current_monsters, screen):
        """Handle double-click events."""
        if event.button == 1:  # Left mouse button
            current_time = time.time() * 1000  # Get current time in milliseconds
            if current_time - self.last_click_time <= double_click_speed:
                if self.dragging_card:
                    # Ensure the current_monsters list has enough elements before accessing indices
                    if len(current_monsters) > 0:
                        target_enemy = current_monsters[0] if current_monsters[0].hp > 0 else (current_monsters[1] if len(current_monsters) > 1 else None)
                    else:
                        target_enemy = None

                    # Proceed only if a valid target_enemy is found
                    if target_enemy:
                        self.game_deck.use_card(self.dragging_card, current_player, target_enemy, screen)  # Pass screen
                        if self.dragging_card in self.cards:  # checks if in deck
                            self.cards.remove(self.dragging_card)
                            self.game_deck.out_of_deck.append(self.dragging_card)
                        self.dragging_card = None
            self.last_click_time = current_time

    def reset_game_state(self):
        """Resets the game state to allow card interactions after unpausing."""
        self.dragging_card = None
        self.original_position = None
        self.last_click_time = 0
        self.cards = self.game_deck.in_deck
        print("[DEBUG] Game state reset after unpausing.")