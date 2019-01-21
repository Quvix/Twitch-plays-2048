import pyglet
import random


class GameArea:
    TILE_SIZE = 100
    LINE_WIDTH = 6
    FONT_SIZE = 20
    GRID_SIZE = 4

    def __init__(self, window, posx, posy):
        self.window = window
        self.posx = posx
        self.posy = posy
        self.players = []
        self.newHighscore = False

        with open('highscore.dat', 'r') as content_file:
            self.highscore = int(content_file.read())
        self.reset()

        self.label = pyglet.text.Label('2048',
                                       font_name='Arial',
                                       bold=True,
                                       font_size=GameArea.FONT_SIZE,
                                       x=30 // 2, y=window.height - 10 // 2,
                                       anchor_x='center', anchor_y='center')

        self.scoreValueText = pyglet.text.Label('0',
                                                font_name='Arial',
                                                bold=True,
                                                font_size=GameArea.FONT_SIZE + 2,
                                                x=self.posx + GameArea.TILE_SIZE // 2,
                                                y=self.posy + 30,
                                                anchor_x='center', anchor_y='center')

        self.scoreText = pyglet.text.Label('Score',
                                           font_name='Arial',
                                           bold=False,
                                           font_size=GameArea.FONT_SIZE - 2,
                                           x=self.posx + GameArea.TILE_SIZE // 2,
                                           y=self.posy + 58,
                                           anchor_x='center', anchor_y='center')

        self.highscoreValueText = pyglet.text.Label('0',
                                                    font_name='Arial',
                                                    bold=True,
                                                    font_size=GameArea.FONT_SIZE + 2,
                                                    x=self.posx + ((
                                                                           GameArea.GRID_SIZE - 1) * GameArea.TILE_SIZE) + GameArea.TILE_SIZE // 2,
                                                    y=self.posy + 30,
                                                    anchor_x='center', anchor_y='center')

        self.highscoreText = pyglet.text.Label('Highscore',
                                               font_name='Arial',
                                               bold=False,
                                               font_size=GameArea.FONT_SIZE - 2,
                                               x=self.posx + ((
                                                                      GameArea.GRID_SIZE - 1) * GameArea.TILE_SIZE) + GameArea.TILE_SIZE // 2,
                                               y=self.posy + 58,
                                               anchor_x='center', anchor_y='center')

    def reset(self):
        if self.newHighscore:
            self.saveHighscore()
            self.newHighscore = False
        self.grid = [[0 for i in range(GameArea.GRID_SIZE)] for j in range(GameArea.GRID_SIZE)]
        self.spawnRandom()
        self.spawnRandom()
        self.score = 0
        self.players = []

    def saveHighscore(self):
        text_file = open("highscore.dat", "w")
        text_file.write(str(self.highscore))
        text_file.close()
        self.savePlayers()

    def addAuthor(self, username):
        self.players.append(username)

    def savePlayers(self):
        result = ', '.join(set(self.players)) + '    '
        text_file = open("players.txt", "w", encoding='utf8')
        text_file.write(result)
        text_file.close()

    def draw(self):
        self.scoreValueText.text = str(self.score)
        self.scoreText.draw()
        self.scoreValueText.draw()

        if(self.score > self.highscore):
            self.highscore = self.score
            self.newHighscore = True

        self.highscoreValueText.text = str(self.highscore)
        self.highscoreText.draw()
        self.highscoreValueText.draw()

        self.drawGrid()
        for i in range(GameArea.GRID_SIZE):
            for j in range(GameArea.GRID_SIZE):
                self.label.x = self.posx + GameArea.TILE_SIZE * i + GameArea.TILE_SIZE // 2
                self.label.y = self.posy - GameArea.TILE_SIZE * j - GameArea.TILE_SIZE // 2
                self.label.text = str(self.grid[i][j])
                if self.label.text != '0':
                    self.label.draw()

    def drawGrid(self):
        pyglet.gl.glLineWidth(GameArea.LINE_WIDTH)
        for i in range(GameArea.GRID_SIZE + 1):
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (
            self.posx + i * GameArea.TILE_SIZE, self.posy + GameArea.LINE_WIDTH // 2,
            self.posx + i * GameArea.TILE_SIZE,
            self.posy - GameArea.TILE_SIZE * GameArea.GRID_SIZE - GameArea.LINE_WIDTH // 2)))
            pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (
            self.posx, self.posy - i * GameArea.TILE_SIZE, self.posx + GameArea.TILE_SIZE * GameArea.GRID_SIZE,
            self.posy - i * GameArea.TILE_SIZE)))

    def update(self):
        self.moveLeft()
        self.moveDown()
        self.addAuthor('Quvix')
        self.addAuthor('Tvoje máma')

    def spawnRandom(self):
        if not self.isFull():
            while True:
                x = random.randint(0, GameArea.GRID_SIZE - 1)
                y = random.randint(0, GameArea.GRID_SIZE - 1)
                if (self.grid[x][y] == 0):
                    self.grid[x][y] = random.randint(1, 2)
                    break

    def old_moveLeft(self):
        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                pos = i
                while pos > 0:
                    if self.grid[pos - 1][j] == 0:
                        self.grid[pos - 1][j] = self.grid[pos][j]
                        self.grid[pos][j] = 0
                        pos -= 1
                    elif self.grid[pos - 1][j] == self.grid[pos][j]:
                        self.grid[pos - 1][j] *= 2
                        self.grid[pos][j] = 0
                        pos -= 1
                    else:
                        break
        self.spawnRandom()

    def moveLeft(self):
        to_collapse = []

        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                pos = i
                while pos > 0:
                    if self.grid[pos - 1][j] == 0:
                        self.grid[pos - 1][j] = self.grid[pos][j]
                        self.grid[pos][j] = 0
                        pos -= 1
                    else:
                        break

        for j in range(0, GameArea.GRID_SIZE):
            pos = 1
            while pos < GameArea.GRID_SIZE:
                if self.grid[pos - 1][j] == self.grid[pos][j]:
                    to_collapse.append((pos, j))
                    pos += 2
                else:
                    pos += 1

        for item in to_collapse:
            self.grid[item[0] - 1][item[1]] *= 2
            self.grid[item[0]][item[1]] = 0
            self.score += self.grid[item[0] - 1][item[1]]

        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                pos = i
                while pos > 0:
                    if self.grid[pos - 1][j] == 0:
                        self.grid[pos - 1][j] = self.grid[pos][j]
                        self.grid[pos][j] = 0
                        pos -= 1
                    else:
                        break

        self.spawnRandom()

    def moveRight(self):
        to_collapse = []

        for i in range(GameArea.GRID_SIZE - 1, -1, -1):
            for j in range(GameArea.GRID_SIZE - 1, -1, -1):
                pos = i
                while pos < GameArea.GRID_SIZE - 1:
                    if self.grid[pos + 1][j] == 0:
                        self.grid[pos + 1][j] = self.grid[pos][j]
                        self.grid[pos][j] = 0
                        pos += 1
                    else:
                        break

        for j in range(GameArea.GRID_SIZE - 1, -1, -1):
            pos = GameArea.GRID_SIZE - 2
            while pos >= 0:
                if self.grid[pos + 1][j] == self.grid[pos][j]:
                    to_collapse.append((pos, j))
                    pos -= 2
                else:
                    pos -= 1

        for item in to_collapse:
            self.grid[item[0] + 1][item[1]] *= 2
            self.grid[item[0]][item[1]] = 0
            self.score += self.grid[item[0] + 1][item[1]]

        for i in range(GameArea.GRID_SIZE - 1, -1, -1):
            for j in range(GameArea.GRID_SIZE - 1, -1, -1):
                pos = i
                while pos < GameArea.GRID_SIZE - 1:
                    if self.grid[pos + 1][j] == 0:
                        self.grid[pos + 1][j] = self.grid[pos][j]
                        self.grid[pos][j] = 0
                        pos += 1
                    else:
                        break

        self.spawnRandom()

    def moveUp(self):
        to_collapse = []

        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                pos = j
                while pos > 0:
                    if self.grid[i][pos - 1] == 0:
                        self.grid[i][pos - 1] = self.grid[i][pos]
                        self.grid[i][pos] = 0
                        pos -= 1
                    else:
                        break

        for i in range(0, GameArea.GRID_SIZE):
            pos = 1
            while pos < GameArea.GRID_SIZE:
                if self.grid[i][pos - 1] == self.grid[i][pos]:
                    to_collapse.append((i, pos))
                    pos += 2
                else:
                    pos += 1

        for item in to_collapse:
            self.grid[item[0]][item[1] - 1] *= 2
            self.grid[item[0]][item[1]] = 0
            self.score += self.grid[item[0]][item[1] - 1]

        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                pos = j
                while pos > 0:
                    if self.grid[i][pos - 1] == 0:
                        self.grid[i][pos - 1] = self.grid[i][pos]
                        self.grid[i][pos] = 0
                        pos -= 1
                    else:
                        break

        self.spawnRandom()

    def moveDown(self):
        to_collapse = []

        for i in range(GameArea.GRID_SIZE - 1, -1, -1):
            for j in range(GameArea.GRID_SIZE - 1, -1, -1):
                pos = j
                while pos < GameArea.GRID_SIZE - 1:
                    if self.grid[i][pos + 1] == 0:
                        self.grid[i][pos + 1] = self.grid[i][pos]
                        self.grid[i][pos] = 0
                        pos += 1
                    else:
                        break

        for i in range(GameArea.GRID_SIZE - 1, -1, -1):
            pos = GameArea.GRID_SIZE - 2
            while pos >= 0:
                if self.grid[i][pos + 1] == self.grid[i][pos]:
                    to_collapse.append((i, pos))
                    pos -= 2
                else:
                    pos -= 1

        for item in to_collapse:
            self.grid[item[0]][item[1] + 1] *= 2
            self.grid[item[0]][item[1]] = 0
            self.score += self.grid[item[0]][item[1] + 1]

        for i in range(GameArea.GRID_SIZE - 1, -1, -1):
            for j in range(GameArea.GRID_SIZE - 1, -1, -1):
                pos = j
                while pos < GameArea.GRID_SIZE - 1:
                    if self.grid[i][pos + 1] == 0:
                        self.grid[i][pos + 1] = self.grid[i][pos]
                        self.grid[i][pos] = 0
                        pos += 1
                    else:
                        break

        self.spawnRandom()

    def isFull(self):
        for i in range(0, GameArea.GRID_SIZE):
            for j in range(0, GameArea.GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        return True

    def isPlayable(self):
        if self.isFull():
            to_collapse = []

            # left
            for j in range(0, GameArea.GRID_SIZE):
                pos = 1
                while pos < GameArea.GRID_SIZE:
                    if self.grid[pos - 1][j] == self.grid[pos][j]:
                        to_collapse.append((pos, j))
                        pos += 2
                    else:
                        pos += 1

            # right
            for j in range(0, GameArea.GRID_SIZE):
                pos = 1
                while pos < GameArea.GRID_SIZE:
                    if self.grid[pos - 1][j] == self.grid[pos][j]:
                        to_collapse.append((pos, j))
                        pos += 2
                    else:
                        pos += 1

            # up
            for i in range(0, GameArea.GRID_SIZE):
                pos = 1
                while pos < GameArea.GRID_SIZE:
                    if self.grid[i][pos - 1] == self.grid[i][pos]:
                        to_collapse.append((i, pos))
                        pos += 2
                    else:
                        pos += 1

            # down
            for i in range(GameArea.GRID_SIZE - 1, -1, -1):
                pos = GameArea.GRID_SIZE - 2
                while pos >= 0:
                    if self.grid[i][pos + 1] == self.grid[i][pos]:
                        to_collapse.append((i, pos))
                        pos -= 2
                    else:
                        pos -= 1

            if not to_collapse:
                return False
            return True

        else:
            return True
