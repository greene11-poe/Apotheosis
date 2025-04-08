import pygame

class Button:
    def __init__(self, rect_or_image, pos, text_input, font, base_color, hovering_color, text_offset_y=0):
        self.text_input = text_input

        if isinstance(rect_or_image, pygame.Rect):
            self.rect = rect_or_image
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            self.image.fill((0, 0, 0, 0))
        else:
            self.image = rect_or_image if rect_or_image else font.render(text_input, True, base_color)
            self.rect = self.image.get_rect(center=pos)

        self.text = font.render(text_input, True, base_color)
        self.text_rect = self.text.get_rect(center=(pos[0], pos[1] + text_offset_y))
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color

        # Combine button and text rects for accurate collision
        self.combined_rect = self.rect.union(self.text_rect)

    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.combined_rect.collidepoint(position)

    def changeColor(self, position):
        if self.combined_rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)