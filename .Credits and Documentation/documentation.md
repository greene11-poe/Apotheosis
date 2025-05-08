Project Description: Apotheosis will be a game similar to Slay the Spire which is a roguelike, turn based card game focused on ascending a tower of enemies and eventually reaching the summit. Cards must be synergistic and enemies will lead up to a boss encounter either ending the game or continuing with multiple acts/towers. Resting areas and merchants would be scattered among the ascent, offering players the chance to heal, improve their deck, and purchase new card options from vendors. Permanent deck upgrades can be earned through bosses, and one character will be available with multiple path options to choose from; these alter the weight and appearance rate of suitable cards to appear for your character.

Game concept: Turn based card game
Genre: Roguelike
Core Mechanics: Deck building, card synergies, merchants, bosses, card costs
    Mana: Card costs

Characters: Knight

    Knight:
        Default Attack: Strike
            Single target damage, low cost, higher card weight.
        Default Defense: Defend
            Adds an amount of Guard, which reduces damage from enemy attacks. More similar to an overshield.
        
        Attacks:
            Bash: Deals a medium amount of damage.
            Bludgeon: Deals a large amount of damage at a high mana cost.
            Cleave: Deals a medium amount of damage to all enemies.
            Iron Wave: Damages enemies and grants players a small amount of block.
            Pommel Strike: Deals high damage and draws 1 card.
            Twin Strike: Deals medium damage twice.
            Bloodletting: Grants mana in exchange for a small amount of health.

    Items:
        Potion: 
            Heals a small amount of health.
        
        Mana Potion:
            Restores a small amount of mana.

Levels: 1: Cave, 2: Forest, 3: Ruins, 4: Dungeon, 5: Castle Halls, 6: Castle Ramparts


# Week 2: 1/30/25
## Task: Setup github and create environment to begin coding.
Created github accounts, booted up vsCode and loaded environments. 
Found assets from baraltech, implemented main menu screen with play (displays map), options, and quit functions (ends program).
Changed font and introduced title screen: APOTHEOSIS
Implemented map for Play screen (WIP)

# Week 3: 2/06/25
## Task: Setup card mouse movement using event type comparisons: == pygame.MOUSEBUTTONDOWN:
Created move_object_by_mouse.py, successfully loaded dimensions and filled black screen. Unsuccessfully retrieved folders from assets/bash.png

# Week 4: 2/11/25
## Task: Repair main menu -> Play (map image)
Minor menu changes with dimensions and colors. Unsuccessfully repaired Play screen and map png import (must scale down image). Attempted to add quit functionality with ESC key with get.event(), must be fixed still.

# Week 4: 2/13/25
Minor menu changes with dimensions and colors.

# Week 5: 2/18/25
Implemented knight main character through piskel and a main menu background screen; using tower assets from https://www.vecteezy.com/free-vector/tower . 