import pygame
from unit import *

class Dragon(Unit):
    """Classe spécifique pour les Dragon, dérivée de Unit."""
    
    def __init__(self, x, y, team):
        super().__init__('Dragon', x, y, 1000, 100, 100, 0, 100, 0, 0.7, 4, team, 0, 6, 6, 1, 2, 0) 

    def draw(self, screen):
        """Affiche l'unité Dragon."""
        Dragon = pygame.image.load("assets/Dragon1bis.png")
        Dragon = pygame.transform.scale(Dragon, (CELL_SIZE, CELL_SIZE))
        screen.blit(Dragon, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.barre_PV(screen)
    
    def passif(self):         #Le passif du Dragon est qu'une fois qu'il a moins de 50% de ses PV, il perd de la vie car il est blessé
        if self.PV <= self.PV_max * 0.5:
            self.PV -= 20
            print("Le Dragon a perdu la moitié de son armure et de sa résistance magique")                                         

    def Compétence_1(self, x, y, target):        
        """
        Compétence 1 : le dragon donne des coup de griffes puissantes autour de lui, faisant des dégâts de zone autour de lui
        """
        if target != self:
            attack = 100 + self.AD * 0.8
            degat_reel = calcul_degats_physiques(attack, target) 
            if target != self:
                distance = abs(self.x - target.x) + abs(self.y - target.y)
                if abs(self.x - target.x) <= self.zone1 and abs(self.y - target.y) <= self.zone1 :
                    if m.sqrt(distance) <= self.zone1 + 1 :
                        target.PV -= degat_reel

    def Compétence_2(self, x, y, target):    
        """
        Compétence 2 : le Dragon lance boule de feu magique sur l'ennemi, lui infligeant des dégâts magiques de zone
        """
        attack = self.AP * 0.5
        degat_reel = calcul_degats_magiques(attack, target) 
        if target != self:
            distance = abs(x - target.x) + abs(y - target.y)
            if abs(x - target.x) <= self.zone2 and abs(y - target.y) <= self.zone2 :
                if m.sqrt(distance) <= self.zone2 + 1 :
                    target.PV -= degat_reel

    def Compétence_3(self, x, y, target):   
        """
        Compétence 3 : le Dragon crache un laser magique sur l'ennemi, lui infligeant des dégâts magique transperçant
        """
        if unit_detected(self, target) :
            aux = target.MR
            target.MR = reduction_resistance_magique(self.PR, target.MR)
            attack = self.AP * 1.2
            degat_reel = calcul_degats_magiques(attack, target) 

            target.PV -= degat_reel
            
            target.MR = aux           #on reset la résistance magique de l'unité
            print(f"Le Dragon a fait {degat_reel:.2f} de dégâts à la cible")