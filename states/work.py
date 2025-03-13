import pygame
from clickable import Clickable
import random 
class Work:
    def __init__(self, game):
        self.game = game

        self.movementTick = self.game.GT(120, oneshot = True)

        self.clientState = 0

        self.clickables = [


        ]

        self.exitOut = False
        self.obungaUnderTableTick = game.GT(60)
        self.dayStarted = False
        self.obungaWither = False
        


    def initiateWorkDay(self):
        self.movementTick.value = 0
        self.clientState = 0
        self.dayStarted = False
        self.obungaUnderTableTick.value = 0
        #self.obungaWither = False
        


    def changeState(self, state):
        self.game.sceneSwitchTick.value = 0
        self.game.switchToState = state

    def tick(self):
        if self.game.clientIndex < len(self.game.todaysClients):
            self.client = self.game.todaysClients[self.game.clientIndex]
        else:
            self.client = None

    def render(self, screen):
        self.game.renderCenter(self.game.workBottom, self.game.resolution/2)

        if not self.game.dialogue:
            self.dayStarted = True

        if self.dayStarted and self.clientState not in [1, 5] and self.movementTick.tick():
            self.clientState += 1
            self.movementTick.value = 0
            if self.clientState == 1 and self.client:

                if self.client.character.obunga:
                    self.game.dialogueIncrement = 0.2
                    self.game.obungaDialog = True

                self.game.dialogue = self.client.dialogue["intro"].copy()

            elif self.clientState == 4:
                self.game.clientIndex += 1
                self.clientState = 0

                if self.game.clientIndex == len(self.game.todaysClients):

                    if self.game.totalKilled > 5:
                        self.game.current_state = "killsDeath"
                        self.clientState = 5

                    elif self.game.day == 6:
                        self.game.sceneSwitchTick.value = 0
                        self.game.switchToState = "End"
                        self.clientState = 5

                    else:
                        self.game.dialogue = ["Siinä olivat asiakkaat tältä erää."]
                        self.game.sceneSwitchTick.value = 0
                        self.game.switchToState = "Town"
                        self.game.workedThisDay = True
                        self.clientState = 5


        offset = [0,30]
        if self.clientState == 0:
            offset[0] = -(self.movementTick.max_value - self.movementTick.value)
            if not self.game.footsteps.get_num_channels() and self.dayStarted:
                self.game.footsteps.play()

        elif self.clientState == 2:
            offset[0] = self.movementTick.value * 1.1

            if not self.game.footsteps.get_num_channels():
                self.game.footsteps.play()

        elif self.clientState == 3:
            offset[0] = 200
            
        
        if self.clientState not in [0, 2]:
            self.game.footsteps.stop()
        
        if self.client and self.clientState in [0,1,2]:

            if self.client.character.obunga:
                self.game.renderCenter(self.game.obunga, self.game.resolution/2 + offset)
                

            else:
                self.game.renderCenter(self.game.char1, self.game.resolution/2 + offset)

        self.game.renderCenter(self.game.workBars, self.game.resolution/2)

        self.game.renderCenter(self.game.workTop, self.game.resolution/2)


        if self.game.day >= 3:
            
            if self.obungaWither:
                self.game.obungaFadeTick -= 1
                self.game.obungaFadeTick = max(self.game.obungaFadeTick, 0)
            else:
                if self.obungaUnderTableTick.tick():
                    if self.game.obungaFadeTick < len(self.game.obungaFADER) - 1:
                        self.game.obungaFadeTick += 1
                        self.game.obungaFadeTick = min(self.game.obungaFadeTick, 60)

            self.game.renderCenter(self.game.obungaFADER[int(self.game.obungaFadeTick)], [self.game.resolution[0]/2, 420])
            r = pygame.Rect(self.game.resolution[0]/2 - 50, 370, 100, 100)
            if r.collidepoint(self.game.mouse_pos) and "mouse0" in self.game.keypress and not self.game.dialogue:
                self.obungaWither = True


        if self.clientState == 1 and not self.game.dialogue and self.client and not self.client.request:
            self.clientState = 2
            self.movementTick.value = 0
            self.game.resources["Kolikot"] += self.client.pay

        elif self.clientState == 1 and not self.game.dialogue and self.client:
            t = self.game.fontS.render(f"Anna {self.client.request} nyt heti!", True, [155,100,100])
            self.game.renderCenter(t, self.game.resolution/2 - [0, 20])

            self.game.renderCenter(self.game.vignette, self.game.resolution/2)

            for i, x in enumerate(["Hyväksy", "Kieltäydy", "Tapa"]):
                xpos = (1-i) * 100
                t = self.game.font.render(f"{x}", True, [255,255,255])

                r = t.get_rect()
                r.center = self.game.resolution/2 - [xpos, -10] 

                r.inflate_ip(4,4)

                if i == 0:
                    t2 = self.game.fontS.render(f"-1 {self.client.request}", True, [255,0,0])
                    self.game.screen.blit(t2, self.game.v2(r.bottomleft) - [0, -5])

                    t2 = self.game.fontS.render(f"+{self.client.pay} kolikkoa", True, [255,255,0])
                    self.game.screen.blit(t2, self.game.v2(r.bottomleft) - [0, -30])

                if r.collidepoint(self.game.mouse_pos):
                    w = 2

                    if "mouse0" in self.game.keypress:
                        if i == 0:

                            if self.game.resources[self.client.request] <= 0:
                                print("No cash")
                                self.game.decline.play()

                            else:
                                self.game.accept.play()
                                self.game.dialogue = self.client.dialogue["accept"].copy()
                                self.game.savedKeypress.clear()
                                self.game.resources[self.client.request] -= 1
                                self.game.resources["Kolikot"] += self.client.pay
                                self.clientState = 2
                                self.movementTick.value = 0
                                self.client.character.add_flag(self.game.day, "accept")
                                self.game.add_global_flag(f"{self.game.day} {self.client.character.name} accept")

                        if i == 2:
                            self.game.resources["Ruumiit"].append(self.client.character)
                            self.game.kill.play()
                            self.clientState = 3
                            self.movementTick.value = 0
                            self.client.character.add_flag(self.game.day, "killed")
                            self.game.add_global_flag(f"{self.game.day} {self.client.character.name} killed")
                            self.game.add_global_flag(f"{self.game.day} killed")
                            self.game.totalKilled += 1

                        if i == 1:
                            
                            self.game.dialogue = self.client.dialogue["deny"].copy()
                            self.game.savedKeypress.clear()
                            self.clientState = 2
                            self.movementTick.value = 0
                            self.client.character.add_flag(self.game.day, "deny")
                            self.game.add_global_flag(f"{self.game.day} {self.client.character.name} deny")
                            

                else:
                    w = 1

                pygame.draw.rect(self.game.screen, [255,255,255], r, width= w)

                self.game.renderCenter(t, self.game.resolution/2 - [xpos, -10])

                

                #self.screen.blit(, [0,0])

        
            

        for x in self.clickables:
            x.tick()
