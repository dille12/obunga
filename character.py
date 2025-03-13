import random
import pygame

nimet = [
    "Matias", "Olavi", "Mikko", "Erkki", "Pentti", "Heikki", "Juhana", "Lauri", "Tapani", "Antti", "Kauko",
    "Paavo", "Yrjänä", "Tuomas", "Kaarle", "Jaakko", "Eerik", "Martti", "Risto", "Vilppu", "Seppo", 
    "Kirsti", "Margareeta", "Elina", "Anna", "Kaarina", "Liisa", "Birgitta", "Kristiina", "Valpuri", "Beata",
    "Eeva", "Johanna", "Brigita", "Marjeta", "Kerttu", "Sofia", "Orvokki", "Susanna", "Aune", "Helena"
]


sukunimet = [
    "Pekkanen", "Kaitajärvi", "Kettunen", "Mäkelä", "Korhonen", "Räisänen", "Heikkinen", "Hämäläinen", "Koskinen", "Lehtonen", "Nieminen", "Peltonen",
    "Savolainen", "Virtanen", "Järvinen", "Toivanen", "Luukkainen", "Tervonen", "Pitkänen", "Paavilainen", "Halonen", "Väänänen"
]



class Character:
    def __init__(self, game, name):
        self.game = game
        if not name:
            self.name = random.choice(nimet) + " " + random.choice(sukunimet)
        else:
            self.name = name

        self.game.allClients.append(self)
        self.state = "intro"  # Tracks the current story progression
        self.flags = []  # Stores past choices (e.g., {"denied": True, "killed": True})
        self.showUps = []
        self.deathText = ""
        self.organUponHarvest = ""
        self.obunga = False

    def setDeathText(self, text):
        self.deathText = text
        
    def setOrganOnHarvest(self, organ):
        self.organUponHarvest = organ
    
    def progress_story(self, day, choice):
        """ Updates character state based on player choice """
        self.flags.append()

    def get_flag(self, day, choice):
        return f"{day}{choice}" in self.flags
    
    def add_flag(self, day, choice):
        print("Adding flag:", f"{day}{choice}")
        return self.flags.append(f"{day}{choice}")


    def get_dialogue(self, day):
        """ Get the character's dialogue based on day and state """
        if day in self.dialogue:
            return self.dialogue[day].get(self.state, ["Hän ei sano mitään..."])  # Default silent response
        return ["Hän ei ole täällä tänään."]

    def should_appear(self, day):
        """ Determines if the character appears based on past events """
        if self.flags.get("killed"):
            return False  # Dead characters don't return (unless they do…👀)
        return day in self.organ_requests
