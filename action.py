import pyxel

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12


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
        pyxel.run(self.update, self.draw)

    def update(self):
        # scroll
        if self.battlePhase == False:
            self.scroll[self.currentStage].update()
        # battle
        else:
            self.battle[self.currentStage].update()


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
        pyxel.text(0, 0, str(self.scroll[0].page[0].block[0].blockXNum), 0)
        pyxel.text(0, 16, str(self.scroll[0].page[0].block[1].blockXNum), 0)

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
                    self.same.append(self.block[i].blockXNum)
                # 床の動くスピード
                self.speed = 1

            def update(self):
                self.x -= self.speed
                self.ground.update(self.x)
                for i in range(self.blockNum):
                    self.block[i].update(self.x)

            def draw(self):
                #pageの切り替わりがわかるように
                pyxel.rect(self.x, 0, 8, windowSizeY, 0)
                self.ground.draw()
                for i in range(self.blockNum):
                    self.block[i].draw()

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
                    self.holeX = self.hole * 16

                def update(self, x):
                    self.x = x

                def draw(self):
                    # 床（固定）
                    for i in range(self.grassFineness):
                        pyxel.rect(self.x + i * windowSizeX / self.grassFineness, windowSizeY - 16, windowSizeX / self.grassFineness,  self.grass[i], 3)
                    # 穴（固定)
                    pyxel.rect(self.x + self.holeX, windowSizeY - 16, 16 * 2,  16, 12)

            class Block:
                def __init__(self, stageNum, x, same):
                    # ページの右端x
                    self.x = x
                    self.temp = 0
                    #blockが横に何個続くか
                    self.blockWidth = 2
                    # blockが何マス目にあるか
                    self.blockXNum = pyxel.rndi(1, 13)
                    #被らないように調節
                    while self.temp != len(same):
                        for s in same:
                            if self.blockXNum != s and self.blockXNum != s + 1:
                                self.temp += 1
                            else:
                                self.temp = 0
                                self.blockXNum = pyxel.rndi(1, 13)
                                break
                    # blockのx座標
                    self.blockX = []
                    for i in range(self.blockWidth):
                        self.blockX.append((self.blockXNum + i) * 16)
                    # blockが上から何マス目にあるか
                    self.blockYNum = pyxel.rndi(5, 9)
                    # blockのy座標
                    self.blockY = self.blockYNum * 16

                def update(self, x):
                    self.x = x

                def draw(self):
                    #TODO itemの絵を入れるとりあえず四角で表記
                    for i in range(self.blockWidth):
                        pyxel.rect(self.x + self.blockX[i], self.blockY, 16, 16, 8)

    class Battle:

        def __init__(self, stageNum):
            pass

        def update(self):
            pass

        def draw(self):
            pass

App()
