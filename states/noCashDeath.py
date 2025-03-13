import pygame
from clickable import Clickable
import random
import sys
class noCashDeath:
    def __init__(self, game):
        self.game = game

        self.phase = 0
        self.started = False

        self.phase0tick = self.game.GT(120, oneshot = True)
        self.phase2tick = self.game.GT(90, oneshot = True)

        self.clickables = [


        ]

        self.obunga_dialogue = [
            "Oletko unohtanut jotain? Vai oletko vain niin tyhmä",
            "Et ole maksanut vuokraasi",
            "Se oli virhe",
            "Minä en anna anteeksi",
            "Hengitä syvään",
            "Tämä on loppu.",
        ]




    def changeState(self, state):
        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = state
        

    def render(self, screen):
        if not self.game.dialogue:
            self.started = True
            self.game.dialogueIncrement = 0.2

        if not self.started:
            return
        
        valOFFSET = random.uniform(0.75, 1.25)
        
        if self.phase == 0:
            if self.phase0tick.tick():
                self.phase = 1
                self.phase0tick.value = 0
            val = int(25 * valOFFSET *self.phase0tick.value / self.phase0tick.max_value)
            self.game.renderCenter(self.game.obungaFADERBIG[val], self.game.resolution/2)

        if self.phase == 1:
            if self.phase0tick.tick():
                self.phase = 2
                self.phase0tick.value = 0
                self.game.obungaDialog = True
                for x in self.obunga_dialogue:
                    self.game.dialogue.append(x.upper())

            self.game.renderCenter(self.game.obungaFADERBIG[int(25 * valOFFSET)], self.game.resolution/2)

        if self.phase == 2:


            if not self.game.dialogue:
                if self.phase2tick.tick():
                    sys.exit()

                if not self.game.jumpscare.get_num_channels():
                    self.game.jumpscare.play()

                valOFFSET = random.uniform(0.3, 1)

                val = 25 + int(75 * valOFFSET *self.phase2tick.value / self.phase2tick.max_value)

                self.game.screen.fill([val* 0.5, 0, 0])

            else:
                val = int(25 * valOFFSET)
                
            self.game.renderCenter(self.game.obungaFADERBIG[val], self.game.resolution/2)

        



    def tick(self):
        pass  # Placeholder for logic updates