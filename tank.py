import pygame
from unit import *

class Tank(Unit):
    """Classe spécifique pour les Tank, dérivée de Unit."""
    
    def __init__(self, x, y, team):
        super().__init__('Tank', x, y, 300, 100, 100, 400, 100, 0.8, 0.5, 5, team, 6, 6, 6, 0, 1, 1) 

    def draw(self, screen):
        """Affiche l'unité Tank."""
        tank = pygame.image.load("assets/Tank1bis.png")
        tank = pygame.transform.scale(tank, (CELL_SIZE, CELL_SIZE))
        screen.blit(tank, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.barre_PV(screen)
    
    def passif(self):         #Le passif du tank est qu'une fois qu'il a moins de 50% de ses PV, il perd 50% d'armure et de résistance magique
        if self.PV <= self.PV_max * 0.5:
            self.AR = 200
            self.MR = 50
            print("Le Tank a perdu la moitié de son armure et de sa résistance magique")                                         

    def Compétence_1(self, x, y, target):        #l'obus tiré est un obus transperçant très efficace contre les unités avec beaucoup d'armure
       if unit_detected(self, target) :
            attack = 50 + self.AD * 1.2
            aux = target.AR           #on enregistre l'armure de l'unité car on va la modifier temporairement

            target.AR = reduction_armure(self.PA, target.AR)
            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel

            target.AR = aux           #on reset l'armure de l'unité
            print(f"Le tank a fait {degat_reel:.2f} de dégâts à la cible")

    def Compétence_2(self, x, y, target):    #l'obus tiré est un obus explosif qui fait des dégâts physiques de zone
        """
        Compétence 2 : le Tank lance tir un obus explosif sur l'ennemi, lui infligeant des dégâts physiques de zone
        """
        attack = self.AD * 1.2
        degat_reel = calcul_degats_physiques(attack, target) 

        if target != self:
            distance = abs(x - target.x) + abs(y - target.y)
            if abs(x - target.x) <= self.zone3 and abs(y - target.y) <= self.zone3 :
                if m.sqrt(distance) <= self.zone3 + 1 :
                    target.PV -= degat_reel

    def Compétence_3(self, x, y, target):   #l'obus tiré est un obus magique qui fait des dégâts magiques de zone et qui transperce les résistences magiques
        """
        Compétence 3 : le Tank lance tir un obus magique sur l'ennemi, lui infligeant des dégâts magique transperçant de zone
        """
        aux = target.MR
        target.MR = reduction_resistance_magique(self.PR, target.MR)
        attack = self.AP * 0.5
        degat_reel = calcul_degats_physiques(attack, target) 

        if target != self:
            distance = abs(x - target.x) + abs(y - target.y)
            if abs(x - target.x) <= self.zone3 and abs(y - target.y) <= self.zone3 :
                if m.sqrt(distance) <= self.zone3 + 1 :
                    target.PV -= degat_reel
        
        target.MR = aux           #on reset la réistence magique de l'unité