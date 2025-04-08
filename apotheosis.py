import pygame
from main_menu import main_menu
from play_menu import play
from settings_menu import settings
from screen_transition import fade_transition  # Import the updated function

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    pygame.display.set_caption("Apotheosis")
    # Start with a black screen
    SCREEN.fill((0, 0, 0))
    pygame.display.update()

    # Render the main menu content first (in render-only mode)
    main_menu(SCREEN, render_only=True)

    # Capture the pre-rendered main menu content
    main_menu_content = SCREEN.copy()

    # Set the screen back to black
    SCREEN.fill((0, 0, 0))
    pygame.display.update()

    # Fade out of black to reveal the main menu
    fade_transition(SCREEN, 1000, mode="out_of_black", content=main_menu_content) # COMMENT FOR DEBUGGING

    # Transition to the main menu
    game_state = main_menu(SCREEN)

    # Main game loop
    while True:
        if game_state == "main_menu":
            # Render the main menu and handle transitions
            game_state = main_menu(SCREEN)
        elif game_state == "play":
            # Fade to black before transitioning to the play screen
            fade_transition(SCREEN, 500, mode="to_black") # COMMENT FOR DEBUGGING
            game_state = play(SCREEN)
            # Fade out of black after transitioning to the play screen
            fade_transition(SCREEN, 500, mode="out_of_black")
        elif game_state == "settings":
            # Fade to black before transitioning to the settings screen
            fade_transition(SCREEN, 500, mode="to_black")
            # Pre-render the settings screen content
            settings(SCREEN, render_only=True)
            # Fade out of black after transitioning to the settings screen
            fade_transition(SCREEN, 500, mode="out_of_black")
            # Enter the settings screen main loop
            game_state = settings(SCREEN)

        pygame.display.update()

if __name__ == "__main__":
    main()