import pyxel

class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Best game for ever")
    
        pyxel.run(self.update, self.draw)

    def update(self):
        print("test")

    def draw(self):
        pyxel.rect(80, 80, 20, 20, 1)

Game()