import pygame, sys
from button import Button
from asset_loader import SCREEN, get_font, DARK_GREY


def settings(screen, render_only=False):  # Added render_only parameter
    SETTINGS_BACK = Button(None, (960, 900), "BACK", get_font(75), "Grey", "White")  # Adjusted position

    # Render the settings screen content
    screen.fill(DARK_GREY)  # Use passed screen

    SETTINGS_TEXT = get_font(72).render("This is the SETTINGS screen.", True, "Black")  # Increased font size
    screen.blit(SETTINGS_TEXT, SETTINGS_TEXT.get_rect(center=(960, 360)))  # Adjusted Position

    SETTINGS_BACK.update(screen)  # Use passed screen

    pygame.display.update()

    # If render_only is True, return immediately after rendering
    if render_only:
        return

    # Main loop for the settings screen
    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        SETTINGS_BACK.changeColor(SETTINGS_MOUSE_POS)
        SETTINGS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):  # Added escape key
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                return "main_menu"  # Return to main menu state

        pygame.display.update()