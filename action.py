import pyxel

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12
playerSpeed = 4  # 2のn乗でないとバグる
scrollSpeed = 0

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
        self.battlePhase = True
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
        # playerインスタンス化
        self.player = self.Player()
        pyxel.run(self.update, self.draw)

    def update(self):
        # scroll
        if self.battlePhase == False:
            self.scroll[self.currentStage].update()
        # battle
        else:
            self.battle[self.currentStage].update(self.player)
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
        # 操作部分の背景（簡易的）
        pyxel.rect(0, 0, controlSize, windowSizeY, 7)
        pyxel.rect(controlSize + windowSizeX, 0, controlSize, windowSizeY, 7)
        pyxel.rect(0, 0, controlSize, windowSizeY / 4, 6)
        pyxel.rect(0, windowSizeY / 4, controlSize, windowSizeY / 2, 8)
        pyxel.rect(0, windowSizeY / 4 * 3, controlSize, windowSizeY / 4, 6)
        pyxel.rect(controlSize + windowSizeX, 0,controlSize, windowSizeY / 4, 6)
        pyxel.rect(controlSize + windowSizeX, windowSizeY / 4, controlSize, windowSizeY / 2, 1)
        pyxel.rect(controlSize + windowSizeX, windowSizeY / 4 * 3, controlSize, windowSizeY / 4, 6)
        pyxel.text(0, 0, str(self.scroll[0].page[0].block[0].x), 0)
        # pyxel.text(0, 16, str(self.scroll[0].page[0].block[1].blockXNum), 0)
        self.player.draw()
        self.Bump(self.player, self.scroll[self.currentStage])

    def Bump(self, player, scroll):
        pageNum = None
        placeNum = None
        for i in range(scroll.pageNum):
            for j in range(16):
                if pageNum == None and placeNum == None and scroll.page[i].x + j * 16 <= player.x <= scroll.page[i].x + (j + 1) * 16:
                    pageNum = i
                    placeNum = j
                    break
        # if scroll.page[pageNum].block[0].blockY #player.yが０〜scroll.page[pageNum].block[0].blockY-16の時の終了判定
        # if windowSizeY - 16 #player.yがscroll.page[pageNum].block[0].blockY+ 16 〜の時の終了判定
    #     pyxel.text(controlSize, 16, str(pageNum) + ":" + str(placeNum), 0)
    #     pyxel.text(controlSize, 32, str(scroll.page[0].x) + ":" + str(player.x), 0)
    #     self.BlockHEAD(player, scroll.page[pageNum])

    # def BlockHEAD(self, player, page):
        
        # if player.canJump[0] == False and player.force > 0 :
        #     for i in page.block:
        #         for j in range(i.amount):
        #             if i.blockX[j] < player.x < i.blockX[j] + 16 and i.blockY <= player.y + 16:
        #                 player.canJump = [True, True]
        #                 player.y = i.blockY - 16
        #                 pyxel.text(controlSize, 32, "Test", 0)




    class Player:
        # 変数名の変更したらcommitmessageに必ず書いてくれ
        def __init__(self):
            self.image = 0
            self.imageX = 0
            self.imageY = 0
            self.imageWidth = 16
            self.imageHeight = 16
            self.imageColor = 6
            self.groundY = windowSizeY - 16 - self.imageHeight
            # 変更しました（初期位置）
            self.x = controlSize
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
                if self.x < controlSize + windowSizeX - self.imageWidth:
                    self.x += self.speed
                # TODO いる？
                # else:
                #     scrollSpeed = playerSpeed
            if pyxel.btn(pyxel.KEY_LEFT) == False and pyxel.btn(pyxel.KEY_RIGHT) == False:
                self.image = 0
            # TODO いる？
            # if pyxel.btn(pyxel.KEY_RIGHT) == False:
            #     scrollSpeed = self.scrollspeed

        def jump(self):
            if (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump[0]:
                self.canJump[0] = False
                self.force = self.JUMP_FORCE
            if (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump[1] and self.force >= -2:
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
            # 変更しました（draw->updateへの移行）
            self.move()
            self.jump()

        def draw(self):
            pyxel.text(10, 16, str(self.x), 0)
            pyxel.text(10, 32, str(self.y), 0)
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY,
                      self.imageWidth, self.imageHeight, self.imageColor)

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
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY,
                      self.imageWidth, self.imageHeight, self.imageColor)

    class Scroll:
        def __init__(self, stageNum):
            # スクロールが全部で何ページか
            self.pageNum = 10
            # pageが全部で何ページか
            self.page = []
            for i in range(self.pageNum):
                self.page.append(self.Page(stageNum, i))
            self.speed = scrollSpeed

        def update(self):
            global scrollSpeed
            if self.page[0].x - self.speed < controlSize + (self.pageNum - 1) * windowSizeX * (-1):
                self.page[0].x = controlSize + \
                    (self.pageNum - 1) * windowSizeX * (-1)
                scrollSpeed = 0
            self.speed = scrollSpeed
            for i in range(self.pageNum):
                self.page[i].update()

        def draw(self):
            # 床（固定）
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, 11)
            # 縦線つけてるだけだよ〜〜
            for i in range(self.pageNum):
                self.page[i].draw()
                for j in range(16):
                    pyxel.rect(self.page[i].x + 16 * j, 0, 1, windowSizeY, 0)
                    pyxel.rect(self.page[i].x, 0, 1, windowSizeY, 8)
            # pyxel.text(controlSize, 0, str(self.page[0].same),0)

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
                self.coinNum = pyxel.rndi(2, 4)
                for i in range(self.coinNum):
                    self.staticCoin.append(
                        self.StaticCoin(stageNum, self.x, self.same))
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
                # pageの切り替わりがわかるように
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
                        pyxel.rect(self.x + i * windowSizeX / self.grassFineness, windowSizeY -
                                   16, windowSizeX / self.grassFineness,  self.grass[i], 3)
                    # 穴（固定)
                    pyxel.rect(self.holeX, windowSizeY - 16, 16 * 2,  16, 12)

            class Block:
                def __init__(self, stageNum, x, same):
                    # ページの右端xself
                    self.x = x
                    self.amount = pyxel.rndi(3, 4)
                    self.start = pyxel.rndi(1, 13)
                    temp = 0
                    # 被らないように調節
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
                    for i in range(self.amount):
                        self.blockX.append(x + (self.start + i) * 16)
                        if pyxel.rndi(0, 1) == 0 and i != 0 and self.blockItem[i - 1] != True:
                            self.blockItem.append(True)
                        else:
                            self.blockItem.append(False)
                    self.blockY = pyxel.rndi(5, 9) * 16

                def update(self, x):
                    self.x = x
                    for i in range(self.amount):
                        self.blockX[i] = x + (self.start + i) * 16

                def draw(self):
                    for i in range(self.amount):
                        if self.blockItem[i] == True:
                            pyxel.blt(
                                self.blockX[i], self.blockY, 0, 16, 0, 16, 16, 6)
                        else:
                            pyxel.blt(
                                self.blockX[i], self.blockY, 0, 16 * 2, 0, 16, 16, 6)

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
            self.boss = self.Boss()
            

        def update(self, player):
            self.boss.update(player)

        def draw(self):
            pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, 5)
            self.boss.draw()
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, 13)
            

        class Boss:
            def __init__(self):
                # self.image = 0
                # self.imageX = 0
                # self.imageY = 0
                self.imageWidth = 32
                self.imageHeight = 32
                # self.imageColor = 6
                self.groundY = windowSizeY - 16 - self.imageHeight
                self.x = controlSize + (windowSizeX - self.imageHeight) / 2
                self.y = self.groundY
                self.action = False
                self.jumpFlag = False
                self.stunFlag = False
                self.moveTemp = pyxel.rndi(0, controlSize * 2 + windowSizeX)
                while controlSize < self.moveTemp < controlSize + windowSizeX:
                        self.moveTemp = pyxel.rndi(0, controlSize * 2 + windowSizeX)
                self.speedX = (self.moveTemp - self.x) / abs(self.moveTemp - self.x) * 2
                self.jumpSpeed = -1 * self.y / 30
                self.jumpUp = True
                self.stunTime = 0
                self.stunSpeed = 8
                self.stunStayTime = 0
                self.time = 0
                self.fireFlag = False
                self.fireSize = [0, 0, 0]
                self.fireTime = 0
                self.beamFlag = False
                self.beamSize = 0
                self.beamDirection = 0
                self.beamSpeed = 0
                self.beamTime = 0
                self.beamVanishtime = 0

            def update(self, player):
                if self.time % 90 == 0 and self.action == False:
                    self.action = True
                    bossAction = pyxel.rndi(0,10)
                    # bossAction = 9
                    if bossAction < 3:
                        self.jumpFlag = True
                    elif bossAction < 6:
                        self.stunFlag = True
                    elif bossAction < 8:
                        self.fireFlag = True
                    elif bossAction < 10:
                        self.beamFlag = True
                        if self.x > controlSize + windowSizeX / 2:
                            self.beamDirection = 1
                        else:
                            self.beamDirection = 0
                self.stun(player)
                self.jump()
                self.fire()
                self.beam()
                if self.beamFlag == False and self.fireFlag == False and self.stunTime == 0:
                    self.moveRL()
                self.time += 1

            def jump(self):
                if self.jumpFlag == True:
                    if self.jumpUp == True:
                        if self.y >= windowSizeY / 4:
                            self.jumpSpeed = -1 * self.y / 30
                        else:
                            self.jumpUp = False
                    else:
                        self.jumpSpeed = self.y / 30
                    self.y += self.jumpSpeed
                    if self.jumpUp == False and self.y >= self.groundY:
                        self.y = self.groundY
                        self.jumpFlag = False
                        self.jumpUp = True
                        self.action = False

            def stun(self, player):
                if self.stunFlag == True:
                    self.jumpFlag = True
                    if self.jumpUp == False:
                        self.jumpFlag = False
                        self.stunTime += 1
                        if self.stunTime > 5:
                            self.y += self.stunSpeed
                            self.stunSpeed += 1
                        if self.y >= self.groundY:
                            self.y = self.groundY
                            self.stunStayTime += 1
                            if player.y == self.groundY:
                                player.isStun = True
                        if self.stunStayTime != 0 and self.stunStayTime < 20:
                            self.stunTime += 1
                        if self.stunStayTime >= 20:
                            player.isStun = False
                            self.stunFlag = False
                            self.jumpUp = True
                            self.stunStayTime = 0
                            self.stunTime = 0
                            self.stunSpeed = 8
                            self.action = False

            def fire(self):
                if self.fireFlag == True:
                    if self.fireTime > 0:
                        self.fireSize[0] += 2
                    if self.fireTime > 10:
                        self.fireSize[1] += 2
                    if self.fireTime > 20:
                        self.fireSize[2] += 2
                    if self.fireSize[0] >= 100:
                        self.fireFlag = False
                        self.fireSize = [0, 0, 0]
                        self.fireTime = 0
                        self.action = False
                    self.fireTime += 1

            def beam(self):
                if self.beamFlag == True:
                    if self.beamTime > 10:
                        self.beamSpeed = 8
                    self.beamSize += self.beamSpeed
                    if self.beamVanishtime == 0 and ((self.beamDirection == 0 and self.beamSize + self.x > controlSize + windowSizeX) or (self.beamDirection == 1 and + self.x - self.beamSize < controlSize)):
                        self.beamVanishtime += 1
                    if self.beamVanishtime != 0:
                        self.beamVanishtime += 1
                    if self.beamVanishtime > 20:
                        self.beamFlag = False
                        self.beamSize = 0
                        self.beamSpeed = 0
                        self.beamTime = 0
                        self.beamVanishtime = 0
                        if self.x > controlSize + windowSizeX / 2:
                            self.beamDirection = 1
                        else:
                            self.beamDirection = 0
                        self.action = False
                    self.beamTime += 1



            def moveRL(self):
                if (self.speedX < 0 and controlSize > self.x + self.speedX):
                    self.moveTemp = pyxel.rndi(0, controlSize)
                    self.speedX *= -1
                if (self.speedX >= 0 and controlSize + windowSizeX < self.x + self.speedX + self.imageWidth):
                    self.moveTemp = pyxel.rndi(controlSize + windowSizeX, controlSize * 2 + windowSizeX)
                    self.speedX *= -1
                if (self.speedX < 0 and self.moveTemp < self.x) or (self.speedX >= 0 and self.moveTemp > self.x):
                    self.x += self.speedX
                else:
                    self.moveTemp = pyxel.rndi(0, controlSize * 2 + windowSizeX)
                    while controlSize < self.moveTemp < controlSize + windowSizeX:
                        self.moveTemp = pyxel.rndi(0, controlSize * 2 + windowSizeX)
                    self.speedX = (self.moveTemp - self.x) / abs(self.moveTemp - self.x) * 2



            def draw(self):
                for size in self.fireSize:
                    pyxel.circ(self.x + self.imageWidth / 2 , self.y + self.imageHeight / 2, size, 0)
                if self.beamDirection == 0:
                    pyxel.rect(self.x, self.y + 4, self.beamSize, self.imageHeight - 8, 8)
                elif self.beamDirection == 1:
                    pyxel.rect(self.x - self.beamSize, self.y + 4, self.beamSize, self.imageHeight - 8, 8)
                pyxel.rect(self.x, self.y, self.imageWidth, self.imageHeight, 8)
                pyxel.text(controlSize, 0, str(self.action), 0)
                # pyxel.text(controlSize, 16, str(self.beamFlag), 0)
                # pyxel.text(controlSize, 32, str(self.beamDirection), 0)
                # pyxel.text(controlSize, 48, str(self.beamSpeed), 0)
                # pyxel.rect(self.x + self.imageWidth / 2 , self.y + self.imageHeight / 2, 10, 10, 0)
                
                # pyxel.circ(0, 0, 100, 0)



def Button():
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (pyxel.mouse_x <= controlSize or controlSize + windowSizeX <= pyxel.mouse_x):
        # 上ボタン押した時返り値10
        # 下ボタン押した時返り値-10
        # 右ボタン押した時返り値1
        # 左ボタン押した時返り値-1
        if 0 <= pyxel.mouse_y <= windowSizeY / 4:
            return 10
        elif windowSizeY / 4 * 3 <= pyxel.mouse_y <= windowSizeY:
            return -10
        elif pyxel.mouse_x <= controlSize:
            return -1
        else:
            return 1


App()
