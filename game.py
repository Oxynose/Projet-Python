import pygame
# Importation élément de l'environnement
from environnement import *
# Importation élément pour personnages
from unit import *
from assassin import *
from tower_knight import *
from tank import *
from ghost import *
from dragon import Dragon

# IMPORTATION IMAGE UTILE
Game_over = pygame.image.load("assets/Gameover.png")
Game_over = pygame.transform.scale(Game_over, (WIDTH // 2, HEIGHT // 2))
Game_over_rect = Game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centrer l'image  
You_win = pygame.image.load("assets/Youwin.png")
You_win = pygame.transform.scale(You_win, (WIDTH // 2, HEIGHT // 2))
You_win_rect = You_win.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Centrer l'image



class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    grid : list[list[bool]]
        La grille représentant les murs.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = []  # Liste pour les unités du joueur
        self.enemy_units = []   # Liste pour les unités ennemies
        
        # AFFICAGE SUR LA GRILLE
        self.grid=Environnement.generate_environnement()
    
    def start(self, player_units, enemy_units):
        print("Démarrage du jeu avec les unités sélectionnées...")
        print("Player 1 units:", player_units)
        print("Player 2 units:", enemy_units)
        self.player_units = player_units
        self.enemy_units = enemy_units
        self.run_game_loop()  # Appeler run_game_loop après la configuration

    def run_game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            # Tour du joueur 1
            self.handle_player1_turn()
            if self.Fin():  # Vérifier si le jeu est terminé
                break

            # Tour du joueur 2
            self.handle_player2_turn()
            if self.Fin():  # Vérifier à nouveau après le tour du joueur 2
                break

            pygame.display.flip()  # Mettre à jour l'écran

    # FONCTION POUR GERER LE DEPLACEMENT DU JOUEUR 1
    def handle_player1_turn(self):
        """Tour du joueur 1"""
        for selected_unit in self.player_units:

            has_acted = False # N'a pas encore jouer
            choice = False #n'a pas encore choisi
            selected_unit.is_selected = True # Est sélectionner

            # Calcul des cases accessibles autour de l'unité selon sa vitesse de mouvement
            accessible_cases = selected_unit.Accessible_case(self.player_units,self.enemy_units,self.grid)
            
            # Initialisation de la case bleue à la position de l'unité sélectionnée
            selected_unit.selection_dx = selected_unit.x
            selected_unit.selection_dy = selected_unit.y

            # AFFICHE LA SELECTION
            self.flip_display(selected_unit, accessible_case=accessible_cases, has_acted=has_acted, accessible_skill_cases=None, skill_used=True, zone=None)
            
            # Choisir la compétence
            choice = False
            accessible_skill_cases = []
            zone = []

            # Déplacement de l'unité
            while not has_acted:

                # Important : gérer les événements Pygame
                for event in pygame.event.get():
                    # Fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        # Déplacement de la case sélectionnée avec les touches directionnelles
                        if event.key == pygame.K_LEFT:
                            if (selected_unit.selection_dx - 1, selected_unit.selection_dy) in accessible_cases:
                                selected_unit.selection_dx -= 1
                        elif event.key == pygame.K_RIGHT:
                            if (selected_unit.selection_dx + 1, selected_unit.selection_dy) in accessible_cases:
                                selected_unit.selection_dx += 1
                        elif event.key == pygame.K_UP:
                            if (selected_unit.selection_dx, selected_unit.selection_dy - 1) in accessible_cases:
                                selected_unit.selection_dy -= 1
                        elif event.key == pygame.K_DOWN:
                            if (selected_unit.selection_dx, selected_unit.selection_dy + 1) in accessible_cases:
                                selected_unit.selection_dy += 1

                        # AFFICHE LES NOUVEAUX ELEMENTS
                        self.flip_display(selected_unit, accessible_cases, has_acted=False, accessible_skill_cases=None, skill_used=None, zone=None)

                        # Si "Espace" est pressée, déplacer l'unité
                        if event.key == pygame.K_SPACE:

                            # Vérifier si l'unité est sur une case d'eau après le déplacement
                            for obj in self.grid:

                                if isinstance(obj, EAU) and obj.x == selected_unit.selection_dx and obj.y == selected_unit.selection_dy:
                                        self.player_units.remove(selected_unit) # Mort = enlève de la liste
                                        return # Personnage mort -> Laisse la main à l'adversaire

                                elif isinstance(obj, CACTUS):
                                    # Si le personnage est SUR le cactus
                                    if obj.x == selected_unit.selection_dx and obj.y ==selected_unit.selection_dy:
                                        selected_unit.PV -= 50 # Enleve 50 PV au personnage
                                        
                                    # Si le personnage est sur les COTES du cactus (haut, bas, gauche, droite)
                                    elif abs(obj.x - selected_unit.selection_dx) + abs(obj.y - selected_unit.selection_dy) == 1:
                                        selected_unit.PV -= 10 # Enleve 10 PV au personnage

                                # CONDITION SI PERSONNAGE EST MORT
                                if selected_unit.PV <= 0:
                                    self.player_units.remove(selected_unit)
                                    return
            
                            # Déplacer l'unité à la position de la case bleue
                            selected_unit.move(selected_unit.selection_dx, selected_unit.selection_dy)
                            has_acted = True # Le joueur à jouer
                            break   

            # AFFICHE LA NOUVELLE POSITION
            self.flip_display(selected_unit, accessible_case=False, has_acted=True, accessible_skill_cases=False, skill_used=False, zone=False)

            # Choisir la compétence
            
            while not choice :

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            accessible_skill_cases = selected_unit.portee_competence("competence1")  # Utilise la portée de la compétence 1
                            zone = selected_unit.zone1
                            selected_skill = "competence1"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x        #IL FAUT IMPERATIVEMENT REINITIALISER LA POSITION DE LA CASE BLEUE
                            selected_unit.selection_dy = selected_unit.y        #POUR EVITER DES GLITCHS

                        elif event.key == pygame.K_z:
                            accessible_skill_cases = selected_unit.portee_competence("competence2")  # Utilise la portée de la compétence 2
                            zone = selected_unit.zone2
                            selected_skill = "competence2"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x
                            selected_unit.selection_dy = selected_unit.y
                        
                        elif event.key == pygame.K_e:

                            accessible_skill_cases = selected_unit.portee_competence("competence3")  # Utilise la portée de la compétence 3
                            zone = selected_unit.zone3
                            selected_skill = "competence3"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x
                            selected_unit.selection_dy = selected_unit.y

                        elif event.key == pygame.K_r:            #Pour sauter le tour si le joueur le veut
                            choice = True
                            break

                        if accessible_skill_cases :   
                            
                            if event.key == pygame.K_LEFT:
                                if (selected_unit.selection_dx - 1, selected_unit.selection_dy) in accessible_skill_cases:
                                    selected_unit.selection_dx -= 1
                            elif event.key == pygame.K_RIGHT:
                                if (selected_unit.selection_dx + 1, selected_unit.selection_dy) in accessible_skill_cases:
                                    selected_unit.selection_dx += 1
                            elif event.key == pygame.K_UP:
                                if (selected_unit.selection_dx, selected_unit.selection_dy - 1) in accessible_skill_cases:
                                    selected_unit.selection_dy -= 1
                            elif event.key == pygame.K_DOWN:
                                if (selected_unit.selection_dx, selected_unit.selection_dy + 1) in accessible_skill_cases:
                                    selected_unit.selection_dy += 1
                            # Nouveau element
                            self.flip_display(selected_unit, accessible_case=False, has_acted=has_acted, accessible_skill_cases=accessible_skill_cases, skill_used=False, zone=zone)

                            # Si "Espace" est pressée, déplacer l'unité
                            if event.key == pygame.K_SPACE: 
                                    # Vérifier si la case sélectionnée correspond à l'unité ciblée
                                    target = None
                                    self_target = None
                                    for unit in self.enemy_units + self.player_units:
                                        if (selected_unit.selection_dx, selected_unit.selection_dy) == (unit.x, unit.y):
                                            if unit != selected_unit:
                                                target = unit
                                                break
                                            if unit == selected_unit:
                                                self_target = unit
                                                break

                                    if target and selected_skill and not (isinstance(selected_unit, Tank) and selected_skill == "competence2") and not (isinstance(selected_unit, Tank) and selected_skill == "competence3") and not (isinstance(selected_unit, Dragon) and selected_skill == "competence1") and not (isinstance(selected_unit, Dragon) and selected_skill == "competence2"): 
                                    # Appliquer la compétence en fonction de la compétence choisie
                                        if selected_skill == "competence1":

                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)
                                                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                                                        
                                        elif selected_skill == "competence2":

                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)     
                                                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        elif selected_skill == "competence3": 
                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)

                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        choice = True
                                        break

                                    elif self_target and selected_skill == "competence1" and isinstance(selected_unit, Tower_Knight):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)     
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Tower Knight a fait {selected_unit.AD * 0.5:.2f} de dégâts autour de lui")
                                        choice = True
                                        break

                                    elif self_target and selected_skill == "competence1" and isinstance(selected_unit, Dragon):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)     

                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Dragon a fait des dégâts physiques autour de lui")
                                        choice = True
                                        break

                                    elif selected_skill == "competence2" and isinstance(selected_unit, Dragon):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Dragon a fait des dégâts en zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence3" and isinstance(selected_unit, Tower_Knight):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Tower Knight a fait des dégâts en zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence2" and isinstance(selected_unit, Tank):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target.team == 'enemy':
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Tank a fait des dégâts physiques de zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence3" and isinstance(selected_unit, Tank):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Tank a fait des dégâts magiques transperçant de zone")
                                        choice = True
                                        break

            if isinstance(selected_unit, Ghost):                           #Activation du passif de Ghost
                for target in self.enemy_units :
                    selected_unit.passif(target)
                    #CONDITION SI PERSONNAGE EST MORT
                    if target.PV <= 0:
                        if target in self.enemy_units:
                            self.enemy_units.remove(target)
                            return
                        elif target in self.player_units:
                            self.player_units.remove(target)
                            return

            elif isinstance(selected_unit, Tower_Knight):              #Activation du passif de TK
                if selected_unit.team == "player":    
                    target = None
                    selected_unit.passif(target)
            
            elif isinstance(selected_unit, Tank):              #Activation du passif de Tank
                if selected_unit.team == "player":    
                    target = None
                    selected_unit.passif()
            elif isinstance(selected_unit, Dragon):              #Activation du passif de Dragon
                if selected_unit.team == "player":    
                    target = None
                    selected_unit.passif()
            
            
            selected_unit.is_selected = False
            # Tour terminé pour cette unité, passer à la suivante
            self.flip_display(selected_unit=True, accessible_case=False, has_acted=has_acted, accessible_skill_cases=False, skill_used=True, zone=False)
            
                
    def handle_player2_turn(self):
        """Tour de l'autre joueur"""

        for selected_unit in self.enemy_units:
            has_acted = False
            selected_unit.is_selected = True

            # Calcul des cases accessibles autour de l'unité selon sa vitesse de mouvement
            accessible_cases = selected_unit.Accessible_case(self.player_units,self.enemy_units,self.grid)
            
            # Initialisation de la case bleue à la position de l'unité sélectionnée
            selected_unit.selection_dx = selected_unit.x
            selected_unit.selection_dy = selected_unit.y

            self.flip_display(selected_unit, accessible_case=accessible_cases, has_acted=has_acted, accessible_skill_cases=None, skill_used=True, zone=None)
            
            # Déplacement de l'unité
            while not has_acted:

                # Important : gérer les événements Pygame
                for event in pygame.event.get():
                    # Fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        # Déplacement de la case sélectionnée avec les touches directionnelles
                        if event.key == pygame.K_LEFT:
                            if (selected_unit.selection_dx - 1, selected_unit.selection_dy) in accessible_cases:
                                selected_unit.selection_dx -= 1
                        elif event.key == pygame.K_RIGHT:
                            if (selected_unit.selection_dx + 1, selected_unit.selection_dy) in accessible_cases:
                                selected_unit.selection_dx += 1
                        elif event.key == pygame.K_UP:
                            if (selected_unit.selection_dx, selected_unit.selection_dy - 1) in accessible_cases:
                                selected_unit.selection_dy -= 1
                        elif event.key == pygame.K_DOWN:
                            if (selected_unit.selection_dx, selected_unit.selection_dy + 1) in accessible_cases:
                                selected_unit.selection_dy += 1

                        # Afficher la sélection
                        self.flip_display(selected_unit, accessible_case=accessible_cases, has_acted=has_acted, accessible_skill_cases=None, skill_used=True, zone=None)

                        # Si "Espace" est pressée, déplacer l'unité
                        if event.key == pygame.K_SPACE:

                            # SI PERSONNAGE SUR EAU OU CACTUS
                            for obj in self.grid:
                                # Si sur eau    
                                if isinstance(obj, EAU) and obj.x == selected_unit.selection_dx and obj.y == selected_unit.selection_dy:
                                    self.enemy_units.remove(selected_unit) # Mort = Enlève personnage de la liste
                                    return # Personnage mort -> Laisse la main à l'adversaire
                                # Si sur un cactus
                                elif isinstance(obj, CACTUS):
                                    # Si le personnage est SUR le cactus
                                    if obj.x == selected_unit.selection_dx and obj.y ==selected_unit.selection_dy:
                                        selected_unit.PV -= 50 # Enleve 50 PV au personnage
                                        
                                    # Si le personnage est sur les COTES du cactus (haut, bas, gauche, droite)
                                    elif abs(obj.x - selected_unit.selection_dx) + abs(obj.y - selected_unit.selection_dy) == 1:
                                        selected_unit.PV -= 10 # Enleve 10 PV au personnage
                                
                                # CONDITION SI PERSONNAGE EST MORT
                                if selected_unit.PV <=0:
                                    self.enemy_units.remove(selected_unit) # Mort = Enlève personnage de la liste
                                    return # Personnage mort -> Laisse la main à l'adversaire

                            # Déplacer l'unité à la position de la case bleue
                            selected_unit.move(selected_unit.selection_dx, selected_unit.selection_dy)
                            has_acted = True
                            break
             # Afficher la sélection               
            self.flip_display(selected_unit, accessible_case=False, has_acted=True, accessible_skill_cases=False, skill_used=False, zone=False)

            # CHOIX COMPETENCE
             # Choisir la compétence
            accessible_skill_cases = []
            zone = []
            choice = False

            while not choice :

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            accessible_skill_cases = selected_unit.portee_competence("competence1")  # Utilise la portée de la compétence 1
                            zone = selected_unit.zone1
                            selected_skill = "competence1"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x        #IL FAUT IMPERATIVEMENT REINITIALISER LA POSITION DE LA CASE BLEUE
                            selected_unit.selection_dy = selected_unit.y        #POUR EVITER DES GLITCHS

                        elif event.key == pygame.K_z:
                            accessible_skill_cases = selected_unit.portee_competence("competence2")  # Utilise la portée de la compétence 2
                            zone = selected_unit.zone2
                            selected_skill = "competence2"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x
                            selected_unit.selection_dy = selected_unit.y

                        elif event.key == pygame.K_e:
                            accessible_skill_cases = selected_unit.portee_competence("competence3")  # Utilise la portée de la compétence 3
                            zone = selected_unit.zone3
                            selected_skill = "competence3"  # Enregistrer la compétence choisie
                            selected_unit.selection_dx = selected_unit.x
                            selected_unit.selection_dy = selected_unit.y

                        elif event.key == pygame.K_r:            #Pour sauter le tour si le joueur le veut
                            choice = True
                            break

                        if accessible_skill_cases :   
                            if event.key == pygame.K_LEFT:
                                if (selected_unit.selection_dx - 1, selected_unit.selection_dy) in accessible_skill_cases:
                                    selected_unit.selection_dx -= 1
                            elif event.key == pygame.K_RIGHT:
                                if (selected_unit.selection_dx + 1, selected_unit.selection_dy) in accessible_skill_cases:
                                    selected_unit.selection_dx += 1
                            elif event.key == pygame.K_UP:
                                if (selected_unit.selection_dx, selected_unit.selection_dy - 1) in accessible_skill_cases:
                                    selected_unit.selection_dy -= 1
                            elif event.key == pygame.K_DOWN:
                                if (selected_unit.selection_dx, selected_unit.selection_dy + 1) in accessible_skill_cases:
                                    selected_unit.selection_dy += 1

                            # Afficher la sélection
                            self.flip_display(selected_unit=selected_unit, accessible_case=False, has_acted=has_acted, accessible_skill_cases=accessible_skill_cases, skill_used=False, zone=zone)

                            
                            # Si "Espace" est pressée, déplacer l'unité
                            if event.key == pygame.K_SPACE: 
                                    # Vérifier si la case sélectionnée correspond à l'unité ciblée
                                    target = None
                                    self_target = None
                                    for unit in self.enemy_units + self.player_units:
                                        if (selected_unit.selection_dx, selected_unit.selection_dy) == (unit.x, unit.y):
                                            if unit != selected_unit:
                                                target = unit
                                                break
                                            if unit == selected_unit:
                                                self_target = unit
                                                break

                                    if target and selected_skill and not (isinstance(selected_unit, Tower_Knight) and selected_skill == "competence3") and not (isinstance(selected_unit, Tank) and selected_skill == "competence2") and not (isinstance(selected_unit, Tank) and selected_skill == "competence3") and not (isinstance(selected_unit, Dragon) and selected_skill == "competence1") and not (isinstance(selected_unit, Tank) and selected_skill == "competence2") and not (isinstance(selected_unit, Tank) and selected_skill == "competence3") and not (isinstance(selected_unit, Dragon) and selected_skill == "competence1") and not (isinstance(selected_unit, Dragon) and selected_skill == "competence2"): 
                                    # Appliquer la compétence en fonction de la compétence choisie
                                        if selected_skill == "competence1":

                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)
                                                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return                                            
                                        
                                        elif selected_skill == "competence2":

                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)     
                                                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        elif selected_skill == "competence3": 

                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)
                                                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        choice = True
                                        break

                                    elif self_target and selected_skill == "competence1" and isinstance(selected_unit, Tower_Knight):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)                                   
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                        print(f"Le Tower Knight a fait {selected_unit.AD * 0.5:.2f} de dégâts autour de lui")
                                        choice = True
                                        break
                                    
                                    elif self_target and selected_skill == "competence1" and isinstance(selected_unit, Dragon):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_1(selected_unit.selection_dx, selected_unit.selection_dy, target)     

                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Dragon a fait des dégâts physiques autour de lui")
                                        choice = True
                                        break

                                    elif selected_skill == "competence2" and isinstance(selected_unit, Dragon):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                                
                                        print(f"Le Dragon a fait des dégâts en zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence3" and isinstance(selected_unit, Tower_Knight):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                        print(f"Le Tower Knight a fait des dégâts en zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence2" and isinstance(selected_unit, Tank):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_2(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                        print(f"Le Tank a fait des dégâts physiques de zone")
                                        choice = True
                                        break

                                    elif selected_skill == "competence3" and isinstance(selected_unit, Tank):
                                        for target in self.enemy_units + self.player_units :
                                            selected_unit.Compétence_3(selected_unit.selection_dx, selected_unit.selection_dy, target)                                
                                            #CONDITION SI PERSONNAGE EST MORT
                                            if target.PV <= 0:
                                                if target in self.enemy_units:
                                                    self.enemy_units.remove(target)
                                                    return
                                                elif target in self.player_units:
                                                    self.player_units.remove(target)
                                                    return
                                        print(f"Le Tank a fait des dégâts magiques transperçant de zone")
                                        choice = True
                                        break

            if isinstance(selected_unit, Ghost):                           #Activation du passif de Ghost
                for target in self.player_units :
                    selected_unit.passif(target)
                    #CONDITION SI PERSONNAGE EST MORT
                    if target.PV <= 0:
                        if target in self.enemy_units:
                            self.enemy_units.remove(target)
                            return
                        elif target in self.player_units:
                            self.player_units.remove(target)
                            return

            elif isinstance(selected_unit, Tower_Knight):              #Activation du passif de TK
                if selected_unit.team == "enemy":    
                    target = None
                    selected_unit.passif(target)

            elif isinstance(selected_unit, Tank):              #Activation du passif de Tank
                if selected_unit.team == "enemy":    
                    target = None
                    selected_unit.passif()

            elif isinstance(selected_unit, Dragon):              #Activation du passif de Dragon
                if selected_unit.team == "enemy":    
                    target = None
                    selected_unit.passif()

            selected_unit.is_selected = False
            # Tour terminé pour cette unité, passer à la suivante
            self.flip_display(selected_unit=True, accessible_case=False, has_acted=has_acted, accessible_skill_cases=False, skill_used=True, zone=False)
            
    # AFFICHAGE COMPETENCE
    def display_skills(self):
        """
        Affiche les compétences disponibles en haut de la fenêtre avec leurs numéros respectifs.
        """
        # Police
        pygame.font.init()
        font = pygame.font.SysFont('tt rounds neue', WIDTH//40)

        # Définir le texte pour chaque compétence
        skill_text_1 = "A: Compétence 1"
        skill_text_2 = "Z: Compétence 2"
        skill_text_3 = "E: Compétence 3"
        skill_text_4 = "R: Passer"
    
        # Créer les surfaces de texte
        skill_surface_1 = font.render(skill_text_1, True, BLACK)  # Texte en noir
        skill_surface_2 = font.render(skill_text_2, True, BLACK)
        skill_surface_3 = font.render(skill_text_3, True, BLACK)
        skill_surface_4 = font.render(skill_text_4, True, BLACK)

        position_1 = (10*WIDTH/12, WIDTH//40)  # Un peu à gauche
        position_2 = (10*WIDTH/12, WIDTH*2//40)  # Au centre
        position_3 = (10*WIDTH/12, WIDTH*3//40)  # Un peu à droite
        position_4 = (10*WIDTH/12, WIDTH*4//40)  # Un peu à droite
    
    
        # Afficher les compétences sur l'écran
        self.screen.blit(skill_surface_1, position_1)
        self.screen.blit(skill_surface_2, position_2)
        self.screen.blit(skill_surface_3, position_3)
        self.screen.blit(skill_surface_4, position_4)

    def display_move_unit(self):
        """
        Affiche les compétences disponibles en haut de la fenêtre avec leurs numéros respectifs.
        """
        # Police
        pygame.font.init()
        font = pygame.font.SysFont('tt rounds neue', WIDTH//35)

        # Définir le texte pour chaque compétence
        move_text_1 = "Déplacer l'unité"
        
        # Créer les surfaces de texte
        move_surface_1 = font.render(move_text_1, True, BLACK)  # Texte en noir

        position_1 = (10*WIDTH/12, WIDTH//40)  # Un peu à gauche
        
        # Afficher les compétences sur l'écran
        self.screen.blit(move_surface_1, position_1)
 
    
    def flip_display(self, selected_unit, accessible_case, has_acted, accessible_skill_cases, skill_used, zone):
        """Affiche la grille avec les éléments du jeu."""
        # Affiche la grille
        self.screen.fill(BLACK)

        # Créer une surface transparente pour la case
        jaune_clair = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Surface avec alpha
        jaune_clair.fill(YELLOWA)  # Remplir avec une couleur jaune et alpha=128 (translucide)

        # Créer une surface bleue translucide pour les cases bleues
        case_bleu_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)  # Surface avec alpha
        case_bleu_surface.fill(BLUEA)  # Remplir avec une couleur bleue et alpha=128 (translucide)
        
        # Afficher les murs
        for mur in self.grid:
            mur.draw(self.screen)  # Dessine chaque mur

        # Afficher les cases accessibles pour de déplacement en jaune
        if accessible_case:
            for case in accessible_case:
                # Dessiner la case translucide
                self.screen.blit(jaune_clair, (case[0] * CELL_SIZE, case[1] * CELL_SIZE))

        # Afficher les cases accessibles pour les compétences en jaune
        if accessible_skill_cases:
            for kase in accessible_skill_cases:
                # Dessiner la case translucider
                self.screen.blit(jaune_clair, (kase[0] * CELL_SIZE, kase[1] * CELL_SIZE))  

        if skill_used == False and selected_unit :
            # Créer une surface bleue translucide pour les cases bleues
            aoe = pygame.Surface((CELL_SIZE * (zone*2+1), CELL_SIZE * (zone*2+1)), pygame.SRCALPHA)  # Surface avec alpha   * (zone*2+1)
            aoe.fill(BLUEA)  # Remplir avec une couleur bleue et alpha=128 (translucide)
 
            # Calculer la position pour centrer la surface
            x_centered = (selected_unit.selection_dx * CELL_SIZE) + (CELL_SIZE // 2) - (aoe.get_width() // 2)
            y_centered = (selected_unit.selection_dy * CELL_SIZE) + (CELL_SIZE // 2) - (aoe.get_height() // 2)

            # Afficher la surface au centre de la cellule
            self.screen.blit(aoe, (x_centered, y_centered))

        # Afficher les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)  # Dessine chaque unité
            unit.barre_PV(self.screen)  # Affiche la barre de vie
        pygame.display.flip()

        # Afficher l'unité sélectionnée en jaune, les unités ennemies en rouge et les alliés en vert
        if selected_unit:
            for unit in self.enemy_units:
                pygame.draw.rect(self.screen, RED, (unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), WIDTH//400)
            for unit in self.player_units:
                pygame.draw.rect(self.screen, GREEN, (unit.x * CELL_SIZE, unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), WIDTH//400)
            if selected_unit in (self.player_units + self.enemy_units):
                pygame.draw.rect(self.screen, YELLOW, (selected_unit.x * CELL_SIZE, selected_unit.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), WIDTH//400)   

        # Afficher la case sélectionnée en bleu pour le déplacement
        if has_acted == False and selected_unit :
            # Position du rectangle sélectionné
            selection_rect = pygame.Rect(selected_unit.selection_dx * CELL_SIZE, selected_unit.selection_dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Vérifier si une unité est présente sur cette case
            is_occupied = False
            for unit in self.player_units + self.enemy_units:
                if unit.x == selected_unit.selection_dx and unit.y == selected_unit.selection_dy:
                    is_occupied = True
                    break

            # Si l'unité est sur cette case, dessiner un rectangle creux
            if is_occupied:
                pygame.draw.rect(self.screen, BLUE, selection_rect, WIDTH//400)  # Rectangle creux (épaisseur de WIDTH//400 pixels)
            else:
                self.screen.blit(case_bleu_surface, (selected_unit.selection_dx * CELL_SIZE, selected_unit.selection_dy * CELL_SIZE))  # Dessiner la case noire translucide pleine

        #Afficher les zones de dégât des compétences
        if skill_used == False and selected_unit :
            # Position du rectangle sélectionné
            selection_rect = pygame.Rect(selected_unit.selection_dx * CELL_SIZE, selected_unit.selection_dy * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Vérifier si une unité est présente sur cette case
            is_occupied = False
            for unit in self.player_units + self.enemy_units:
                if unit.x == selected_unit.selection_dx and unit.y == selected_unit.selection_dy:
                    is_occupied = True
                    break
                 
            # Si l'unité est sur cette case, dessiner un rectangle creux
            if is_occupied:
                pygame.draw.rect(self.screen, BLUE, selection_rect, WIDTH//400)  # Rectangle creux 

        # Afficher les compétences en haut de l'écran
        if has_acted :
            self.display_skills()
        if accessible_case:
            self.display_move_unit()
        # Rafraîchir l'écran
        pygame.display.flip()
        
    # FONCTION QUI GERE QUITTER OU RECOMMENCER LE JEU
    def wait_for_input(self):
        """Attend que le joueur appuie sur Échap pour quitter ou Entrée pour recommencer."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    pygame.quit()
                    exit()

    # FONCTION DE GESTION DE LA FIN DU JEU
    def Fin(self):
        """Vérifie si le jeu est terminé et affiche l'image correspondante au centre de la fenêtre."""
        if len(self.player_units) == 0:
            print("Les ennemis ont gagné !")
            self.screen.blit(Game_over, Game_over_rect)  # Afficher l'image
            pygame.display.flip()  # Mettre à jour l'écran pour afficher l'image

            # Attente de la touche pour quitter ou recommencer
            self.wait_for_input()  # Méthode d'attente

            return True

        elif len(self.enemy_units) == 0:
            print("Le joueur a gagné !")
            self.screen.blit(You_win, You_win_rect)  # Afficher l'image
            pygame.display.flip()  # Mettre à jour l'écran pour afficher l'image

            # Attente de la touche pour quitter ou recommencer
            self.wait_for_input()  # Méthode d'attente

            return True

        return False

