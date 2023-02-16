import pyxel

controlSize = 16 * 6
windowSizeX = 16 * 16
windowSizeY = 16 * 12


class App:
    def __init__(self):
        pyxel.init(windowSizeX + controlSize * 2, windowSizeY, fps=1)
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

    class Scroll:
        def __init__(self, stageNum):
            #スクロールが全部で何ページか
            self.pageNum = 1
            # pageが全部で何ページか
            self.page = []
            for i in range(self.pageNum):
                self.page.append(self.Page(stageNum, i))

        def update(self):
            pass

        def draw(self):
            # 床（固定）
            pyxel.rect(controlSize, windowSizeY - 16, windowSizeX, 16, 11)
            for i in range(self.pageNum):
                self.page[0].draw()

        class Page:
            def __init__(self, stageNum, pageNum):
                self.x = pageNum * windowSizeX
                self.ground = self.Ground(stageNum, self.x)

            def update(self):
                pass

            def draw(self):
                self.ground.draw()

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
                    self.holeX = self.x + pyxel.rndi(1, 13) * 16

                def update(self):
                    pass

                def draw(self):
                    # 床（固定）
                    for i in range(self.grassFineness):
                        pyxel.rect(self.x + controlSize + i * windowSizeX / self.grassFineness, windowSizeY - 16, windowSizeX / self.grassFineness,  self.grass[i], 3)
                    pyxel.rect(controlSize + self.holeX, windowSizeY - 16, 16 * 2,  16, 12)

    class Battle:

        def __init__(self, stageNum):
            pass

        def update(self):
            pass

        def draw(self):
            pass

App()
