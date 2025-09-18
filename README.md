# "Clash of Multiverse"

A pixel-art RPG-style turn-based strategy game.

## Table of contents
- [Contributors](#contributors)
- [Game overview](#game_overview)
- [Use](#use)
- [Rules](#rules)
- [Code architecture](#code_achitecture)
- [Obstacle](#obstacle)
- [Character](#character)

## Contributors
Students from Sorbonne Université Sciences as part of a pedagogical project in the Object Oriented Programming in Python teaching unit.
Master 1 -  Engineering for Health, Mechatronic Systems for Rehabilitation (M1-IPS SMR).

### List of contributors : 
- GUERIN Jacques: jacques.guerin@etu.sorbonne-universite.fr
- PORTENEUVE Margot: margot.porteneuve@etu.sorbonne-universite.fr
- ALAOUI MRANI Ahmed: ahmed.alaoui-mrani@etu.sorbonne-universite.fr

### University supervisors: 
- Louis ANNABI: louis.annabi@sorbonne-universite.fr
- Ramy ISKANDER, ramy.iskander@sorbonne-universite.fr

## Game overview


## Use
### Launch the game
To start the game, run the `menu.py` file. Pygame must be installed.

```bash
pip install pygame
```

Then launch the game with the next command :
```bash
python menu.py
```
Then press on the play button to launch a game or the infos button for more details
On the choose character screen, you must click on the different units to pick them for your team composition
Click on the discussion point to see mor informations about the character
To lauch the game, each player must peak 4 units

## Rules
-The goal is to destroy all ennemy units.
-Damage to allies is enabled
-Units cannot attack themselves
-If a unit move on a water tile, it will die immediatly and give the turn to the other player.
-All units have 3 active skills
-All units have a different passif skill

### Controls:
- **Navigation**: Use the mouse to navigate in the menu.
- **Movement**: Use the arrow keys to move the selected tile.
- **Action**: Press the `Space` key to confirm a move or apply the choosen skill.
- **Skills**: Choose a skill by pressing the number keys (`a`, `z` or ``.).
- **Quit**: Close the window to exit the game or press `Escape`.
- **Endgame**: At the end of a game, press any key to quit the game.

## Code Architecture
The game is organized into several Python files, each with a specific responsibility:

- **`menu.py`**: The main entry point of the game. It handles the display and game loop.
- **`game.py`**: Contains the game logic, such as managing player and enemy turns, and applying skills.
- **`unit.py`**: Defines the `Unit` class, which represents a unit on the field, with its health, attack, defense, and skills.
- **`environement.py`** : Define the different elements present in the environment to display them and generate their positions on the map using different class such as `Block` and `Environnement`.

### Description of Main Classes:
- **`Unit`**: Units have attributes like health, defense, attack, speed, and skills. They can move on the board and attack other units.

## Obstacle
There are 5 elements in the game environment: 
- Wall: A fixed block that cannot be crossed or passed over.
- Tree: A fixed block that cannot be crossed (like a wall).
- Water: Fixed block, if the character moves onto a water square, he dies instantly.
- Cactus: Fixed block, if the character positions himself on a square next to it (top, bottom, left, right), he loses -10 hit points. If the character lands on the cactus, he loses 50 points.
- Grass: Serves as soil, has no functionality.  

## Character
- Assassin : 200 Health Point, 100 Attack Damage, 50 Ability Power, 50 Armor, 50 Magic resist, 0.6 Armor penetration, 0 Magic penetration, 5 Movement Speed
Passif : Every time the Assassin kills a unit, it will gain 50 Attack damage
Skill 1 : A cut that deals 50 + AD * 1.8 physical damage
Skill 2 : A deep cut that deals 50 + AD * 1.2 with 60% armor penetration (better against tanky units)
Skill 3 : A magic enhanced cut that deals 50 + AD * 1.2 physical damage and AP * 1.5 magic damage

- Tower Knight : 800 HP, 50 AD, 50 AP, 200 AR, 200 MR, 0.3 Armor penetration, 0 Magic penetration, 2 MS
Passif : At the end of his turn, the Tower Knight regains 20 HP
Skill 1 : The Tower Knight hits the ground with his enormoous shield, dealing AD * 0.5 brut damage arpund him (brut means it ignore the target's resistance)
Skill 2 : The Tower Knight pierce the target with his lance dealing AD * 0.8 physical damage with 30% armor penetration (better against tanky units)
Skill 3 : The Tower Knight throw a magical lance that deals AP * 1.2 magic damage in a 3x3 zone

- Tank : 300 HP, 100 AD, 100 AP, 400 AR, 100 MR, 0.8 Armor penetration, 0.5 Magic penetration, 5 MS
Passif : If the Tank has less than half its hit points, it loses half it's armor and magic resist as well
Skill 1 : Shoot a Armor Piercing Fin Stabilised Discarded Shell (APFSDS) that deals 50 + self.AD * 1.2 physical damage with 80% armor penetration (extremely efficient against very well armored units)
Skill 2 : Shoot a High Explosif shell (HE) that deals AD * 1.2 physical damage in a 3x3 zone
Skill 3 : Shoot a  Magically Enhanced shell (ME) that deals AP * 0.5 magic damage with a 50% magic penetration

- Dragon : 1000 HP, 100 AD, 100 AP, 0 Armor, 100 Magic Resist, 0 Armor Ppenetration, 0.7 Magic penetration, 4 MS
Passif : If the Dragon has less than half its hit points, it loses 20 HP at the end of his turn
Skill 1 : the dragon uses its sharp claws to tear apart any unit around it dealing 100 + AD * 0.8 physical damage
Skill 2 : Throws a magical fireball dealing AP * 0.5 magic damage in  4x4 zone
Skill 3 : Shoot a laser at it's target dealing AP * 1.2 magic damage with a 70% magic resist penetration

- Ghost face : 200 HP, 100 AD, 50 AP, 50 Armor, 50 Magic resist, 0.4 Armor penetration, 0 magic pen, 4 MS
Passif : Deals AP * 0.2 brut damage around him with a range of 4 tiles
Skill 1 : Hit multiple times the target with it's sharp knife dealing AD * 0.4 each cut (the more cut he deals bigger is the probability that he miss and stop hiting the target)
Skill 2 : Throws a knife up to 5 times dealing AD * 0.4 each time
Skill 3 : A deep cut that deals 50 + AD * 1.2 with 80% armor penetration (better against tanky units)

