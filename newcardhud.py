import pygame
import sys
from button import Button
from cards import Card
from deck import deck
from event import EventHandler
from screen_transition import fade_transition
from asset_loader import *
import random

class NewCardHud:
    def __init__(self):
        self.hud_deck = []  # Stores the cards to display in the HUD
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))  # Semi-transparent background
        self.background.set_alpha(128)
        self.background.fill((0, 0, 0))
        self.active = False
        self.skip_button_rect = None  # Initialize skip button rect

    
    def activate(self):
        self.active = True
        self.generate_hdeck(SCREEN)
    
    def generate_hdeck(self, screen):
        new_cards = [
            ("Bloodletting", 3, ".assets/Cards/card_bloodletting.png"),
            ("Bludgeon", 32, ".assets/Cards/card_bludgeon.png"),
            ("Cleave", 8, ".assets/Cards/card_cleave.png"),
            ("Iron Wave", 5, ".assets/Cards/card_iron_wave.png"),
            ("Bash", 8, ".assets/Cards/card_Bash.png"),
            ("Pommel Strike", 9, ".assets/Cards/card_pommel_strike.png"),
            ("Twin Strike", 5, ".assets/Cards/card_twin_strike.png")
        ]

        selected_cards = random.sample(new_cards, 3)

        self.hud_deck = []

        card_width, card_height = 225, 225
        change_x = 50

        # Center the 2nd card (2/3) using its center, then add offsets for adjustments
        start_x = SCREEN_WIDTH // 2 - card_width // 2 - (change_x + card_width)
        start_y = 540 - card_height // 2
        offset_x = 0  # Adjust this value to move the cards horizontally
        offset_y = -40  # Adjust this value to move the cards vertically

        for (name, damage, image_path) in selected_cards:
            card_x = start_x + (change_x + card_width) * len(self.hud_deck) + offset_x
            card_y = start_y + offset_y
            card = Card(
                name, 1, damage,
                pygame.transform.scale(pygame.image.load(image_path), (card_width, card_height)),
                card_x, card_y
            )
            card.rect = card.image.get_rect(topleft=(card.x, card.y))
            self.hud_deck.append(card)


         
    def draw_hud(self, screen, event_handler):
        if not self.active:
            event_handler.reset_game_state()  # Reset game state to allow interactions
            return
        
        # print("Drawing HUD")
        
        screen.blit(self.background, (0, 0))

        # Draw a rounded grey rectangle behind the cards
        rect_width = 1000
        rect_height = 500
        rect_x = SCREEN_WIDTH // 2 - rect_width // 2
        rect_y = 500 - rect_height // 2
        rounded_rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
        pygame.draw.rect(rounded_rect, (0,0,0, 220), (0, 0, rect_width, rect_height), border_radius=20)
        screen.blit(rounded_rect, (rect_x, rect_y))

        # Draw the text "Choose a Card!" slightly above the cards using the `get_font` function from asset_loader
        text_surface = get_font(72).render("Choose a Card!", True, "White")
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, rect_y + 70))  # Position above the rectangle
        screen.blit(text_surface, text_rect)

        for card in self.hud_deck:
            screen.blit(card.image, (card.x, card.y))

        # Add a skip button to the rewards screen
        skip_button_text = "Skip"
        skip_button_font = get_font(72)
        skip_button_surface = skip_button_font.render(skip_button_text, True, "White")
        self.skip_button_rect = skip_button_surface.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 140))

        # Check for hover and click
        mouse_pos = pygame.mouse.get_pos()
        if self.skip_button_rect.collidepoint(mouse_pos):
            skip_button_surface = skip_button_font.render(skip_button_text, True, "Red")
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                self.active = False  # Dismiss the reward screen
        
        screen.blit(skip_button_surface, self.skip_button_rect)

    def handle_events(self, event, event_handler):
        """Handle events for the reward screen."""
        if not self.active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            for card in self.hud_deck:
                card_rect = card.image.get_rect(topleft=(card.x, card.y))
                if card_rect.collidepoint(event.pos):
                    event_handler.game_deck.out_of_deck.append(card)
                    self.hud_deck.remove(card)  # Remove the selected card from the reward deck
                    self.active = False  # Deactivate the reward screen
                    return

            if self.skip_button_rect and self.skip_button_rect.collidepoint(event.pos):
                self.active = False  # Deactivate the reward screen if skip is clicked

