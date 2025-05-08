import pygame, sys
from button import Button
from asset_loader import *
from screen_transition import *
from asset_loader import MAIN_MENU_OST  # Import main menu soundtrack

def main_menu(screen, render_only=False):
    # Use a specific channel for the main menu soundtrack
    main_menu_channel = pygame.mixer.Channel(0)  # Assign channel 0 for the main menu OST
    if not main_menu_channel.get_busy():  # Check if the channel is already playing
        main_menu_channel.play(MAIN_MENU_OST, loops=-1)  # Play and loop the soundtrack

    buttons = [
        Button(pygame.Rect(860, 700, 100, 50), (860, 700), "PLAY", get_font(72), "Black", "White", 10),
        Button(pygame.Rect(860, 850, 100, 50), (860, 850), "SETTINGS", get_font(72), "Black", "White", 10),
        Button(pygame.Rect(860, 1000, 100, 50), (860, 1000), "QUIT", get_font(72), "Black", "White", 10),
        # Button(pygame.Rect(1400, 700, 100, 50), (1400, 700), "TEST STAGE 5", get_font(50), "Red", "White", 10)
    ]

    # Render the main menu content
    screen.blit(MAIN_MENU_BACKGROUND, (0, 0))
    screen.blit(MAINMENUKNIGHT, (-200, 300))

    # Revert the title text "APOTHEOSIS" to its original position
    MENU_TEXT = get_font(160).render("A P O T H E O S I S", True, DARK_GOLD)
    screen.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(960, 140)))

    for button in buttons:
        button.update(screen)

    pygame.display.update()

    # If render_only is True, return immediately after rendering
    if render_only:
        return

    selected_button_index = 0
    mouse_over_button = False  # Track if mouse is over any button.

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        mouse_over_button = False  # Reset each frame.

        # Update button colors based on selection and mouse hover
        for i, button in enumerate(buttons):
            if button.checkForInput(MENU_MOUSE_POS):
                button.text = button.font.render(button.text_input, True, "White")  # Highlight mouse hover
                selected_button_index = i  # Update selected index to match mouse.
                mouse_over_button = True
            elif i == selected_button_index and not mouse_over_button:
                button.text = button.font.render(button.text_input, True, "White")  # Highlight selected
            else:
                button.text = button.font.render(button.text_input, True, "Black")  # Default color
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fade_transition(screen, 1000, mode="to_black")  # Smooth fade to black
                main_menu_channel.stop()  # Stop the main menu soundtrack
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected_button_index = (selected_button_index - 1) % len(buttons)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected_button_index = (selected_button_index + 1) % len(buttons)
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Simulate button click
                    if selected_button_index == 0:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "play"  # Return control to the main driver
                    elif selected_button_index == 1:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "settings"  # Return control to the main driver
                    elif selected_button_index == 2:
                        fade_transition(screen, 1000, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        pygame.quit()
                        sys.exit()
                    elif selected_button_index == 3:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "main_menu"  # Corrected to return "main_menu"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[selected_button_index].checkForInput(MENU_MOUSE_POS):
                    if selected_button_index == 0:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "play"  # Return control to the main driver
                    elif selected_button_index == 1:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "settings"  # Return control to the main driver
                    elif selected_button_index == 2:
                        fade_transition(screen, 1000, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        pygame.quit()
                        sys.exit()
                    elif selected_button_index == 3:
                        fade_transition(screen, 500, mode="to_black")  # Fade to black
                        main_menu_channel.stop()  # Stop the main menu soundtrack
                        return "main_menu"  # Corrected to return "main_menu"

        pygame.display.update()