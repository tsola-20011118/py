import pyxel

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12
playerSpeed = 4 # 2のn乗でないとバグる
scrollSpeed = 2

# Loves jinyang♡
# Loves rkurimot♡

class App:
    def __init__(self):
        pyxel.init(windowSizeX + controlSize * 2, windowSizeY, fps=30)
        pyxel.load("action.pyxres")
        # 全部で何ステージあるか
        self.stageNum = 4
        # 今何ステージ目か
        self.currentStage = 0
        # ステージ内のバトルフェーズか（False=scroll, True=battle）
        self.battlePhase = False
        # ステージ
        self.scroll = []
        # scrolllインスタンス化
        for i in range(self.stageNum):
            self.scroll.append(self.Scroll(i))
        # battle
        self.battle = []
        # battleインスタンス化
        for i in range(self.stageNum):
            self.battle.append(self.Battle(i))
        #playerインスタンス化
        self.player = self.Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        # scroll
        if self.battlePhase == False:
            self.scroll[self.currentStage].update()
        # battle
        else:
            self.battle[self.currentStage].update()
        self.player.update()


    def draw(self):
        # 全体背景
        pyxel.cls(7)
        # action部分の背景
        pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, 12)
        # scroll
        if self.battlePhase == False:
            self.scroll[self.currentStage].draw()
        # battle
        else:
            self.battle[self.currentStage].draw()
        #操作部分の背景（簡易的）
        pyxel.rect(0, 0, controlSize, windowSizeY, 7)
        pyxel.rect(controlSize + windowSizeX, 0, controlSize, windowSizeY, 7)
        # pyxel.text(0, 0, str(self.scroll[0].page[0].block[0].blockXNum), 0)
        # pyxel.text(0, 16, str(self.scroll[0].page[0].block[1].blockXNum), 0)
        self.player.draw()
    
    class Player:
        def __init__(self):
            self.image = 0
            self.imageX = 0
            self.imageY = 0
            self.imageWidth = 16
            self.imageHeight = 16
            self.imageColor = 6
            self.groundY = windowSizeY - 16 - self.imageHeight
            self.x = 156
            self.y = self.groundY
            self.speed = playerSpeed
            self.force = -1
            self.JUMP_FORCE = -12
            self.canJump = [True, True]
            self.y_prev = self.y
            self.scrollspeed = scrollSpeed

        def move(self):
            global playerSpeed, scrollSpeed
            if pyxel.btn(pyxel.KEY_LEFT) and self.x > controlSize:
                self.image = 2
                self.x -= self.speed
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.image = 1
                if self.x < controlSize + windowSizeX - self.imageWidth - 64:
                    self.x += self.speed
                else:
                    scrollSpeed = playerSpeed
            if pyxel.btn(pyxel.KEY_LEFT) == False and pyxel.btn(pyxel.KEY_RIGHT) == False:
                self.image = 0
            if pyxel.btn(pyxel.KEY_RIGHT) == False:
                scrollSpeed = self.scrollspeed

        def jump(self):
            if pyxel.btn(pyxel.KEY_SPACE) and self.canJump[0]:
                self.canJump[0] = False
                self.force = self.JUMP_FORCE
            if pyxel.btn(pyxel.KEY_SPACE) and self.canJump[1] and self.force >= -2:
                self.canJump[1] = False
                self.force = self.JUMP_FORCE
            if self.canJump[0] == False and self.canJump[1] == True:
                self.y += self.force
                self.force += 1
                if self.y >= self.groundY:
                    self.y = self.groundY
                    self.canJump[0] = True
            if self.canJump[1] == False and self.canJump[0] == False:
                self.y += self.force
                self.force += 1
                if self.y >= self.groundY:
                    self.y = self.groundY
                    self.canJump = [True, True]

            # if self.canJump[0] == False and self.canJump[1] == True:
            #     pyxel.text(10, 32, str(self.canJump), 0)
            #     y_tmp = self.y
            #     self.y += (self.y - self.y_prev) + self.force
            #     self.force = 1
            #     self.y_prev = y_tmp
            #     if self.y >= self.groundY:
            #         self.y = self.groundY
            #         self.canJump[0] = True
            # if self.canJump[1] == False and self.canJump[0] == False:
            #     pyxel.text(10, 48, str(self.canJump), 0)
            #     y_tmp = self.y
            #     self.y += (self.y - self.y_prev) + self.force
            #     self.force = 1
            #     self.y_prev = y_tmp
            #     if self.y >= self.groundY:
            #         self.y = self.groundY
            #         self.canJump = [True, True]

        def update(self):
            pass

        def draw(self):
            self.move()
            self.jump()
            pyxel.text(10, 16, str(self.x), 0)
            pyxel.text(10, 32, str(self.y), 0)
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY, self.imageWidth, self.imageHeight, self.imageColor)

    class Item:
        def __init__(self):
            self.image = 0
            self.imageX = 0
            self.imageY = 0
            self.imageWidth = 16
            self.imageHeight = 16
            self.imageColor = 6
            self.x = 100
            self.y = 100

        def update(self):
            pass

        def draw(self):
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY, self.imageWidth, self.imageHeight, self.imageColor)

    class Scroll:
        def __init__(self, stageNum):
            #スクロールが全部で何ページか
            self.pageNum = 10
            # pageが全部で何ページか
            self.page = []
            for i in range(self.pageNum):
                self.page.append(self.Page(stageNum, i))

        def update(self):
            for i in range(self.pageNum):
                self.page[i].update()

        def draw(self):
            # 床（固定）
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, 11)
            for i in range(self.pageNum):
                self.page[i].draw()
            pyxel.text(controlSize, 0, str(self.page[0].same),0)

        class Page:
            def __init__(self, stageNum, pageNum):
                self.x = pageNum * windowSizeX + controlSize
                self.same = []
                self.ground = self.Ground(stageNum, self.x)
                self.same.append(self.ground.hole)
                self.block = []
                self.blockNum = 2
                for i in range(self.blockNum):
                    self.block.append(self.Block(stageNum, self.x, self.same))
                    for j in range(self.block[i].amount):
                        self.same.append(self.block[i].start + j)
                self.staticCoin = []
                self.coinNum = pyxel.rndi(2,4)
                for i in range(self.coinNum):
                    self.staticCoin.append(self.StaticCoin(stageNum, self.x, self.same))
                    self.same.append(self.staticCoin[i].coin)
                # 床の動くスピード
                self.speed = 0

            def update(self):
                global scrollSpeed
                self.speed = scrollSpeed
                self.x -= self.speed
                self.ground.update(self.x)
                for i in range(self.blockNum):
                    self.block[i].update(self.x)
                for i in range(self.coinNum):
                    self.staticCoin[i].update(self.x)

            def draw(self):
                #pageの切り替わりがわかるように
                # pyxel.rect(self.x, 0, 8, windowSizeY, 0)
                self.ground.draw()
                for i in range(self.blockNum):
                    self.block[i].draw()
                for i in range(self.coinNum):
                    self.staticCoin[i].draw()

            class Ground:
                def __init__(self, stageNum, x):
                    # ページの右端x
                    self.x = x
                    # 草の縦幅設定
                    self.grass = []
                    self.grassFineness = int(16 * 16 / 2)
                    for i in range(self.grassFineness):
                        self.grass.append(pyxel.rndi(3, 7))
                    # 穴のX座標
                    self.hole = pyxel.rndi(1, 13)
                    self.holeX = x + self.hole * 16

                def update(self, x):
                    self.x = x
                    self.holeX = x + self.hole * 16

                def draw(self):
                    # 床（固定）
                    for i in range(self.grassFineness):
                        pyxel.rect(self.x + i * windowSizeX / self.grassFineness, windowSizeY - 16, windowSizeX / self.grassFineness,  self.grass[i], 3)
                    # 穴（固定)
                    pyxel.rect(self.holeX, windowSizeY - 16, 16 * 2,  16, 12)

            class Block:
                def __init__(self, stageNum, x, same):
                    # ページの右端x
                    self.x = x
                    self.amount = pyxel.rndi(3,4)
                    self.start = pyxel.rndi(1, 13)
                    temp = 0
                    #被らないように調節
                    while temp != len(same):
                        for s in same:
                            if self.start != s:
                                temp += 1
                            else:
                                temp = 0
                                self.start = pyxel.rndi(1, 13)
                                break
                    self.blockX = []
                    self.blockItem = []
                    self.blockType = []
                    for i in range(self.amount):
                        self.blockX.append(x + (self.start + i) * 16)
                        if pyxel.rndi(0, 1) == 0 and i != 0 and self.blockItem[i - 1] != True:
                            self.blockItem.append(True)
                        else:
                            self.blockItem.append(False)
                        self.blockType.append(pyxel.rndi(2, 3))
                    self.blockY = pyxel.rndi(5, 9) * 16

                def update(self, x):
                    self.x = x
                    for i in range(self.amount):
                        self.blockX[i] = x + (self.start + i) * 16

                def draw(self):
                    for i in range(self.amount):
                        if self.blockItem[i] == True:
                            pyxel.blt(self.blockX[i], self.blockY, 0, 16, 0, 16, 16, 6)
                        else:
                            pyxel.blt(self.blockX[i], self.blockY, 0, 16 * self.blockType[i], 0, 16, 16, 6)

            class StaticCoin:
                def __init__(self, stageNum, x, same):
                    # ページの右端x
                    self.x = x
                    self.coin = pyxel.rndi(1, 13)
                    temp = 0
                    # 被らないように調節
                    while temp != len(same):
                        for s in same:
                            if self.coin != s:
                                temp += 1
                            else:
                                temp = 0
                                self.coin = pyxel.rndi(1, 13)
                                break
                    self.coinX = x + self.coin * 16
                    self.coinGet = False
                    self.coinY = pyxel.rndi(1, 9) * 16

                def update(self, x):
                    self.x = x
                    self.coinX = x + self.coin * 16

                def draw(self):
                    if self.coinGet == False:
                        pyxel.blt(self.coinX, self.coinY, 0, 0, 16, 16, 16, 6)


                
    class Battle:

        def __init__(self, stageNum):
            pass

        def update(self):
            pass

        def draw(self):
            pass

App()