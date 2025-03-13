import pygame
from clickable import Clickable
class Bedroom:
    def __init__(self, game):
        self.game = game

        self.clickables = [
            Clickable(self.game, pygame.Rect(
                388, 126, 40, 170
            ),
            "Mene kaupunkiin",
            self.changeState,
            "Town"),

            Clickable(self.game, pygame.Rect(
                7, 215, 135, 120
            ),
            "Yritä nukkua",
            self.sleep),

        ]

    def changeState(self, state):
        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = state

    def tick(self):
        pass

    def sleep(self, _):
        self.game.sceneSwitchTick.value = 0

        if not self.game.workedThisDay:
            self.game.switchDialogue = ["Minun täytyy mennä töihin."]
            return

        if self.game.day == 5:
            needs = 10
        else:
            needs = 5

        if self.game.resources["Kolikot"] >= needs:
            if self.game.day == 1:
                self.game.switchDialogue = ["Saan vaivoin unta."]
                if self.game.totalKilled:
                    if self.game.totalKilled == 1:
                        self.game.switchDialogue.append("Tapoin tänään ihmisen...")
                    else:
                        self.game.switchDialogue.append(f"Tapoin tänään {self.game.totalKilled} ihmistä...")
                else:
                    self.game.switchDialogue.append("Minun täytyy tappaa ihmisiä jotta voin maksaa vuokrani...")

                self.game.switchDialogue.append("Ja kyläläiset varmasti huomaavat jos ihmisiä alkaa katoamaan.")
                self.game.switchDialogue.append("Minun täytyy tappaa vain harvat ja valitut.")

            elif self.game.day == 4:
                self.game.switchDialogue = ["Sain nipin napin viisi kolikkoa kasaan vuokraani varten."]
                self.game.switchDialogue.append(f"Olen tappanut nyt {self.game.totalKilled} ihmistä...")
                self.game.switchDialogue.append(f"Kuinkahan käy, jollen saa vuokraani maksettua, tai kyläläiset huomaavat murhani?")
                self.game.switchDialogue.append(f"Obunga vaatii tänään 10 kolikkoa vuokrasta.")
                self.game.switchDialogue.append(f"Miten voinkaan saada niin paljon kasaan.")
            
            elif self.game.day == 5:
                self.game.muted = True
                self.game.switchDialogue = ["Maksoin 10 kolikkoa Obungalle."]
                self.game.switchDialogue.append(f"Mutta mikä oli sen hinta?")
                self.game.switchDialogue.append(f"{self.game.totalKilled} ruumista...")
                self.game.switchDialogue.append(f"Kuinkahan nyt käy?")

            else:
                self.game.switchDialogue = ["Sain nipin napin viisi kolikkoa kasaan vuokraani varten."]
                self.game.switchDialogue.append(f"Olen tappanut nyt {self.game.totalKilled} ihmistä...")
                self.game.switchDialogue.append(f"Kuinkahan käy, jollen saa vuokraani maksettua, tai kyläläiset huomaavat murhani?")
                
            self.game.day += 1
            self.game.resources["Kolikot"] -= 5

        else:
            self.game.muted = True
            self.game.switchDialogue = ["Selkäpiissäni karmii.", "Voiko olla...", "Etten maksanutkaan vuokraa?"]
            self.game.switchToState = "noCashDeath"


        self.game.workedThisDay = False

    def render(self, screen):
        self.game.renderCenter(self.game.bedroom, self.game.resolution/2)

        for x in self.clickables:
            x.tick()
