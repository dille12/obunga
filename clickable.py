class Clickable:
    def __init__(self, game, rect, text, action, arg = None):
        self.game = game
        self.rect = rect
        self.rect.left += 187
        self.text = text
        self.action = action
        self.arg = arg


    def tick(self):
        if self.rect.collidepoint(self.game.mouse_pos):
            t = self.game.font.render(self.text, True, [255,255,255])
            self.game.screen.blit(t, [20, 440])


            if "mouse0" in self.game.keypress:
                self.action(self.arg)