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
        # Center the text relative to the button's rect
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.text_rect.y += text_offset_y  # Apply vertical offset if needed

        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.is_hovered = False  # Track hover state

    def update(self, screen):
        # Render the button image and text once per frame
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, mouse_pos):
        # Check if the mouse position is within the button's rect
        is_clicked = self.rect.collidepoint(mouse_pos)
        # print(f"Mouse Position: {mouse_pos}, Button Rect: {self.rect}, Clicked: {is_clicked}")  # Debug: Print details
        return is_clicked

    def changeColor(self, position):
        # Update text color only if the hover state changes
        if self.rect.collidepoint(position):
            if not self.is_hovered:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
                self.is_hovered = True
                # print(f"Button '{self.text_input}' is hovered.")  # Debug: Hover state
        else:
            if self.is_hovered:
                self.text = self.font.render(self.text_input, True, self.base_color)
                self.is_hovered = False
                # print(f"Button '{self.text_input}' is not hovered.")  # Debug: Hover state