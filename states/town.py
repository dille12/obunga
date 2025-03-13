import pygame
from clickable import Clickable
import random
class Town:
    def __init__(self, game):
        self.game = game

        

        self.clickables = [
            Clickable(self.game, pygame.Rect(
                285, 320, 170, 160
            ),
            "Mene töihin",
            self.goToWork,
            None),

            Clickable(self.game, pygame.Rect(
                0, 385, 110, 160
            ),
            "Mene kotiin",
            self.changeState,
            "Bedroom"),

            Clickable(self.game, pygame.Rect(
                130, 415, 70, 35
            ),
            "Paloittele ruumiit",
            self.extract,
            None),

        ]

    def tick(self):
        pass  # Placeholder for logic updates

    def extract(self, _):
        self.game.sceneSwitchTick.value = 0

        if self.game.resources["Ruumiit"]:

            for x in self.game.resources["Ruumiit"]:
                #random.seed(x.name)
                organ = x.organUponHarvest
                deathText = x.deathText
                self.game.switchDialogue.append(deathText)
                if organ:
                    self.game.resources[organ] += 1
                    self.game.switchDialogue.append(f"+1 {organ}")

        else:
            self.game.switchDialogue.append(f"Minulla ei ole ruumiita paloiteltavana.")
        
        self.game.resources["Ruumiit"].clear()



    def goToWork(self, _):

        self.game.getDaysClients()

        if self.game.workedThisDay:
            self.game.dialogue = ["Tälle päivälle ei ole enään asiakkaita."]
            self.game.savedKeypress.clear()
            self.game.keypress.clear()
            print(self.game.dialogue)
            return

        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = "Work"
        self.game.states["Work"].initiateWorkDay()

        if self.game.day == 1:
            self.game.switchDialogue = ["Minun täytyy kerätä viisi kolikkoa joka päivä vuokraa varten.", "Vuokranantajani on Obunga.", "Minun täytyy surmata kyläläisiä jotta saan kauppatavaraa."]

        
        self.game.clientIndex = 0
    
    def changeState(self, state):
        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = state
        

    def render(self, screen):
        self.game.renderCenter(self.game.town, self.game.resolution/2 )

        for x in self.clickables:
            x.tick()
