import pygame
from unit import *

class Tower_Knight(Unit):
    """Classe spécifique pour les Tower_Knight, dérivée de Unit."""
    
    def __init__(self, x, y, team):
        super().__init__('Tower_Knight', x, y, 800, 50, 50, 200, 200, 0.3, 0, 2, team, 0, 2, 5, 1, 0, 1)    #Pour sa première compétence, le TK n'a une portée que de 0 car il fait des 
                                                                                            #dégâts just autour de lui
    def draw(self, screen):
        """Affiche l'unité Tower_Knight."""
        TK = pygame.image.load("assets/TK7bis.png")
        TK = pygame.transform.scale(TK, (CELL_SIZE, CELL_SIZE))
        screen.blit(TK, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.barre_PV(screen)

    def passif(self, target):
        if self.PV < self.PV_max:
            if self.PV >= self.PV_max - 20:
                print(f"Le Tower Knight a regagné {(self.PV_max-self.PV):.1f} de PV")
                self.PV = self.PV_max
                
            else:
                self.PV += 20
                print("Le Tower Knight a regagné 20 PV")

    def Compétence_1(self, x, y, target):
        """
        Compétence 1 : le TK écrase son bouclier au sol, faisant des dégâts de zone autour de lui
        """
        if target != self:
            distance = abs(self.x - target.x) + abs(self.y - target.y)
            if abs(self.x - target.x) <= self.zone1 and abs(self.y - target.y) <= self.zone1 :
                if m.sqrt(distance) <= self.zone1 + 1 :
                    target.PV -= self.AD * 0.5                             #dégâts brut, les dégâts ignorent les résistences des ennemis

    def Compétence_2(self, x, y, target):
        """
        Compétence 2 : le TK donne un coup de lance transperçant l'ennemi, lui infligeant des dégâts de pénétration d'armure
        """
        if unit_detected(self, target) :
            attack = 20 + self.AD * 0.8
            aux = target.AR                                                 #on enregistre l'armure de l'unité car on va la modifier temporairement

            target.AR = reduction_armure(self.PA, target.AR)
            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel

            target.AR = aux                                                 #on reset l'armure de l'unité
            print(f"Le Tower Knight a fait {degat_reel:.2f} de dégâts à la cible")

    def Compétence_3(self, x, y, target):
        """
        Compétence 3 : le TK lance une lance magique sur l'ennemi, lui infligeant des dégâts magiques de zone
        """
        attack =  self.AP * 1.2
        degat_reel = calcul_degats_magiques(attack, target) 

        if target != self:
            distance = abs(x - target.x) + abs(y - target.y)
            if abs(x - target.x) <= self.zone3 and abs(y - target.y) <= self.zone3 :
                if m.sqrt(distance) <= self.zone3 + 1 :
                    target.PV -= degat_reel