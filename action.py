import pyxel
import math

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12
playerSpeed = 4  # 2のn乗でないとバグる
scrollSpeed = 2

# A little bit hate jinyang💔
# Loves rkurimot♡
# Loves igagurimot♡
# Loves roostar♡ and Bython♡
# Loves flower ghost♡


class App:
    def __init__(self):
        pyxel.init(windowSizeX + controlSize * 2, windowSizeY, fps=30)
        pyxel.load("action.pyxres")
        self.start()
        self.life = 5
        pyxel.run(self.update, self.draw)

    def update(self):
        global scrollSpeed
        if self.gameMode == 0:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (controlSize <= pyxel.mouse_x <=  controlSize + windowSizeX):
                self.gameMode = 1
        elif self.gameMode == 1:
            # scroll
            if self.battlePhase == False:
                if self.player.alive == True:
                    self.Bump(self.player, self.scroll[self.currentStage])
                    self.scroll[self.currentStage].update(self.currentStage)
                    for i in range(self.scroll[self.currentStage].pageNum):
                        for j in range(self.scroll[self.currentStage].page[i].coinNum):
                            self.CoinGet(self.scroll[self.currentStage].page[i].staticCoin[j], self.player)
                        if self.currentStage != 0:
                            for j in range(self.scroll[self.currentStage].page[i].enemyNum):
                                self.EnemyBump(self.scroll[self.currentStage].page[i].enemy[j], self.player)
                        for j in range(self.scroll[self.currentStage].page[i].blockNum):
                            self.BlockToItem(self.scroll[self.currentStage].page[i].block[j], self.player, self.scroll[self.currentStage].page[i])
                        for j in range(self.scroll[self.currentStage].page[i].blockNum):
                            self.BlockToItem(self.scroll[self.currentStage].page[i].block[j], self.player, self.scroll[self.currentStage].page[i])
                        for j in range(self.scroll[self.currentStage].page[i].itemNum):
                            self.ItemGet(self.player, self.scroll[self.currentStage].page[i].item[j])
                for i in range(self.scroll[self.currentStage].pageNum):
                    self.HoleDown(self.scroll[self.currentStage].page[i].ground, self.player)
                # if self.player.life < 0:
                #     self.gameMode = -10
                #     self.life -= 1life 
            # battle
            else:
                self.battle[self.currentStage].update(self.player)
                if self.player.life < 0:
                    self.player.life = 6
                    self.gameMode = -20
                    self.temp = self.time
                    self.life -= 1
            if self.player.alive == True:
                self.player.update()
            if self.battlePhase  == False and self.player.x > controlSize + 16 * 15 - self.player.speed and self.scroll[self.currentStage].page[0].x == controlSize +  (self.scroll[self.currentStage].pageNum - 1) * windowSizeX * (-1):
                self.battlePhase = True
            if self.battlePhase  == True and self.battle[self.currentStage].boss.damage == 0:
                if self.currentStage == 2:
                    self.gameMode = 2
                    self.endroll = self.Endroll("Game Clear")
                self.battlePhase = False
                self.currentStage += 1
                scrollSpeed = 2
            if self.life < 0:
                self.gameMode = -100
                self.endroll = self.Endroll("Game Over")
        elif self.gameMode == 2:
            self.gameMode = 3
        elif self.gameMode == 3 or self.gameMode == -100:
            self.endroll.update()
            if self.endroll.time > 550 and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 1, 1) and (controlSize <= pyxel.mouse_x <=  controlSize + windowSizeX):
                self.gameMode = -1
        elif self.gameMode == -1:
            self.reset()
            self.life = 5
            self.gameMode = 0
        elif self.gameMode == -10:
            if self.time > self.temp + 80:
                self.gameMode = 1
                self.scroll[self.currentStage] = self.Scroll(self.currentStage)
                self.battle[self.currentStage] = self.Battle(self.currentStage)
                self.player = self.Player()
                self.time = 0
                self.battlePhase = False
        elif self.gameMode == -20:
            if self.time > self.temp + 80:
                self.gameMode = 1
                self.scroll[self.currentStage] = self.Scroll(self.currentStage)
                self.battle[self.currentStage] = self.Battle(self.currentStage)
                self.player = self.Player()
                self.time = 0
                self.battlePhase = True
        self.time += 1

    def draw(self):
        # 全体背景
        pyxel.cls(7)
        if self.gameMode == 0 or self.gameMode == 1:
            # scroll
            if self.battlePhase == False:
                self.scroll[self.currentStage].draw()
            # battle
            else:
                self.battle[self.currentStage].draw(self.player)
            self.player.draw()
            if self.gameMode == 1:
                pyxel.rect(controlSize + 40 + 60, windowSizeY - 1 - 10, windowSizeX - 100, 10, 0)
                pyxel.rect(controlSize + 42 + 60, windowSizeY - 1 - 8, windowSizeX - 104, 6, 13)
                pyxel.rect(controlSize + 42 + 60, windowSizeY - 1 - 8, (windowSizeX - 104) / self.player.lifeMax * self.player.life, 6, 8)
        elif self.gameMode == 2:
            pass
        elif self.gameMode == 3 or self.gameMode == -100:
            self.endroll.draw()
        if self.gameMode == -10 or self.gameMode == -20:
            pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, 0)
            for i in range(self.life + 1):
                if i != self.life or (i == self.life and self.time % 10 > 5 and self.time < self.temp + 40):
                    pyxel.blt(controlSize + 16 * 4.5 + i * 20, 16 * 5, 0, 0, 0, 16, 16, 6)
            if self.time < self.temp + 80:
                pyxel.text(controlSize + 16 * 7.5, 16 * 6, "RETRY!!", 7)
        if self.gameMode == 0:
            pyxel.blt(controlSize, 0, 1, 0, 16 * 2, 16, 16, 1)
            if self.time % 10 > 5:
                pyxel.text(controlSize + 16 * 8, 16 * 8, "TAP TO START !!", 0)
        # 操作部分の背景（簡易的）
        pyxel.rect(0, 0, controlSize, windowSizeY, 7)
        pyxel.rect(controlSize + windowSizeX, 0, controlSize, windowSizeY, 7)
        pyxel.rect(0, 0, controlSize, windowSizeY / 4, 6)
        pyxel.rect(0, windowSizeY / 4, controlSize, windowSizeY / 2, 8)
        pyxel.rect(0, windowSizeY / 4 * 3, controlSize, windowSizeY / 4, 6)
        pyxel.rect(controlSize + windowSizeX, 0,controlSize, windowSizeY / 4, 6)
        pyxel.rect(controlSize + windowSizeX, windowSizeY / 4, controlSize, windowSizeY / 2, 1)
        pyxel.rect(controlSize + windowSizeX, windowSizeY / 4 * 3, controlSize, windowSizeY / 4, 6)
        # if self.scroll[self.currentStage].page[0].item:
        #     pyxel.text(0,0, str(self.scroll[self.currentStage].page[0].item[0].blockX), 0)
        #     pyxel.text(0,32, str(self.scroll[self.currentStage].page[0].item[0].y), 0)
        #     pyxel.text(0,48, str(self.scroll[self.currentStage].page[0].item[0].x + self.scroll[self.currentStage].page[0].item[0].blockX), 0)
        #     pyxel.text(0,56, str(controlSize + self.scroll[self.currentStage].page[0].item[0].blockX), 0)
        # pyxel.text(0,16, str( self.gameMode), 0)
        if self.gameMode == 1:
            pyxel.rect(0, 0, controlSize, 16 * 3, 0)
            pyxel.blt(0, 0, 0, 0, 0, 16, 16, 0)
            pyxel.text(18, 6, str(self.item[0]), 7)
            pyxel.blt(16 * 2, 0, 0, 0, 0, 16, 16, 0)
            pyxel.text(16 * 2 + 18, 6, str(self.item[1]), 7)
            pyxel.blt(16 * 4, 0, 0, 0, 0, 16, 16, 0)
            pyxel.text(16 * 4 + 18, 6, str(self.item[2]), 7)

    def Bump(self, player, scroll):
        pageNum = None
        placeNum = None
        for i in range(scroll.pageNum):
            for j in range(16):
                if pageNum == None and placeNum == None and scroll.page[i].x + j * 16 <= player.x <= scroll.page[i].x + (j + 1) * 16:
                    pageNum = i
                    placeNum = j
                    break
        # listX = []
        # listY = []
        # for i in scroll.page[pageNum].block:
        #     for j in range(i.amount):
        #         if i.blockX[j] < player.x < i.blockX[j] + 16 and i.blockY < player.y + player.force + 16 < i.blockY + 16:
        #             listX.append(i.blockX[j])
        #             listY.append(i.blockY)
        if self.battlePhase == False:
            self.BlockHEAD(player, scroll.page[pageNum])
            self.BlockASS(player, scroll.page[pageNum])
            self.BlockSIDE(player, scroll.page[pageNum])


        # if scroll.page[pageNum].block[0].blockY #player.yが０〜scroll.page[pageNum].block[0].blockY-16の時の終了判定
        # if windowSizeY - 16 #player.yがscroll.page[pageNum].block[0].blockY+ 16 〜の時の終了判定

    def BlockHEAD(self, player, page):
        flag = True
        for i in page.block:
            for j in range(i.amount):
                if i.blockX[j] < player.x < i.blockX[j] + 16 and i.blockY - 6 < player.y + 16 + player.force < i.blockY + 6 and player.y + 16 <= i.blockY:
                    player.canJump = 2
                    player.y = i.blockY - 16
                    player.grandY = i.blockY - 16
                    player.isFall = False
                    player.force = 0
                    flag = False
                    break
        if flag:
            player.isFall = True
    def BlockASS(self, player, page):
        for i in page.block:
            for j in range(i.amount):
                if i.blockX[j] < player.x < i.blockX[j] + 16 and i.blockY + 10 < player.y + player.force < i.blockY + 16 and player.y >= i.blockY + 16:
                    player.force = 0.5
                    player.isFall = True
                    break

    def BlockSIDE(self, player, page):
        for i in page.block:
            for j in range(i.amount):
                if i.blockX[j] < player.x + 16  + playerSpeed < i.blockX[j] + 16 and i.blockY < player.y + 16 < i.blockY + 16:
                    player.x = i.blockX[j] - 16 - scrollSpeed
                    player.canMove[0] = False
                    break
                elif i.blockX[j] > player.x + 16 + playerSpeed > i.blockX[j] + 16 and i.blockY < player.y + 16 < i.blockY + 16:
                    player.x = i.blockX[j] + 16 - scrollSpeed
                    player.canMove[1] = False
                    break
                else:
                    player.canMove = [True, True]

    def HoleDown(self, hole, player):
        if player.alive == True and player.y == windowSizeY - 32 and hole.holeX + 4 < player.x < hole.holeX + 16 - 4:
            player.alive = False
        if  player.alive == False:
            player.y += 0.2
            if self.gameMode != -10 and player.y > windowSizeY:
                self.gameMode = -10
                self.life -= 1
                self.temp = self.time

    def CoinGet(self, coin, player):
        if coin.coinGet == False and coin.coinX - 16 < player.x < coin.coinX + 16 and coin.coinY - 16 < player.y < coin.coinY + 16:
            player.life += 1
            if player.life > 18:
                player.life = 18
            coin.coinGet = True

    def EnemyBump(self, enemy, player):
        if enemy.enemyGet == False and enemy.enemyX - 16 < player.x < enemy.enemyX + 16 and enemy.enemyY - 16 < player.y < enemy.enemyY + 16:
            player.life -= 1
            if player.life < 0:
                player.life = 0
            enemy.enemyGet = True

    def BlockToItem(self, block, player, page):
        for i in range(block.amount):
            if player.force < 0 and block.blockX[i] - 15 < player.x < block.blockX[i] + 15 and block.blockY + 16 > player.y + player.force > block.blockY:
                player.y = block.blockY + 16
                player.force = 0
                if block.blockItem[i] == True:
                    block.blockItem[i] = False
                    page.itemNum += 1
                    page.item.append(page.Item(page.x, block.blockY, block.blockX[i]))
                    block.imageX[i] = 16 * 3
                # player.isFall = True

    def ItemGet(self, player, item):
        if item.itemGet == False and item.blockX - 16 < player.x < item.blockX + 16 and item.y - 16 < player.y < item.y + 16:
            item.itemGet = True
            self.item[self.currentStage] += 1

    def reset(self):
        self.stageNum = 3
        # 今何ステージ目か
        # self.currentStage = 0
        # ステージ内のバトルフェーズか（False=scroll, True=battle）
        # self.battlePhase = True
        self.battlePhase = False
        # scrolllインスタンス化
        for i in range(self.stageNum):
            self.scroll[i] = self.Scroll(i)
        # battleインスタンス化
        for i in range(self.stageNum):
            self.battle[i] = self.Battle(i)
        # playerインスタンス化
        self.player = self.Player()
        # gameModeの選択
        # 0:スタート画面
        # 1:gameplay時
        # 2:clear画面
        # 3:endroll
        # -1 :reset
        # -10:gameOver時
        self.gameMode = 0
        self.endroll = self.Endroll("Game Clear")
        self.time = 0
        self.temp = 0

    def start(self):
        self.stageNum = 3
        # 今何ステージ目か
        self.currentStage = 0
        # ステージ内のバトルフェーズか（False=scroll, True=battle）
        # self.battlePhase = True
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
        # playerインスタンス化
        self.player = self.Player()
        # gameModeの選択
        # 0:スタート画面
        # 1:gameplay時
        # 2:clear画面
        # 3:endroll
        # -1 :reset
        # -10:gameOver時
        self.gameMode = 0
        self.endroll = self.Endroll("Game Clear")
        self.time = 0
        self.temp = 0
        self.item = [0, 0, 0]

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
            self.JUMP_FORCE = -8
            self.canJump = 2
            self.y_prev = self.y
            self.scrollspeed = scrollSpeed
            self.isFall = False
            self.isStun = False
            self.canMove = [True, True]
            self.life = 6
            self.alive = True
            self.lifeMax = 18

        def move(self):
            if self.isStun == False:
                self.imageX = 0
                if pyxel.btn(pyxel.KEY_LEFT) and self.x > controlSize and self.canMove[1] == True:
                    self.image = 2
                    self.x -= self.speed
                if pyxel.btn(pyxel.KEY_RIGHT) and self.canMove[0] == True:
                    self.image = 1
                    if self.x < controlSize + windowSizeX - self.imageWidth:
                        self.x += self.speed
                if pyxel.btn(pyxel.KEY_LEFT) == False and pyxel.btn(pyxel.KEY_RIGHT) == False:
                    self.image = 0
            else:
                self.image = 1
                self.imageX = 16

        def jump(self):
            if self.isStun == False:
                if (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump == 2:
                    self.canJump = 1
                    self.force = self.JUMP_FORCE
                    self.isFall = False
                elif (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump == 1 and self.force >= -2:
                    self.canJump = 0
                    self.force = self.JUMP_FORCE
                    self.isFall = False
                if self.canJump == 1:
                    if self.force <= 0:
                        self.y += self.force
                        self.force += 0.5
                    if self.force == 0:
                        self.isFall = True
                    if self.y >= self.groundY:
                        self.y = self.groundY
                        self.canJump = 2
                        self.isFall = False
                elif self.canJump == 0:
                    if self.force <= 0:
                        self.y += self.force
                        self.force += 0.5
                    if self.force == 0:
                        self.isFall = True
                    if self.y >= self.groundY:
                        self.y = self.groundY
                        self.canJump = 2
                        self.isFall = False

        def fall(self):
            self.y += self.force
            self.force += 0.5
            if self.y >= self.groundY:
                self.y = self.groundY
                self.canJump = 2
                self.isFall = False



        # def jump(self):
        #     if self.isStun == False:
        #         if (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump[0]:
        #             self.canJump[0] = False
        #             self.force = self.JUMP_FORCE
        #             self.isFall = False
        #         if (Button() == 10 or pyxel.btn(pyxel.KEY_SPACE)) and self.canJump[1] and self.force >= -2:
        #             self.canJump[1] = False
        #             self.force = self.JUMP_FORCE
        #             self.isFall = False
        #         if self.canJump[0] == False and self.canJump[1] == True:
        #             self.y += self.force
        #             self.force += 1
        #             if self.y >= self.groundY:
        #                 self.y = self.groundY
        #                 self.canJump[0] = True
        #                 self.isFall = True
        #         if self.canJump[1] == False and self.canJump[0] == False:
        #             self.y += self.force
        #             self.force += 1
        #             if self.y >= self.groundY:
        #                 self.y = self.groundY
        #                 self.canJump = [True, True]
        #                 self.isFall = True

        # def fall(self):
        #     self.y += self.force
        #     self.force += 1
        #     if self.y + self.force >= self.grandY:
        #         self.y = self.grandY
        #         self.canJump = [True, True]
        #         self.isFall = False

        def update(self):
            if self.x - scrollSpeed > controlSize:
                self.x -= scrollSpeed
            self.move()
            self.jump()
            if self.isFall:
                self.fall()

        def draw(self):
            pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY,self.imageWidth, self.imageHeight, self.imageColor)
            # pyxel.text(controlSize, 0, str(self.isStun), 0)

    class Scroll:
        def __init__(self, stageNum):
            # スクロールが全部で何ページか
            self.pageNum = 6
            # pageが全部で何ページか
            self.page = []
            for i in range(self.pageNum):
                self.page.append(self.Page(stageNum, i))
            self.speed = scrollSpeed
            if stageNum == 0:
                self.back_image = 12
                self.ground_image = 11
            elif stageNum == 1:
                self.back_image = 14
                self.ground_image = 8
            elif stageNum == 2:
                self.back_image = 5
                self.ground_image = 12

        def update(self, stageNum):
            global scrollSpeed
            if self.page[0].x - self.speed < controlSize + (self.pageNum - 1) * windowSizeX * (-1):
                self.page[0].x = controlSize + (self.pageNum - 1) * windowSizeX * (-1)
                scrollSpeed = 0
            self.speed = scrollSpeed
            for i in range(self.pageNum):
                self.page[i].update(stageNum)

        def draw(self):
            # action部分の背景
            pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, self.back_image)
            # 床（固定）
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, self.ground_image)
            # 縦線つけてるだけだよ〜〜
            for i in range(self.pageNum):
                self.page[i].draw(i)
                for j in range(16):
                    pyxel.rect(self.page[i].x + 16 * j, 0, 1, windowSizeY, 0)
                    pyxel.rect(self.page[i].x, 0, 1, windowSizeY, 8)
            

        class Page:
            def __init__(self, stageNum, pageNum):
                global scrollSpeed
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
                    self.staticCoin.append(self.StaticCoin(stageNum, self.x, self.same))
                    self.same.append(self.staticCoin[i].coin)
                self.enemy = []
                self.enemyNum = 2
                if stageNum == 1 or stageNum == 2:
                    for i in range(self.enemyNum):
                        self.enemy.append(self.Enemy(stageNum, self.x, self.same))
                self.item = []
                self.itemNum = 0
                # 床の動くスピード
                self.speed = 0

            def update(self, stageNum):
                global scrollSpeed
                if stageNum == 2 and scrollSpeed != 0:
                    scrollSpeed = 3
                self.speed = scrollSpeed
                self.x -= self.speed
                self.ground.update(self.x)
                for i in range(self.blockNum):
                    self.block[i].update(self.x)
                for i in range(self.coinNum):
                    self.staticCoin[i].update(self.x)
                if self.enemy:
                    for i in range(self.enemyNum):
                        self.enemy[i].update(self.x)
                if self.item:
                    for i in range(self.itemNum):
                        self.item[i].update(self.x)

            def draw(self, pageNum):
                # pageの切り替わりがわかるように
                # pyxel.rect(self.x, 0, 8, windowSizeY, 0)
                self.ground.draw()
                if self.item:
                    for i in range(self.itemNum):
                        self.item[i].draw()
                for i in range(self.blockNum):
                    self.block[i].draw()
                for i in range(self.coinNum):
                    self.staticCoin[i].draw()
                if self.enemy:
                    for i in range(self.enemyNum):
                        self.enemy[i].draw()
                if pageNum == 5:
                    pyxel.blt(self.x + 16 * 15, 16, 0, 16 * 4, 0, 16, 16, 6);
                    for i in range(8):
                        pyxel.blt(self.x + 16 * 15, 32 + i * 16, 0, 16 * 4, 16, 16, 16, 6);
                    pyxel.blt(self.x + 16 * 15, 16 * 10, 0, 16 * 2, 0, 16, 16, 6);

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
                    self.hole = pyxel.rndi(6, 13)
                    self.holeX = x + self.hole * 16
                    if stageNum == 0:
                        self.hole_image = 12
                        self.grass_image = 3
                    elif stageNum == 1:
                        self.hole_image = 14
                        self.grass_image = 2
                    elif stageNum == 2:
                        self.hole_image = 5
                        self.grass_image = 1

                def update(self, x):
                    self.x = x
                    self.holeX = x + self.hole * 16

                def draw(self):
                    # 床（固定）
                    for i in range(self.grassFineness):
                        pyxel.rect(self.x + i * windowSizeX / self.grassFineness, windowSizeY -
                                   16, windowSizeX / self.grassFineness,  self.grass[i], self.grass_image)
                    # 穴（固定)
                    pyxel.rect(self.holeX, windowSizeY - 16, 16 * 2,  16, self.hole_image)

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
                    self.imageX = []
                    for i in range(self.amount):
                        self.blockX.append(x + (self.start + i) * 16)
                        if pyxel.rndi(0, 1) == 0 and i != 0 and self.blockItem[i - 1] != True:
                            self.blockItem.append(True)
                            self.imageX.append(16)
                        else:
                            self.blockItem.append(False)
                            self.imageX.append(16 * 2)
                    self.blockY = pyxel.rndi(5, 9) * 16

                def update(self, x):
                    self.x = x
                    for i in range(self.amount):
                        self.blockX[i] = x + (self.start + i) * 16

                def draw(self):
                    for i in range(self.amount):
                        pyxel.blt( self.blockX[i], self.blockY, 0, self.imageX[i], 0, 16, 16, 6)

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

            class Enemy:
                def __init__(self, stageNum, x, same):
                    # ページの右端x
                    self.x = x
                    self.enemy = pyxel.rndi(1, 13)
                    temp = 0
                    # 被らないように調節
                    while temp != len(same):
                        for s in same:
                            if self.enemy != s:
                                temp += 1
                            else:
                                temp = 0
                                self.enemy = pyxel.rndi(1, 13)
                                break
                    self.enemyX = x + self.enemy * 16
                    self.enemyY = pyxel.rndi(1, 9) * 16
                    self.enemyGet = False

                def update(self, x):
                    self.x = x
                    self.enemyX = x + self.enemy * 16

                def draw(self):
                    if self.enemyGet == False:
                        pyxel.blt(self.enemyX, self.enemyY, 0, 16 * 2, 16 * 5, 16, 16, 6)

            class Item:
                def __init__(self, x, y, blockX):
                    self.image = 0
                    self.imageX = 0
                    self.imageY = 0
                    self.imageWidth = 16
                    self.imageHeight = 16
                    self.imageColor = 6
                    self.x = x
                    self.y = y
                    self.blockX = blockX
                    self.temp = y - 16
                    self.itemGet = False

                def update(self, x):
                    self.blockX -= scrollSpeed
                    if self.temp != self.y:
                        self.y -= 0.5

                def draw(self):
                    if self.itemGet == False:
                        pyxel.blt(self.blockX, self.y, self.image, self.imageX, self.imageY, self.imageWidth, self.imageHeight, self.imageColor)

    class Battle:
        def __init__(self, stageNum):
            self.boss = self.Boss(stageNum)
            self.time = 0
            if stageNum == 0:
                self.back_image = 12
                self.ground_image = 11
            elif stageNum == 1:
                self.back_image = 14
                self.ground_image = 8
            elif stageNum == 2:
                self.back_image = 5
                self.ground_image = 12

        def update(self, player):
            # if self.time == 0:
            #     self.lifeMax = player.life
            self.playerMoveCheck(player)
            self.boss.update(player)
            self.time += 1

            # elif self.fireFlag == True:
            # elif self.beamFlag == True:

        def draw(self, player):
            pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, self.back_image)
            self.boss.draw()
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, self.ground_image)
            # pyxel.text(controlSize, 16, str(self.boss.y - player.imageHeight < player.y < self.boss.y + self.boss.imageHeight), 0)
            # bossのライフ管理　TODO いる？
            pyxel.rect(controlSize + 40, 10, windowSizeX - 80, 10, 0)
            pyxel.rect(controlSize + 42, 12, windowSizeX - 84, 6, 5)
            pyxel.rect(controlSize + 42, 12, (windowSizeX - 84) / 3 * self.boss.damage, 6, 8)

        def playerMoveCheck(self, player):
            if player.x + player.speed + player.imageWidth > self.boss.x and player.x < self.boss.x and self.boss.y - player.imageHeight < player.y < self.boss.y + self.boss.imageHeight:
                player.canMove[0] = False
            else:
                player.canMove[0] = True
            if player.x - player.speed < self.boss.x + self.boss.imageWidth and player.x > self.boss.x and self.boss.y - player.imageHeight < player.y < self.boss.y + self.boss.imageHeight:
                player.canMove[1] = False
            else:
                player.canMove[1] = True

        class Boss:
            def __init__(self, stageNum):
                self.image = 0
                self.imageWidth = 32
                self.imageHeight = 32
                self.imageColor = 6
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
                self.damage = 3
                self.isDead = False
                self.temp = 0
                self.lifeReduce = 0
                self.reduce = False
                self.reduceTime = 0
                if stageNum == 0:
                    self.imageX = 0
                    self.imageY = 48
                elif stageNum == 1:
                    self.imageX = 32
                    self.imageY = 48
                elif stageNum == 2:
                    self.imageX = 0
                    self.imageY = 80

            def update(self, player):
                if self.reduce == False:
                    if self.time % 120 == 0 and self.action == False:
                        self.action = True
                        bossAction = pyxel.rndi(0,10)
                        # bossAction = 7
                        if bossAction < 3:
                            self.jumpFlag = True
                        elif bossAction < 6:
                            self.stunFlag = True
                        elif bossAction < 8:
                            self.fireFlag = True
                        elif bossAction <= 10:
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
                        self.moveRL(player)
                    self.be_stamp( player)
                    self.be_damage(player)
                else:
                    self.stunTime += 1
                    if self.reduceTime == 0:
                        self.x -= 4
                        self.y -= 1
                    if self.x < controlSize + 8 or self.reduceTime != 0:
                        self.reduceTime += 1
                    if self.reduceTime >= 10 and self.y != self.groundY:
                        self.y += 5
                        if self.y >= self.groundY:
                            self.y = self.groundY
                            self.stunTime = 0
                    if self.stunTime >= 10 and  self.y == self.groundY:
                        self.reduce = False
                        self.reduceTime = 0
                        self.stunTime = 0
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
                            if player.y == self.groundY + self.imageHeight - player.imageHeight:
                                player.isStun = True
                        if self.stunStayTime != 0 and self.stunStayTime < 20:
                            self.stunTime += 1
                        if self.stunStayTime >= 40:
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
                        self.beamSpeed = 10
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
                        self.action = False
                    self.beamTime += 1

            def be_damage(self, player):
                if self.lifeReduce == 0:
                    if self.jumpFlag == True:
                        pass
                        # 通常時と同じ挙動
                    elif self.stunFlag == True:
                        pass
                        # stun内に記述
                    elif self.fireFlag == True:
                        if (self.y - player.y) * (self.y - player.y) + (self.x - player.x) * (self.x - player.x) <= self.fireSize[0] * self.fireSize[0]:
                            player.life -= 1
                            self.lifeReduce = 1
                            player.isStun = True
                    elif self.beamFlag == True:
                        if self.groundY + self.imageHeight - player.imageHeight - 16 <= player.y <= self.groundY + self.imageHeight - player.imageHeight:
                            if self.beamDirection == 0 and self.x < player.x < self.x + self.beamSize - 10:
                                player.life -= 1
                                self.lifeReduce = 1
                                player.isStun = True
                            elif self.beamDirection == 1 and self.x - self.beamSize + 10 < player.x < self.x:
                                player.life -= 1
                                self.lifeReduce = 1
                                player.isStun = True
                    if self.y - player.imageHeight / 2 < player.y < self.y + self.imageHeight - player.imageHeight / 2 and self.x - player.imageWidth < player.x < self.x + self.imageWidth:
                        player.life -= 1
                        self.lifeReduce = 1
                        player.isStun = True
                if self.lifeReduce != 0:
                    self.lifeReduce += 1
                    if self.lifeReduce >= 30:
                        self.lifeReduce = 0
                        player.isStun = False

            def be_stamp(self, player):
                if self.lifeReduce == 0 and self.x - self.imageWidth / 3 < player.x and player.x + player.imageWidth < self.x + self.imageWidth / 3 * 4 and self.y - player.imageHeight * 2 < player.y < self.y:
                    self.damage -= 1
                    self.lifeReduce = 1
                    self.reduce = True
                    self.temp = self.x
                    if self.damage == 0:
                        self.isDead = True

            def moveRL(self, player):
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
                if self.fireFlag == True:
                    for size in self.fireSize:
                        for x in range(36):
                            pyxel.blt(self.x + self.imageWidth / 2 + math.cos(x * 10) * size - 8 , self.y + self.imageHeight / 2 + math.sin(x * 10) * size - 8,self.image, self.imageX + 16 , self.imageY + 64, 16, 16, self.imageColor)
                        # pyxel.circ(self.x + self.imageWidth / 2 , self.y + self.imageHeight / 2, size, 0)
                if self.beamDirection == 0:
                    for i in range(int(self.beamSize / 16)):
                        pyxel.blt(self.x - 16  + self.imageWidth + i * 16, self.y + 12, self.image, self.imageX, self.imageY + 64 , 16, 16, self.imageColor)
                    pyxel.blt(self.x - 16 + self.imageWidth + int(self.beamSize / 16) * 16, self.y + 12, self.image, self.imageX, self.imageY + 64, self.beamSize - int(self.beamSize / 16) * 16, 16, self.imageColor)
                elif self.beamDirection == 1:
                    for i in range(int(self.beamSize / 16)):
                        pyxel.blt(self.x - i * 16, self.y + 12, self.image, self.imageX, self.imageY + 64, 16, 16, self.imageColor)
                    pyxel.blt(self.x - self.beamSize + 16, self.y + 12, self.image, self.imageX, self.imageY + 64, self.beamSize - int(self.beamSize / 16) * 16, 16, self.imageColor)
                pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY, self.imageWidth, self.imageHeight, self.imageColor)
                # pyxel.text(controlSize, 16, str(self.stunTime), 0)

    class Endroll:
        def __init__(self, str):
            self.time = 0
            self.commend_0 = -16
            self.commend_1 = -32
            self.commend_2 = -16
            self.commend_3 = -16
            self.str = str

        def update(self):
            if 0 <= self.time < 160:
                self.commend_0 += 1.5
            elif 160 <= self.time < 320:
                self.commend_1 += 1.5
            elif 320 <= self.time < 480:
                self.commend_2 += 1.5
            elif 480 <= self.time < 550:
                self.commend_3 += 1.5
            self.time += 1

        def draw(self):
            pyxel.rect(controlSize, 0, windowSizeX, windowSizeY, 0)
            if 0 <= self.time < 160:
                pyxel.text(controlSize + 16 * 6.3, self.commend_0, str(self.str), 7)
            elif 160 <= self.time < 320:
                pyxel.text(controlSize + 16 * 6.3, self.commend_1, "creater : tsola", 7)
                pyxel.text(controlSize + 16 * 6.3, self.commend_1 + 16, "          tayuuki", 7)
            elif 320 <= self.time < 480:
                pyxel.text(controlSize + 16 * 5.9, self.commend_2, "painter : tayuuki", 7)
            elif 480 <= self.time:
                pyxel.text(controlSize + 16 * 4.9, self.commend_3, "Thank You For Playing!!", 7)
                if (self.time > 550 and self.time % 10 < 5) or (480 <= self.time < 550):
                    pyxel.text(controlSize + 16 * 5.4, self.commend_3 + 16, "Press To Back HOME", 7)

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
