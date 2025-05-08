import pygame

class Card:
    def __init__(self, name, mana_cost, damage, image, x, y):
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage  # Add damage attribute
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


