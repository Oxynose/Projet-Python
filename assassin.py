import pygame
from unit import *

class Assassin(Unit):
    """Classe spécifique pour le Protagonist, dérivée de Unit."""
    
    def __init__(self, x, y, team):
        super().__init__('Assassin', x, y, 200, 100, 50, 50, 50, 0.6, 0, 5, team, 1, 1, 1, 0, 0, 0)  #SI LA COMPETENCE NE CONCERNE QU4UNE CASE ALORS LA ZONE VAUT ZERO

    def draw(self, screen):
        """Affiche l'unité Assassin et sa barre de vie."""
        Assassin = pygame.image.load("assets/Assassin4bis.png")
        Assassin = pygame.transform.scale(Assassin, (CELL_SIZE, CELL_SIZE))
        screen.blit(Assassin, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.barre_PV(screen)
    
    def passif(self):
        pass                #Son passif est implémenté dans ses compétences : lorsque l'assassin tue une unité, il gagne 50 d'AD

    def Compétence_1(self, x, y, target):
        if unit_detected(self, target) :
            attack = 50 + self.AD * 1.8
            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel
            print(f"L'assassin a fait {degat_reel:.2f} de dégâts à la cible")
            if target.PV <= 0:
                self.AD +=50
                print(f"L'unité ASSASSIN a gagné 50 d'AD pour un total d'AD de {self.AD}")

    def Compétence_2(self, x, y, target):
       if unit_detected(self, target) :
            attack = 50 + self.AD * 1.2
            aux = target.AR           #on enregistre l'armure de l'unité car on va la modifier temporairement

            target.AR = reduction_armure(self.PA, target.AR)
            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel

            target.AR = aux           #on reset l'armure de l'unité
            print(f"L'assassin a fait {degat_reel:.2f} de dégâts à la cible")
            if target.PV <= 0:
                self.AD +=50
                print(f"L'unité ASSASSIN a gagné 50 d'AD pour un total d'AD de {self.AD}")

    def Compétence_3(self, x, y, target):
       if unit_detected(self, target) :
            attack1 = 50 + self.AD * 1.2 
            attack2 =  self.AP * 1.5
            aux = target.MR           #on enregistre l'armure de l'unité car on va la modifier temporairement

            target.MR = reduction_resistance_magique(self.PA, target.AR)
            degat_reel = calcul_degats_magiques(attack2, target) + calcul_degats_physiques(attack1, target)
            target.PV -= degat_reel

            target.MR = aux
            print(f"L'assassin a fait {degat_reel:.2f} de dégâts à la cible")
            if target.PV <= 0:
                self.AD +=50
                print(f"L'unité ASSASSIN a gagné 50 d'AD pour un total d'AD de {self.AD}")