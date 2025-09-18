import pygame
import math as m
from environnement import *
from abc import ABC, abstractmethod

# CONSTANTES

GRID_SIZE =  16      #Taille de la fenêtre en nombre de cellules
CELL_SIZE = 40       #Taille des cellules

WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 60
# CONSTANTE POUR L4AFFICHAGE DES COULEURS SUR LES CASES POUR DEPLACEMENT ET COMPETENCES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACKA = (0, 0, 0, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLUEA = (0, 0, 255, 128)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
YELLOWA = (255, 255, 0, 128)

# CLASSE UNIT ABTRACT

class Unit(ABC):
    """
    Super-classe abstraite pour les personnage du jeu. 
    Cette classe regroupe les attributs communs (position, point de vie, attaque, défense, rapidité, point magique, équipe)
    Méthodes :
        barre_PV pour gérer les points de vie
        portee_competence : responsable de differentes portee en fonction des competences
        accessible_case : regarde quelles sont les cases accessible pour le déplacement
        move : pour le déplacement de l'unité
        5 méthodes abstraite pour défininir les compétences, dessiner les peronnages, definir leur passif
    """
    
    def __init__(self,nom, x, y, PV, AD, AP, AR, MR, PA, PR, MS, team, portee1, portee2, portee3, zone1, zone2, zone3):
        """Constructeur : initialisation des variables"""
        self.nom = nom
        self.x = x # Position x unité
        self.y = y # Position y unité
        self.PV = PV # Point de vie
        self.PV_max = PV # Point de vie maximal (au départ)
        self.AD = AD # Attack Damage (dégat physique de l'unité)
        self.AP = AP # Ability Power
        self.AR = AR # Statistique de défence 
        self.MR = MR 
        self.PA = PA 
        self.PR = PR
        self.MS = MS #movement speed
        self.team = team  # 'player' ou 'enemy'
        # PORTEE DES COMPETENCES
        self.portee1 = portee1
        self.portee2 = portee2
        self.portee3 = portee3
        # ZONE DEFINI D'ATTAQUE
        self.zone1 = zone1
        self.zone2 = zone2
        self.zone3 = zone3

    def barre_PV(self, screen):
        """Dessine la barre de vie sous l'unité."""
        PV_ratio = self.PV / self.PV_max
        bar_width = CELL_SIZE
        bar_height = CELL_SIZE / 5
        bar_x = self.x * CELL_SIZE
        bar_y = (self.y + 1) * CELL_SIZE - bar_height
        bar_PV = (0, 255, 0)
        bar_PVmax = (255, 0, 0)

        pygame.draw.rect(screen, bar_PVmax, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, bar_PV, (bar_x, bar_y, (bar_width * PV_ratio), bar_height))

        font = pygame.font.SysFont("Arial", CELL_SIZE // 5)
        PV_text = f"{self.PV:.0f}/{self.PV_max:.0f}"
        text_surface = font.render(PV_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(text_surface, text_rect)

    def portee_competence(self, competence):
        """Calcule les cases accessibles pour la compétence en fonction de la portée."""
        accessible_skill_cases = set()

        # Choisir la portée en fonction de la compétence
        if competence == "competence1":
            portee = self.portee1  # Utilise la portée de la compétence 1
        elif competence == "competence2":
            portee = self.portee2  # Utilise la portée de la compétence 2
        elif competence == "competence3":
            portee = self.portee3  # Utilise la portée de la compétence 3
        
        for dx in range(-portee, portee + 1):
            for dy in range(-portee, portee + 1):
                # Vérifier que nous sommes dans les limites de la grille
                if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
                    # Vérifier si la case est dans la portée
                    if m.sqrt(abs(dx) + abs(dy)) <= portee+1:
                        accessible_skill_cases.add((self.x + dx, self.y + dy))
        return accessible_skill_cases
    

    def Accessible_case(self,liste_perso1, liste_perso2, grid):
            """Renvoie les cases accessibles autour de l'unité en fonction de sa vitesse de mouvement."""
            accessible_case = set()
            MS = self.MS  # La vitesse de mouvement de l'unité

            # Parcourir toutes les directions autour de l'unité 
            for dx in range(-MS, MS + 1):
                for dy in range(-MS, MS + 1):
                    # Vérifier que nous sommes dans les limites de la grille
                    if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
                        if abs(dx) + abs(dy) <= MS:  # Limiter à la portée de mouvement                        
                            # Vérifier si la case est occupée par une unité (du joueur ou de l'ennemi)
                            is_occupied = False
                            for u in liste_perso1 + liste_perso2:
                                if u.x == self.x + dx and u.y == self.y + dy and u != self:
                                    is_occupied = True
                                    break
                        
                            # Vérifier si la case est occupée par un mur ou un arbre
                            
                            for obj in grid:
                                if isinstance(obj, (MUR,TREE)) and obj.x == self.x + dx and obj.y == self.y + dy:
                                    is_occupied = True
                                    break
                        
                            # Si la case n'est pas occupée par une unité, un arbre, ou un mur
                            if not is_occupied:
                                accessible_case.add((self.x + dx, self.y + dy))
        
            return accessible_case 
    
    def move(self, new_x, new_y):
        """Déplace l'unité"""
        self.x = new_x
        self.y = new_y
    

    @abstractmethod
    def draw(self, screen):
        """Méthode abstraite pour dessiner l'unité (doit être redéfinie dans les sous-classes)."""
        pass

    @abstractmethod
    def passif(self, target):
        """Méthode abstraite pour attaquer une autre unité (doit être redéfinie dans les sous-classes)."""
        pass

    @abstractmethod
    def Compétence_1(self, target):
        """Méthode abstraite pour attaquer une autre unité (doit être redéfinie dans les sous-classes)."""
        pass

    @abstractmethod
    def Compétence_2(self, target):
        """Méthode abstraite pour attaquer une autre unité (doit être redéfinie dans les sous-classes)."""
        pass
    
    @abstractmethod
    def Compétence_3(self, target):
        """Méthode abstraite pour attaquer une autre unité (doit être redéfinie dans les sous-classes)."""
        pass

# FONCTIONNALITE DE JEU
def unit_detected(selected_unit, unit):
        if unit.x == selected_unit.selection_dx and unit.y == selected_unit.selection_dy :
            return True
        else: 
            return False
        
def calcul_degats_physiques(attack, target):

    degats = attack * 100 / (100 + target.AR)
    return degats

def calcul_degats_magiques(attack, target):

    degats = attack * 100 / (100 + target.MR)
    return degats

def reduction_armure(unit_PAR, target_AR):
    armor = target_AR * (1 - unit_PAR)
    return armor

def reduction_resistance_magique(unit_PMR, target_MR):
    MR = target_MR * (1 - unit_PMR)
    return MR

        