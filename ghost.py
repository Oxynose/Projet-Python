import pygame
import random
from unit import *

class Ghost(Unit):
    """Classe spécifique pour le Protagonist, dérivée de Unit."""
    
    def __init__(self, x, y, team):
        super().__init__('Ghost', x, y, 200, 100, 50, 50, 50, 0.8, 0, 4, team, 1, 3, 1, 0, 0, 0)     #SI LA COMPETENCE NE CONCERNE QU'UNE CASE ALORS LA ZONE VAUT ZERO

    def draw(self, screen):
        """Affiche l'unité Assassin."""
        Ghost = pygame.image.load("assets/Ghost1.png")
        Ghost = pygame.transform.scale(Ghost, (CELL_SIZE, CELL_SIZE))
        screen.blit(Ghost, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        self.barre_PV(screen)
    
    def passif(self, target):           #Son passif est une zone qui fait des dégâts à chaque tour
        distance = abs(self.x - target.x) + abs(self.y - target.y)
        if distance <= 4:
            target.PV -= self.AP * 0.2

    def Compétence_1(self, x, y, target):
        if unit_detected(self, target) :
            # Initialisation du nombre total de dégâts
            count = 0
            attack = self.AD * 0.4
            # Initialisation de la probabilité de "pile" à 0.0
            prob_pile = 0.0
            
            # Tant que la probabilité de "pile" n'est pas atteinte (ou ne dépasse pas 1.0), on recommence
            while True:
                # Effectuer le tirage avec la probabilité actuelle de "pile"
                tirage = random.random()  # Donne un nombre entre 0 et 1
                if tirage <= prob_pile:
                    # Si c'est "pile", on arrête
                    break
                else:
                    attack += self.AD * 0.4  # Incrémenter les dégâts
                    # Incrémenter la probabilité de faire pile
                    prob_pile = min(prob_pile + 0.05, 1.0)  # Limiter la probabilité à 1.0
                    count += 1

            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel
            print(f"Ghost a fait {degat_reel:.2f} de dégâts à la cible avec {count} coups de couteau")

    def Compétence_2(self, x, y, target):
       if unit_detected(self, target) :
           # Initialisation du nombre total de dégâts
            attack = 0
            count = 0
            # Tant que la probabilité de "pile" n'est pas atteinte (ou ne dépasse pas 1.0), on recommence
            for i in range(5):
                if random.random() <= 0.4:
                    attack = attack
                else:
                    attack += self.AD * 0.4  # Incrémenter les dégâts
                    count += 1

            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel    
            print(f"Ghost a fait {degat_reel:.2f} de dégâts à la cible avec {count} lancers de couteau réussis sur {i+1}")
 
    def Compétence_3(self, x, y, target):
         
        if unit_detected(self, target) :
            attack = 50 + self.AD * 1.2
            aux = target.AR           #on enregistre l'armure de l'unité car on va la modifier temporairement

            target.AR = reduction_armure(self.PA, target.AR)
            degat_reel = calcul_degats_physiques(attack, target)
            target.PV -= degat_reel

            target.AR = aux           #on reset l'armure de l'unité
            print(f"Le Ghost a fait {degat_reel:.2f} de dégâts à la cible")
        