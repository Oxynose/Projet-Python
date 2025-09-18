from plantuml import PlantUML
uml_code = """
@startuml

' Grouper les classes similaires pour réduire la largeur
package "Unités" {
    class Unit {
        - nom: str
        - x: int
        - y: int
        - PV: int
        - PV_max: int
        - AD: int
        - AP: int
        - AR: int
        - MR: int
        - PA: int
        - PR: int
        - MS: int
        - team: str
        - portee1: int
        - portee2: int
        - portee3: int
        - zone1: int
        - zone2: int
        - zone3: int
        + __init__(nom: str, x: int, y: int, PV: int, AD: int, AP: int, AR: int, MR: int, PA: int, PR: int, MS: int, team: str, portee1: int, portee2: int, portee3: int, zone1: int, zone2: int, zone3: int)
        + barre_PV(screen)
        + portee_competence(competence: str): set
        + Accessible_case(liste_perso1: list, liste_perso2: list, grid: list): set
        + move(new_x: int, new_y: int)
        + draw(screen)
        + passif(target)
        + Compétence_1(target)
        + Compétence_2(target)
        + Compétence_3(target)
    }

    class Assassin {
        + __init__(x: int, y: int, team: str)
        + draw(screen)
        + passif(target)
        + Compétence_1(target)
        + Compétence_2(target)
        + Compétence_3(target)
    }

    class TowerKnight {
        + __init__(x: int, y: int, team: str)
        + draw(screen)
        + passif(target)
        + Compétence_1(target)
        + Compétence_2(target)
        + Compétence_3(target)
    }

    class Tank {
        + __init__(x: int, y: int, team: str)
        + draw(screen)
        + passif(target)
        + Compétence_1(target)
        + Compétence_2(target)
        + Compétence_3(target)
    }

    class Ghost {
        + __init__(x: int, y: int, team: str)
        + draw(screen)
        + passif(target)
        + Compétence_1(x: int, y: int, target)
        + Compétence_2(x: int, y: int, target)
        + Compétence_3()
    }

    class Dragon {
        + __init__(x: int, y: int, team: str)
        + draw(screen)
        + passif()
        + Compétence_1(x: int, y: int, target)
        + Compétence_2(x: int, y: int, target)
        + Compétence_3(x: int, y: int, target)
    }

    Unit <|-- Assassin : hérite de
    Unit <|-- TowerKnight : hérite de
    Unit <|-- Tank : hérite de
    Unit <|-- Ghost : hérite de
    Unit <|-- Dragon : hérite de
}

package "Environnement" {
    class Block {
        - x: int
        - y: int
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class MUR {
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class HERBE {
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class TREE {
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class EAU {
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class CACTUS {
        + __init__(x: int, y: int)
        + draw(screen)
    }

    class Environnement {
        + __init__() 
        + generate_environnement(): list
    }

    Block <|-- MUR : hérite de
    Block <|-- HERBE : hérite de
    Block <|-- TREE : hérite de
    Block <|-- EAU : hérite de
    Block <|-- CACTUS : hérite de

    Environnement "1" -- "*" Block : génère
}

package "Jeu" {
    class Game {
        - screen: pygame.Surface
        - player_units: list[Unit]
        - enemy_units: list[Unit]
        - grid: list[list[bool]]
        + __init__(screen)
        + start(player_units: list[Unit], enemy_units: list[Unit])
        + run_game_loop()
        + handle_player1_turn()
        + handle_player2_turn()
        + flip_display(selected_unit: Unit, accessible_case: set, has_acted: bool, accessible_skill_cases: set, skill_used: bool, zone: set)
        + display_skills()
        + display_move_unit()
        + Fin(): bool
        + wait_for_input()
    }
    
    Game --> Unit : gère
    Game --> Environnement : utilise
}

@enduml
"""
# Sauvegarde du code UML dans un fichier
with open("game_diagram.uml", "w") as file:
    file.write(uml_code)

# Création de l'instance PlantUML et génération du diagramme
plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')
plantuml.processes_file('game_diagram.uml')  # Génère le diagramme à partir du fichier UML