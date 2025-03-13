import pygame
from clickable import Clickable
import random
class killsDeath:
    def __init__(self, game):
        self.game = game
        self.started = False
        self.phase = 0
        self.phaseSwitchTick = self.game.GT(60, oneshot = True)

    def tick(self):
        pass  # Placeholder for logic updates


    def render(self, screen):
        self.game.muted = True

        if not self.started and not self.game.dialogue:
            self.started = True

            if self.phase == 0:
                self.game.runSound.play()

            elif self.phase == 1:
                self.game.doorSmash.play()


        if not self.game.dialogue:

            if self.started and self.phase == 0 and not self.game.runSound.get_num_channels():
                if self.phaseSwitchTick.tick():
                    self.phase = 1
                    self.phaseSwitchTick.value = 0
                    self.started = False
                    self.game.dialogue = ["Joku taitaa olla ovella."]


            elif self.started and self.phase == 1 and not self.game.doorSmash.get_num_channels():
                if self.phaseSwitchTick.tick():
                    self.phase = 2
                    self.phaseSwitchTick.value = 0
                    self.started = False
                    self.game.sceneSwitchTick.value = 0
                    self.game.switchToState = "killsDeath2"
                

        

        self.game.renderCenter(self.game.workBottom, self.game.resolution/2)

        self.game.renderCenter(self.game.workBars, self.game.resolution/2)

        self.game.renderCenter(self.game.workTop, self.game.resolution/2)
