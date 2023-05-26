import pyxel, random

class Ennemy:
    def __init__(self, type, hp, speed, damage):
        if (random.randint(0, 1) == 0):
            self.x = -10
        else:
            self.x = 140
        if (type == 0):
            self.y = 60
        else:
            self.y = 70
        self.type = type
        self.hp = hp | 1
        self.speed = 1
        self.damage = damage
    
    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def move(self, isRight):
        if isRight == 1:
            self.setLocation(self.x + self.speed, self.y)
        else:
            self.setLocation(self.x - self.speed, self.y)

    def ai(self, player_x):
        if (player_x < self.x):
            self.move(0)
        else:
            self.move(1)

class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Best game for ever")
        
        self.mainMenu = True
        self.gameOver = False

        self.clouds_list = []

        self.player_hp = 3

        self.player_position = [60, 93]
        self.jump = 0
        self.antijump = 0
        self.direc = 1
        self.dg = 1

        self.timer = 0

        self.blast_list = []
        self.blast_count = 1

        self.animation = 0

        self.ennemies_list = []

        pyxel.load("2.pyxres")

        pyxel.run(self.update, self.draw)

    def player_move(self):
        if pyxel.btn(pyxel.KEY_D):
            self.player_position[0] += 1
            self.direc = 2
            if self.dg == -2:
                if self.jump > 0:
                    self.player_position[0] += 1
        if pyxel.btn(pyxel.KEY_Q):
            self.player_position[0] -= 1
            self.direc = -2
            if self.dg == 2:
                if self.jump > 0:
                    self.player_position[0] -= 1

        if self.jump == 0:
            if pyxel.btnr(pyxel.KEY_Z):
                self.jump = 1

    def player_jumpinair(self):
        if self.jump == 1:
            self.dg = self.direc
        if self.jump > 0:
            if self.antijump == 0:
                self.player_position[0] += self.dg
                self.player_position[1] -= 6
                self.jump += 1
                if self.jump == 10:
                    self.antijump = 1
                    self.player_position[0] += self.dg
        if self.antijump == 1:
            self.player_position[0] += self.dg * 0.5
            self.player_position[1] += 3
            self.jump -= 0.5
            if self.jump == 1:
                self.jump = 0
                self.antijump = 0

    def tp_player(self):
        if self.player_position[0] > 127:
            self.player_position[0] = -15
        if self.player_position[0] < -15:
            self.player_position[0] = 127

    def creation_blast(self):
        if pyxel.btnr(pyxel.KEY_SPACE) and self.blast_count == 1:
            if self.direc == 2:
                self.blast_list.append([self.player_position[0] + 10, self.player_position[1] + 6, 2])
                self.blast_count = 0
            else:
                self.blast_list.append([self.player_position[0] - 8, self.player_position[1] + 6, -2])
                self.blast_count = 0

    def shoot_move(self):
        for blast in self.blast_list:
            blast[0] += blast[2]

    def add_blast(self):
        if self.blast_count == 0:
            if pyxel.frame_count % 30 == 0:
                self.blast_count = 1

    def checkPlayerDie(self):
        if (self.player_hp < 1):
            if (self.gameOver == False):
                self.gameOver = True

    def show_timer(self):
        pyxel.text(50, 15, "Timer: " + str(self.timer), 0)
        if pyxel.frame_count % 30 == 0:
            self.timer += 1

    def rand_ennemies(self):
        if self.timer < 16:
            if (pyxel.frame_count % 30 == 0):
                if (random.randint(0, 1) > 0):
                        self.ennemies_list.append(Ennemy(0, 0, 1, 0))
        if self.timer < 46 and self.timer > 15:
            if (random.randint(0, 1) > 0):
                    for i in range(random.randint(1, 2)):
                        self.ennemies_list.append(Ennemy(random.randint(0, 1), 0, 1, 0))
        if self.timer < 101 and self.timer > 45:
            if (random.randint(0, 1) == 1):
                for i in range(random.randint(1, 4)):
                    self.ennemies_list.append(Ennemy(random.randint(0, 1), 0, 1, 0))
        if self.timer < 201 and self.timer > 100:
            if (random.randint(0, 1) == 1):
                for i in range(random.randint(1, 6)):
                    self.ennemies_list.append(Ennemy(random.randint(0, 1), 0, 1, 0))
        if self.timer > 200:
            for i in range(random.randint(1, self.timer / 22)):
                    self.ennemies_list.append(Ennemy(random.randint(0, 1), 0, 1, 0))

    def update(self):
        for cloud in self.clouds_list:
            self.cloudAnimation(cloud)
            self.cloudRemove(cloud)

        if (self.mainMenu):
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):
                if (pyxel.mouse_x > 40 and pyxel.mouse_x < 40 + 30):
                    if (pyxel.mouse_y > 80 and pyxel.mouse_y < 80 + 10):
                        self.mainMenu = False
        else:
            if (len(self.ennemies_list) > 0):
                for ennemy in self.ennemies_list:
                    ennemy.ai(self.player_position[0])

            self.player_move()
            self.player_jumpinair()
            self.tp_player()

            self.creation_blast()
            self.shoot_move()
            self.add_blast()

            self.checkColision()

            self.checkPlayerDie()

            self.rand_ennemies()

            if (self.gameOver):
                if pyxel.btnr(pyxel.KEY_R):
                    self.gameOver = False
                    self.mainMenu = True
                    self.player_hp = 3
                    self.timer = 0

    def draw(self):
        pyxel.cls(0)
        self.generateMap()

        for cloud in self.clouds_list:
            pyxel.blt(cloud[0], cloud[1], 1, 0, 0, 12, 5, 2)

        if (self.mainMenu):
            pyxel.blt(41, 30, 1, 0, 24, 47, 15, 2)
            pyxel.rect(49.5, 80, 29, 10, 1)
            pyxel.text(57, 82, "Play", 2)
            pyxel.blt(pyxel.mouse_x, pyxel.mouse_y, pyxel.cursor, 0, 0, 8, 8, 0)
            pyxel.text(4, 120, "SillyTeam", 0)
        else:
            if (self.gameOver):
                pyxel.text(41, 30, "Game Over !", 0)
                pyxel.text(41, 40, "Score : " + str(self.timer), 0)

                pyxel.text(20, 60, "retourner au menu avec R", 0)
            else:
                self.show_timer()
                for ennemy in self.ennemies_list:
                    self.show_ennemy(ennemy)

                for blast in self.blast_list:
                    if (blast[2] > 0):
                        pyxel.blt(blast[0], blast[1], 1, 24, 46, 12, 4, 2)
                    else:
                        pyxel.blt(blast[0], blast[1], 1, 9, 46, 12, 4, 2)

                pyxel.text(10, 10, "Vies " + str(self.player_hp), 0)

                self.player_animation()
            

    def show_ennemy(self, ennemy):
        if (ennemy.type == 0):
            if (self.player_position[0] > ennemy.x):
                pyxel.blt(ennemy.x, ennemy.y, 1, 32, 56, 22, 46, 2)
            else:
                pyxel.blt(ennemy.x, ennemy.y, 1, 9, 56, 22, 46, 2)
        else:
            if (self.player_position[0] > ennemy.x):
                pyxel.blt(ennemy.x, ennemy.y, 1, 34, 116, 17, 34, 2)
            else:
                pyxel.blt(ennemy.x, ennemy.y, 1, 12, 116, 17, 34, 2)

    def player_animation(self):
        if (self.jump > 0):
            if (self.direc == 2):
                pyxel.blt(self.player_position[0], self.player_position[1], 1, 64, 0, 16, 16, 2)
            else:
                pyxel.blt(self.player_position[0], self.player_position[1], 1, 64, 16, 16, 16, 2)
        else:
            if pyxel.btnr(pyxel.KEY_D):
                self.animation = 0
            if pyxel.btn(pyxel.KEY_D):
                if (self.direc == 2):
                    if (pyxel.frame_count % 30 == 0):
                        self.animation = self.animation + 1
                    if (self.animation % 2):
                        pyxel.blt(self.player_position[0] - 1, self.player_position[1], 1, 62, 48, 18, 15, 2)
                    else:
                        pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 0, 16, 15, 2)                        
                else:
                    pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 16, 16, 15, 2)
            else:
                if pyxel.btnr(pyxel.KEY_Q):
                    self.animation = 0
                if pyxel.btn(pyxel.KEY_Q):
                    if (self.direc == -2):
                        if (pyxel.frame_count % 30 == 0):
                            self.animation = self.animation + 1
                        if (self.animation % 2):
                            pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 32, 18, 15, 2)
                        else:
                            pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 16, 16, 15, 2)                        
                    else:
                        pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 16, 16, 15, 2)
                else:
                    if (self.direc == 2):
                        pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 0, 16, 15, 2)
                    else:
                        pyxel.blt(self.player_position[0], self.player_position[1], 1, 48, 16, 16, 15, 2)

    def generateMap(self):
        terrain_x = 0
        
        pyxel.rect(0, 0, 128, 105, 6)
        pyxel.circ(16, 16, 15, 10)
        while terrain_x < 128:
            pyxel.blt(terrain_x, 128 - 23, 0, 8, 8, 8, 15)
            pyxel.blt(terrain_x, 128 - 8, 0, 8, 15, 8, 8)
            terrain_x += 8

        self.generateClouds()

    def generateClouds(self):
        clouds_limit = 7

        while (len(self.clouds_list) <= clouds_limit - 1):
            cloud_x = random.randrange(-128, 0)
            cloud_y = random.randrange(5, 20)
            cloud_speed = random.random()
            self.clouds_list.append([cloud_x, cloud_y, cloud_speed])

    def cloudAnimation(self, cloud):
        cloud[0] += cloud[2]

    def cloudRemove(self, cloud):
        if (cloud[0] > 128):
            self.clouds_list.remove(cloud)

    def checkColision(self):
        for ennemy in self.ennemies_list:
            if (self.player_position[0] >= ennemy.x and self.player_position[0] + 16 <= ennemy.x + 24 and self.player_position[1] >= ennemy.y - 20):
                self.player_hp = self.player_hp - 1
                self.ennemies_list.remove(ennemy)
            for blast in self.blast_list:
                if (blast[0] >= ennemy.x and blast[0] <= ennemy.x + 20 and blast[1] >= ennemy.y):
                    self.ennemies_list.remove(ennemy)
                    self.blast_list.remove(blast)
Game()