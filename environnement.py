# FICHIER PRORMMATION DE L'ENVIRONNEMENT

import pygame
from abc import ABC, abstractmethod
# CONSTANTE POUR LA GRILLE
GRID_SIZE =  16         
CELL_SIZE = 40

# IMPORTATION DES IMAGES DE L'ENVIRONNEMENT

mur = pygame.image.load("assets/mur1.png")
mur = pygame.transform.scale(mur, (CELL_SIZE, CELL_SIZE))
herbe = pygame.image.load("assets/herbe.jpg")
herbe = pygame.transform.scale(herbe, (CELL_SIZE, CELL_SIZE))
tree = pygame.image.load("assets/tree.jpeg")
tree = pygame.transform.scale(tree, (CELL_SIZE, CELL_SIZE))
eau = pygame.image.load("assets/eau.jpg")
eau = pygame.transform.scale(eau, (CELL_SIZE, CELL_SIZE))
cactus = pygame.image.load("assets/image_cactus.jpg")
cactus = pygame.transform.scale(cactus, (CELL_SIZE, CELL_SIZE))

# CREATION CLASSE BLOCK abstraite
class Block (ABC):
    """ Classe abstraite pour les différents éléments de l'environnement.
    Prend en élément la position, et une méthode draw absraite pour l'affichage
    """
    def __init__(self, x,y):
        """ Initiliasation dans le constructeur"""
        self.x = x # Position x dans la grille
        self.y = y # Position y dans la grille
    
    
    @abstractmethod
    def draw(self, screen):
        """Méthode abstraite pour afficher l'élément (redéfinie dans les sous-classes)."""
        pass


# ELEMENTS : MUR, HERBE, ARBRE, EAU, CACTUS

class MUR(Block):
    """Classe programmation des murs. 
        Personnage ne peuvent pas se placer sur la case mur (programmer dans méthode accessible_case)
        Affichage sur la map
        Heritage Classe Block.
    """
    # CONSTRUCTEUR
    def __init__(self, x, y):
        super().__init__(x, y) # Heritage du constructeur de Block

    # AFFICHAGE
    def draw(self, screen):
        """AFFICHAGE IMAGE MUR."""
        screen.blit(mur, (self.x * CELL_SIZE, self.y * CELL_SIZE)) # Affichage image à la position donnée

class HERBE(Block):
    """Classe programmation des Herbes
        Affichage sur la map
        Heritage Classe Block.
    """

    def __init__(self, x, y):
        super().__init__(x, y)  

    def draw(self, screen):
        """AFFICHAGE IMAGE HERBE."""
        screen.blit(herbe, (self.x * CELL_SIZE, self.y * CELL_SIZE)) # Affichage image à la position demandé

class TREE(Block):
    """Classe programmation des arbres. 
        Impossible de passé deçu mais certain personnage peuvent les détruires et les transformer en Herbe
        Affichage sur la map
        Heritage Classe Block.
    """

    def __init__(self, x, y):
        super().__init__(x, y)  

    def draw(self, screen):
        """AFFICHAGE IMAGE ARBRE."""
        screen.blit(tree, (self.x * CELL_SIZE, self.y * CELL_SIZE))


class EAU(Block):
    """Classe programmation de l'eau.
        Si personnage sur l'eau, tue le personnage (programmmation dans game)
        Affichage sur la map
        Heritage Classe Block.
    """

    def __init__(self, x, y):
        super().__init__(x, y)  

    def draw(self, screen):
        """AFFICHAGE IMAGE EAU."""
        screen.blit(eau, (self.x * CELL_SIZE, self.y * CELL_SIZE))

class CACTUS(Block):
    """Classe programmation des cactus.
        Cactus fait perdre des PV aux personnages qui passent à coté ou qui sont sur la case cactus ( programmer dans game) 
        Afficage sur la map
        Heritage Classe Block.
    """

    def __init__(self, x, y):
        super().__init__(x, y)  

    def draw(self, screen):
        """AFFICHAGE IMAGE CACTUS."""
        screen.blit(cactus, (self.x * CELL_SIZE, self.y * CELL_SIZE))


# CLASSE ENVIRONNEMENT : génère l'environnement en plaçant les éléments

class Environnement:
    def __init__(self):
        pass

    def generate_environnement():
        """GENERER ENVIRONNEMENT
            A des coordonnée fixe
        """
        coord_mur = [(0,12), (1,12), (2,12), (3,12), (4,12), (5,12), (6,12), (7,12), (8,2), (9,2), (10,2), (11,2), (12,2), 
             (13,2), (13,3), (13,4), (13,5), (13,6)]
        coord_arbre = [(8,0), (9,0), (10,0), (11,0), (12,0), (13,0), (14,0), (15,0),(8,1), (9,1), (10,1), (11,1), (12,1),
                        (13,1), (14,1), (15,1),(0,9), (0,10), (0,11),(1,9), (1,10), (1,11)]
        coord_eau = [(6,6),(7,6),(5,7),(6,7),(7,7),(8,7),(5,8),(6,8),(7,8),(8,8),(6,9),(7,9)]
        coord_cactus = [(1,5), (11,8)]

        # INITIALISATION ENVIRONNEMENT
        environnement = []
        # POSITION COORDONNEE DU MUR
        for (x,y) in coord_mur:
            environnement.append(MUR(x,y))
        # POSITION COORDONNEE ARBRE
        for (x,y) in coord_arbre:
            environnement.append(TREE(x,y))
        # POSITION COORDONNEE EAU
        for (x,y) in coord_eau:
            environnement.append(EAU(x,y))
        # POSITION COORDONNEE CACTUS
        for (x,y) in coord_cactus:
             environnement.append(CACTUS(x,y))
        # POSITION COORDONNEE HERBE
        for x in range (GRID_SIZE):
             for y in range (GRID_SIZE):
                  if (x,y) not in (coord_arbre + coord_cactus + coord_eau + coord_mur):
                       environnement.append(HERBE(x,y))

        return environnement