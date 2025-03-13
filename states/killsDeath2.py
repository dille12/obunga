import pygame
from clickable import Clickable
import random
import sys
class killsDeath2:
    def __init__(self, game):
        self.game = game
        self.started = False
        self.phase = 0
        self.phaseSwitchTick = self.game.GT(120, oneshot = True)

    def tick(self):
        pass  # Placeholder for logic updates


    def render(self, screen):
        self.game.muted = True

        if not self.started and not self.game.dialogue:
            self.started = True

            if not self.game.jumpscare.get_num_channels():
                self.game.jumpscare.play()

        if not self.game.dialogue:
            if self.started and self.phase == 0:
                if self.phaseSwitchTick.tick():
                    self.phase = 1
                    self.phaseSwitchTick.value = 0
                    self.started = False
                    self.game.dialogueIncrement = 0.2
                    self.game.obungaDialog = True
                    self.game.dialogue = ["SAASTAINEN MURHAAJA."]


            elif self.started and self.phase == 1:
                if self.phaseSwitchTick.tick():
                    self.phase = 2
                    self.phaseSwitchTick.value = 0
                    self.started = False
                    sys.exit()
                

        

        self.game.renderCenter(self.game.lynch, self.game.resolution/2)

