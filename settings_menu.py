import pygame, sys
from button import Button
from asset_loader import SCREEN, get_font, DARK_GREY

# Define common resolutions
RESOLUTIONS = [(1920, 1080)]  # Only keep 1920x1080
FULLSCREEN = False  # Track fullscreen state

def settings(screen, render_only=False):
    global FULLSCREEN

    SETTINGS_BACK = Button(None, (960, 900), "BACK", get_font(75), "Grey", "White")
    RESOLUTION_BUTTONS = [
        Button(None, (960, 500 + i * 100), f"{res[0]}x{res[1]}", get_font(50), "Grey", "White")
        for i, res in enumerate(RESOLUTIONS)
    ]
    FULLSCREEN_BUTTON = Button(None, (960, 800), "TOGGLE FULLSCREEN", get_font(50), "Grey", "White")
    EXIT_FULLSCREEN_BUTTON = Button(None, (960, 700), "EXIT FULLSCREEN", get_font(50), "Grey", "White")

    # Render the settings screen content
    screen.fill(DARK_GREY)

    SETTINGS_TEXT = get_font(72).render("SETTINGS", True, "Black")
    screen.blit(SETTINGS_TEXT, SETTINGS_TEXT.get_rect(center=(960, 200)))

    SETTINGS_BACK.update(screen)
    for button in RESOLUTION_BUTTONS:
        button.update(screen)
    FULLSCREEN_BUTTON.update(screen)
    EXIT_FULLSCREEN_BUTTON.update(screen)

    pygame.display.update()

    if render_only:
        return

    # Main loop for the settings screen
    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        SETTINGS_BACK.changeColor(SETTINGS_MOUSE_POS)
        for button in RESOLUTION_BUTTONS:
            button.changeColor(SETTINGS_MOUSE_POS)
        FULLSCREEN_BUTTON.changeColor(SETTINGS_MOUSE_POS)
        EXIT_FULLSCREEN_BUTTON.changeColor(SETTINGS_MOUSE_POS)

        SETTINGS_BACK.update(screen)
        for button in RESOLUTION_BUTTONS:
            button.update(screen)
        FULLSCREEN_BUTTON.update(screen)
        EXIT_FULLSCREEN_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return "main_menu"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                    return "main_menu"

                for i, button in enumerate(RESOLUTION_BUTTONS):
                    if button.checkForInput(SETTINGS_MOUSE_POS):
                        # Change resolution
                        pygame.display.set_mode(RESOLUTIONS[i], pygame.FULLSCREEN if FULLSCREEN else 0)
                        screen = pygame.display.get_surface()  # Update the screen object
                        screen.fill(DARK_GREY)  # Clear screen after resolution change

                if FULLSCREEN_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    # Toggle fullscreen
                    FULLSCREEN = not FULLSCREEN
                    pygame.display.set_mode(
                        pygame.display.get_surface().get_size(),
                        pygame.FULLSCREEN if FULLSCREEN else 0
                    )
                    screen = pygame.display.get_surface()  # Update the screen object
                    screen.fill(DARK_GREY)  # Clear screen after toggling fullscreen

                if EXIT_FULLSCREEN_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    # Exit fullscreen mode
                    FULLSCREEN = False
                    pygame.display.set_mode(
                        pygame.display.get_surface().get_size(),
                        0  # Windowed mode
                    )
                    screen = pygame.display.get_surface()  # Update the screen object
                    screen.fill(DARK_GREY)  # Clear screen after exiting fullscreen

        pygame.display.update()
