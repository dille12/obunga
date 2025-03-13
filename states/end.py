import pygame
from clickable import Clickable
class End:
    def __init__(self, game):
        self.game = game

        self.clickables = [


        ]

    def changeState(self, state):
        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = state

    def tick(self):
        pass



    def render(self, screen):
        t = self.game.font.render("Obungakauhupeli oli nyt tässä.", True, [255,255,255])
        self.game.renderCenter(t, self.game.resolution/2)

