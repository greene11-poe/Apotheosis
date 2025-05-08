import pygame

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def fade_transition(screen, duration, mode="both", content=None):
    """
    Handles fade transitions: fade to black, fade out of black, or both.
    
    Args:
        screen: The pygame screen surface.
        duration: Total duration of the fade (in milliseconds).
        mode: "to_black" for fade to black, "out_of_black" for fade out of black, or "both".
        content: Optional surface to reveal during the fade-out transition.
    """
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))  # Black overlay
    steps = 100
    delay_per_step = duration / steps

    if mode in ("to_black", "both"):
        # Fade to black (increase alpha from 0 to 255)
        for i in range(steps + 1):
            alpha = int(255 * (i / steps))  # Gradually increase alpha
            fade_surface.set_alpha(alpha)
            if content:
                screen.blit(content, (0, 0))  # Redraw the pre-rendered content
            screen.blit(fade_surface, (0, 0))  # Overlay the black surface
            pygame.display.update()
            pygame.time.delay(int(delay_per_step))

    if mode in ("out_of_black", "both"):
        # Fade out of black (decrease alpha from 255 to 0)
        for i in range(steps + 1):
            alpha = int(255 * (1 - i / steps))  # Gradually decrease alpha
            fade_surface.set_alpha(alpha)
            if content:
                screen.blit(content, (0, 0))  # Redraw the pre-rendered content
            else:
                screen.fill((0, 0, 0))  # Ensure the screen is black if no content is provided
            screen.blit(fade_surface, (0, 0))  # Overlay the black surface
            pygame.display.update()
            pygame.time.delay(int(delay_per_step))