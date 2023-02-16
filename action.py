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
        pyxel.blt(0,0,0,0,0,16,32, 7)

    class player:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.speed = 1
            self.jump = 1
            self.direction = 0
            self.image = 0
            self.imageX = 0
            self.imageY = 0
            self.imageWidth = 16
            self.imageHeight = 32
            self.imageColor = 7
        
        def update(self):
            pass

        def draw(self):
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY, self.imageWidth, self.imageHeight, self.imageColor)


App()
