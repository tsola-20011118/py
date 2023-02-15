import pyxel

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12

# Loves jinyang

class App:
    def __init__(self):
        pyxel.init(windowSizeX + controlSize * 2, windowSizeY, fps=30)
        pyxel.load("action.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(1)
        pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, 8)
        # pyxel.blt(0,0,0,0,0,16,32, 7)

App()
