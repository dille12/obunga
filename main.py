
import os
import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    FROZEN = True
else:
    FROZEN = False

import pygame
from keypress import key_press_manager
from states.town import Town  # Import the Town state
from states.bedroom import Bedroom  # Import the Town state
from states.work import Work  # Import the Town state
from states.noCashDeath import noCashDeath
from states.killsDeath import killsDeath
from states.killsDeath2 import killsDeath2
from states.end import End
import numpy 
# Initialize Pygame
pygame.init()
from gametick import GameTick
# Screen dimensions
SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

from genCharacters import genCharacters

# Colors
BLACK = (0, 0, 0)


# Screen setup

pygame.display.set_caption("Obunga")
import random
from character import Character
# Clock for controlling the frame rate
clock = pygame.time.Clock()

def make_surface_rgba(array):
    """Returns a surface made from a [w, h, 4] numpy array with per-pixel alpha
    """
    shape = array.shape
    if len(shape) != 3 and shape[2] != 4:
        raise ValueError("Array not RGBA")

    # Create a surface the same width and height as array and with
    # per-pixel alpha.
    surface = pygame.Surface(shape[0:2], pygame.SRCALPHA, 32)

    # Copy the rgb part of array to the new surface.
    pygame.pixelcopy.array_to_surface(surface, array[:,:,0:3])

    # Copy the alpha part of array to the surface using a pixels-alpha
    # view of the surface.
    surface_alpha = numpy.array(surface.get_view('A'), copy=False)
    surface_alpha[:,:] = array[:,:,3]

    return surface

class Game:
    def __init__(self):
        self.running = True  
        self.keypress = []
        self.keypress_held_down = []
        self.mousepos = [0, 0]
        self.v2 = pygame.math.Vector2
        self.resolution = self.v2(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.GT = GameTick

        self.sceneSwitchTick = self.GT(40, oneshot=True)
        self.sceneSwitchTick.value = 15
        self.switchToState = None
        self.switchDialogue = []

        self.globalFlags = []


        self.workedThisDay = False

        self.muted = False

        self.dialogue = [
            "...",
            "Jokin on pielessä...",
            "Kylän asukit.",
            "Kukaan ei puhu siitä ääneen, mutta he tietävät...",
            "Obunga tulee viiden päivän päästä.",
            "Tarvitsen elimiä."
        ]
        self.dialogueIndex = 0
        self.dialogueIncrement = 1
        self.obungaDialog = False

        self.allClients = []
        self.day = 1
        self.totalKilled = 0

        genCharacters(self)

        self.getDaysClients()
        #sys.exit()


        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN)

        a = pygame.Surface(self.resolution).convert_alpha()
        self.blackOut = []
        for x in range(21):
            a.fill([0,0,0])
            a2 = a.copy()
            a2.set_alpha(255*x/15)
            self.blackOut.append(a2)

        self.font = pygame.font.Font("texture/font.ttf", 30)
        self.fontS = pygame.font.Font("texture/font.ttf", 20)

        obungaTemp = pygame.image.load("texture/obungaHead.png").convert_alpha()
        obungaTemp = pygame.transform.scale(obungaTemp, [100,100])

        self.obunga = pygame.Surface((100, 100), flags=pygame.SRCALPHA).convert_alpha()
        self.obunga.blit(obungaTemp, [0,0])

        
        

        self.obungaFADER = []
        self.obungaFADERBIG = []
        obungaRGB = pygame.surfarray.array3d(self.obunga) / 255  # Normalize RGB
        obungaAlpha = pygame.surfarray.array_alpha(self.obunga) / 255  # Normalize Alpha

        for i in range(100):
            i2 = i / 100
            fadeFactor = i2 ** 3  # Correct exponentiation

            obungaRGB2 = obungaRGB * fadeFactor**(1.1 - obungaRGB)
            alphaMock = numpy.mean(obungaRGB2, axis=-1) * obungaAlpha

            #obungaAlpha2 = obungaAlpha * fadeFactor  # Fade alpha too

            # Reconstruct the surface with faded RGBA
            obungaRGBA = numpy.dstack((obungaRGB2, alphaMock)) * 255
            
            obungaSurf = make_surface_rgba(obungaRGBA.astype(numpy.uint8))

            self.obungaFADER.append(obungaSurf)

            obungaSurfTemp = pygame.transform.scale(obungaSurf, [480,480])
            self.obungaFADERBIG.append(obungaSurfTemp)

        self.obungaFadeTick = 0


        

        self.kill = pygame.mixer.Sound("audio/kill.wav")
        self.decline = pygame.mixer.Sound("audio/decline.wav")
        self.accept = pygame.mixer.Sound("audio/success.wav")
        self.footsteps = pygame.mixer.Sound("audio/footsteps.wav")
        self.obungadialogsound = pygame.mixer.Sound("audio/obunga.wav")
        self.jumpscare = pygame.mixer.Sound("audio/jumpscare.wav")
        self.outrage = pygame.mixer.Sound("audio/anger.wav")
        self.music = pygame.mixer.Sound("audio/loop.wav")
        self.runSound = pygame.mixer.Sound("audio/run.wav")
        self.doorSmash = pygame.mixer.Sound("audio/doorsmash.wav")
        self.outrage.set_volume(0)
        self.outrageVolume = 0

        #pygame.mixer.music.load()
        #pygame.mixer.music.play(-1)

        self.town = pygame.image.load("texture/town.png").convert()
        self.town = pygame.transform.scale(self.town, [480,480])

        self.vignette = pygame.image.load("texture/vignette.png").convert_alpha()
        self.vignette = pygame.transform.scale(self.vignette, [480,480])

        self.vignettedialog = pygame.image.load("texture/vignettedialog.png").convert_alpha()
        self.vignettedialog = pygame.transform.scale(self.vignettedialog, [480,480])

        self.bedroom = pygame.image.load("texture/bedroom.png").convert()
        self.bedroom = pygame.transform.scale(self.bedroom, [480,480])

        self.workTop = pygame.image.load("texture/workTop.png").convert_alpha()
        self.workTop = pygame.transform.scale(self.workTop, [480,480])
        self.workBottom = pygame.image.load("texture/workBottom.png").convert_alpha()
        self.workBottom = pygame.transform.scale(self.workBottom, [480,480])
        self.workBars = pygame.image.load("texture/workBars.png").convert_alpha()
        self.workBars = pygame.transform.scale(self.workBars, [480,480])

        self.lynch = pygame.image.load("texture/deathbycorpses.png").convert_alpha()
        self.lynch = pygame.transform.scale(self.lynch, [480,480])

        self.organs = {}
        self.resources = {"Kolikot": 3, "Ruumiit" : []}
        for x in ["maha", "sydän", "munuainen", "maksa"]:
            tmp = pygame.image.load(f"texture/{x}.png").convert_alpha()
            tmp = pygame.transform.scale(tmp, [20,20])
            self.organs[x] = tmp
            self.resources[x] = 1


        

        self.char1 = pygame.image.load("texture/character1.png").convert_alpha()
        self.char1 = pygame.transform.scale(self.char1, [100,100])

        #self.generateTownPeople()

        # Game state management
        self.states = {
            "Town": Town(self),
            "Bedroom": Bedroom(self),
            "Work" : Work(self),
            "noCashDeath" : noCashDeath(self),
            "killsDeath" : killsDeath(self),
            "killsDeath2" : killsDeath2(self),
            "End" : End(self),
        }

        
        
        self.current_state = "Bedroom"


    def add_global_flag(self, flag):
        if flag not in self.globalFlags:
            self.globalFlags.append(flag)

    def getDaysClients(self):
        self.todaysClients = []
        for client in self.allClients:
            print(client.showUps)
            for showUp in client.showUps:

                ShowingUp = True

                print(showUp.day)

                if showUp.day == self.day:
                    
                    for flagCheck in showUp.onFlags:
                        if flagCheck not in client.flags and flagCheck not in self.globalFlags:
                            ShowingUp = False
                            print("Flag not present:", flagCheck)
                            break

                    if ShowingUp:
                        self.todaysClients.append(showUp)
                        print("added showup", showUp, showUp.day)
                else:
                    print("WRONG DAY")

        print(self.todaysClients)


    def handleKeypresses(self):
        key_press_manager(self)
        
    def update(self):
        self.savedKeypress = self.keypress.copy()
            
        if self.dialogue:
            self.keypress.clear()
            self.mouse_pos = self.v2([0,0])

        if self.current_state:
            self.states[self.current_state].tick()  # Update the current game state


    def renderCenter(self, im, pos):
        pos2 = pos - self.v2(im.get_size())/2
        self.screen.blit(im, pos2)

    
    def draw(self):
        self.screen.fill(BLACK)  # Clear the screen
        if self.current_state:
            self.states[self.current_state].render(self.screen)  # Draw the current state


        if not self.dialogue and self.current_state not in ["End", "noCashDeath", "killsDeath", "killsDeath2"]:
            self.renderResources()


        
        if not self.sceneSwitchTick.isMaxed():

            if not self.dialogue:
                self.sceneSwitchTick.tick()

            val = 20 - abs(self.sceneSwitchTick.value - 20)
            

            if val == 20 and self.switchToState:
                self.current_state = self.switchToState
                self.switchToState = None

            if val == 20 and self.switchDialogue:
                self.dialogue += self.switchDialogue
                self.switchDialogue.clear()

            self.screen.blit(self.blackOut[val], [0,0])



        if self.dialogue:
            
            self.renderCenter(self.vignettedialog, self.resolution/2)

            if isinstance(self.dialogue[0], list):
                text, speaker = self.dialogue[0]
            else:
                text = self.dialogue[0]
                speaker = ""

            if self.dialogueIndex <= len(text):
                self.dialogueIndex += self.dialogueIncrement


            cut = min(int(self.dialogueIndex), len(text))

            if self.obungaDialog:
                color = [255,0,0]
                offset = [random.randint(-2,2), random.randint(-2,2)]

                if cut < len(text) and not self.obungadialogsound.get_num_channels():
                    self.obungadialogsound.play()
                elif cut == len(text):
                    self.obungadialogsound.stop()

            else:
                color = [255,255,255]
                offset = [0,0]

            t = self.font.render(text[:cut], True, color)
            self.renderCenter(t, self.resolution/2 + offset)

            
            t = self.fontS.render(speaker, True, [200,155,155])
            self.renderCenter(t, self.resolution/2 - [0, 30] + offset)

            if "mouse0" in self.savedKeypress:
                if cut < len(text):
                    self.dialogueIndex = len(text)
                else:
                    self.dialogue.remove(self.dialogue[0])
                    self.dialogueIndex = 0
     

        

        pygame.display.update()  


    def renderResources(self):
        t = self.font.render(f"Päivä {self.day}", True, [255,155,155])
        self.screen.blit(t, [10, 5])

        coins = self.resources["Kolikot"]
        t = self.font.render(f"Kolikot: {coins}", True, [255,155,155])
        self.screen.blit(t, [10, 30])

        y = 100

        corpses = self.resources["Ruumiit"]
        if corpses:
            t = self.font.render(f"Ruumiit: {len(corpses)}", True, [255,155,155])
            self.screen.blit(t, [10, 65])

        for x in self.resources:
            if x not in self.organs:
                continue

            self.screen.blit(self.organs[x], [10, y])

            amount = self.resources[x]
            t = self.font.render(f"x {amount}", True, [255,155,155])
            self.screen.blit(t, [35, y])

            y += 25


    def handleMusic(self):

        if self.muted:
            self.outrage.set_volume(0)
            self.music.set_volume(0)
            return

        if self.totalKilled/5 > self.outrageVolume:
            self.outrageVolume += 0.0002
        elif self.totalKilled/5 < self.outrageVolume:
            self.outrageVolume -= 0.0002


        self.outrage.set_volume(self.outrageVolume)
        self.music.set_volume(1-0.3*self.outrageVolume)
        if not self.outrage.get_num_channels():
            self.outrage.play()

        if not self.music.get_num_channels():
            self.music.play()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handleKeypresses()
            self.handleMusic()
            self.update()
            self.draw()
            
            clock.tick(60)  # Limit FPS to 60
        
        pygame.quit()
        sys.exit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
