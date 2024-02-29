import pyxel
from pygame import mixer #Apenas para musica e sons

ataques = []
golpes = []
coletaveis = []
inimigos = []
hazards = []
deads = []
alreadySpawn = []

TILE_WALL_Y = 11

telaX = 0
win = False

# TILES SPAWN INIMIGOS
TILE_SPAWN1 = (20, 0) # Inimigo 1 -CONFIRMAD
TILE_SPAWN2 = (24, 0) # Inimigo 2
TILE_SPAWN3 = (28, 0) #Inimigo 3

TILE_SPAWN4 = (26, 0) # Bola de fogo
TILE_SPAWN5 = (25, 0) # + Vida Maxima
TILE_SPAWN6 = (21, 0) # + Vida - CONFIRMA

TILE_SPAWN7 = (23, 0) # Espinho
TILE_SPAWN8 = (23, 1) # Espinho
TILE_SPAWN9 = (20, 6) # Flecha
TILE_SPAWN10 = (25, 2) # Ball

mixer.init()

mixer.music.load('sound/musica_v6.wav')
mixer.music.set_volume(0.2)

arrowThrow = mixer.Sound("sound/arrowThrow.wav")
mixer.Sound.set_volume(arrowThrow, 0.1)
enemy1Die = mixer.Sound("sound/enemy1Die.wav")
mixer.Sound.set_volume(enemy1Die, 1)
enemy2Die = mixer.Sound("sound/enemy2Die.wav")
mixer.Sound.set_volume(enemy2Die, 0.1)
enemy3Attack = mixer.Sound("sound/enemy3Attack.wav")
mixer.Sound.set_volume(enemy3Attack, 0.1)
enemy3Die = mixer.Sound("sound/enemy3Die.wav")
mixer.Sound.set_volume(enemy3Die, 0.1)
enemy3TakeDamage = mixer.Sound("sound/enemy3TakeDamage.wav")
mixer.Sound.set_volume(enemy3TakeDamage, 0.1)
spike = mixer.Sound("sound/espinhosNascendo.wav")
mixer.Sound.set_volume(spike, 0.1)
pulo = mixer.Sound("sound/jump.wav")
mixer.Sound.set_volume(pulo, 0.1)
matsDie = mixer.Sound("sound/mathDie.wav")
mixer.Sound.set_volume(matsDie, 0.1)
matsShoot = mixer.Sound("sound/mathiShoot.wav")
mixer.Sound.set_volume(matsShoot, 0.1)
matsTakeDamage = mixer.Sound("sound/mathTakeDamage.wav")
mixer.Sound.set_volume(matsTakeDamage, 0.1)
matsWalk = mixer.Sound("sound/mathWalk.wav")
mixer.Sound.set_volume(matsWalk, 0.1)
power1 = mixer.Sound("sound/powerup1.wav")
mixer.Sound.set_volume(power1, 0.1)
power2 = mixer.Sound("sound/powerup2.wav")
mixer.Sound.set_volume(power2, 0.1)
power3 = mixer.Sound("sound/poweruplife.wav")
mixer.Sound.set_volume(power3, 0.1)
select = mixer.Sound("sound/select.wav")
mixer.Sound.set_volume(select, 0.1)

# --- FUNÇÕES --- #

def limparLista(lista):
    i = 0
    while i < len(lista):
        elem = lista[i]
        if elem.is_alive:
            i += 1
        else:
            lista.pop(i)
def get_tile(tile_x, tile_y):
    return pyxel.tilemap(0).pget(tile_x, tile_y)
def is_wall(x, y):
    tile = get_tile(x,y)
    return tile[1] <= TILE_WALL_Y
def is_plat(x, y): #USAR PARA PLATAFORMAS
    tile = get_tile(x,y)
    return tile[1] <= TILE_WALL_Y - 4
def restart():
    alreadySpawn.clear()
def is_wallForEnemy(x, y): # Parede para inimigos
    tile = get_tile(x,y)
    return tile[1] <= TILE_WALL_Y + 4
def obstrucao(x, y, d, h, w):
    i = 1
    while i < 16:
        if colide(x, y - 1, d, h=h, w=w):
            y -= 1
        i -= 1
def spawn(b):
    for i in range(b, b+pyxel.width//8 + 50):
        for j in range(pyxel.height//8):
            a = get_tile(i, j)
            if a == TILE_SPAWN1 and not ((i, j) in alreadySpawn):
                inimigo(i*8, (j*8)-16, 1, w=16, h=16)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN2 and not ((i, j) in alreadySpawn):
                inimigo(i * 8, (j * 8) - 32, 1, w=32, h=32, apa=2)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN3 and not ((i, j) in alreadySpawn):
                inimigo(i*8, (j*8) - 64, 2, w=64, h=64, apa=3, life=5)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN4 and not ((i, j) in alreadySpawn):
                coletavel(i*8, (j*8)-18, 1)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN5 and not ((i, j) in alreadySpawn):
                coletavel(i * 8, (j * 8) - 18, 2)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN6 and not ((i, j) in alreadySpawn):
                coletavel(i * 8, (j * 8) - 18, 3)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN7 and not ((i, j) in alreadySpawn):
                hazard(i*8, (j*8) - 16, 1, 2)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN8 and not ((i, j) in alreadySpawn):
                hazard(i * 8, (j * 8) + 16, 1, 4)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN9 and not ((i, j) in alreadySpawn):
                hazard(i * 8, j * 8, 2, 3)
                alreadySpawn.append((i, j))
            elif a == TILE_SPAWN10 and not ((i, j) in alreadySpawn):
                hazard(i * 8, j * 8, 3, 3, r=100)
                alreadySpawn.append((i, j))
def colide(x, y, d, h, w, e=0):
    x1 = (x - 1) // 8
    x2 = x // 8
    x3 = (x + w - 1) // 8
    x4 = (x + w) // 8
    y1 = (y - 1) // 8
    y2 = y // 8
    y3 = (y + h - 1) // 8
    y4 = (y + h) // 8
    if d == 1 and e==0: #Direita
        if is_wall(x4, y2) or is_wall(x4, y3) or is_wall(x3, y2) or is_wall(x3, y3):
            return True
    elif d == 1 and e==1: #Direita
        if is_wallForEnemy(x4, y2) or is_wallForEnemy(x4, y3) or is_wallForEnemy(x3, y2) or is_wallForEnemy(x3, y3):
            return True
    elif d == 2: #Inferior
        if is_wall(x2, y4) or is_wall(x3, y4) or is_wall(x2, y3) or is_wall(x3, y3):
            return True
    elif d == 3 and e==0: #Esquerda
        if is_wall(x1, y2) or is_wall(x1, y3) or is_wall(x2, y2) or is_wall(x2, y3):
            return True
    elif d == 3 and e==1: #Esquerda
        if is_wallForEnemy(x1, y2) or is_wallForEnemy(x1, y3) or is_wallForEnemy(x2, y2) or is_wallForEnemy(x2, y3):
            return True
    elif d == 4: #Superior
        if is_plat(x2, y1) or is_plat(x3, y1) or is_plat(x2, y2) or is_plat(x3, y2):
            return True
def colisao(x1, y1, w1, h1, x2, y2, w2, h2):
    return x1 < x2 + w2 and x2 < x1 + w1 and y1 < y2 + h2 and y2 < y1 + h1

# --- CLASSES --- #
# RELOGIO
class relogio:
    def __init__(self, segundos):
        self.inicio = pyxel.frame_count // 60
        self.atual = self.inicio
        self.seg = segundos
        self.final = self.inicio + self.seg
        self.final2 = self.inicio + self.seg
        self.pulso = False
        self.ativa = False

    def pulsos(self):
        if self.atual >= self.final:
            self.final += self.seg
            self.pulso = True
        else:
            self.pulso = False
    def cooldown(self):
        if self.atual >= self.final2:
            self.ativa = True

    def update(self):
        self.atual = pyxel.frame_count // 60
        self.pulsos()
        self.cooldown()
# PROJETEIS INIMIGOS
class ataque:
    def __init__(self, x, y, d, w, h, apa=1):
        self.x = x
        self.y = y
        self.d = d
        self.w = w
        self.h = h
        self.apa = apa
        self.count = 0
        self.anim = [192, 224]
        self.is_alive = True
        ataques.append(self)

    def update(self):
        if self.is_alive:
            if colide(self.x, self.y, self.d, self.h, self.w):
                self.is_alive = False
            if self.d == 1:
                self.x += 3
            elif self.d == 3:
                self.x -= 3

    def draw(self):
        if self.is_alive:
            if self.apa == 1:
                if self.d == 1:
                    pyxel.blt(self.x, self.y, 0, 192, 48, -self.w, self.h, 15)
                elif self.d == 3:
                    pyxel.blt(self.x, self.y, 0, 192, 48, self.w, self.h, 15)
            elif self.apa == 2:
                if pyxel.frame_count % 30 == 0:
                    self.count += 1
                if self.count == 2:
                    self.count = 0
                if self.d == 1:
                    pyxel.blt(self.x, self.y, 2, self.anim[self.count], 40, self.w, self.h, 15)
                elif self.d == 3:
                    pyxel.blt(self.x, self.y, 2, self.anim[self.count], 40, -self.w, self.h, 15)
#PROJETEIS DO PERSONAGEM
class golpe:
    def __init__(self, x, y, d, w, h, n=1, apa=1):
        self.x = x
        self.y = y
        self.d = d
        self.w = w
        self.h = h
        self.n = n
        self.apa = apa
        self.is_alive = True
        self.count = 0
        self.anim = [0, 16, 32, 48]
        golpes.append(self)


    def update(self):
        if colide(self.x, self.y, self.d, 16, 16):
            self.is_alive = False
        if self.d == 1:
            self.x += 3
        elif self.d == 3:
            self.x -= 3

    def draw(self):
        if self.is_alive:
            if self.n == 1:
                if pyxel.frame_count % 4 == 0 and self.count != 4:
                    self.count += 1
                if self.count == 4:
                    self.count = 0
                if self.d == 1:
                    pyxel.blt(self.x, self.y, 1, self.anim[self.count], 160, self.w, self.h, 15)
                elif self.d == 3:
                    pyxel.blt(self.x, self.y, 1, self.anim[self.count], 160, -self.w, self.h, 15)
            if self.n == 2:
                if pyxel.frame_count % 4 == 0 and self.count != 4:
                    self.count += 1
                if self.count == 4:
                    self.count = 0
                if self.d == 1:
                    pyxel.blt(self.x, self.y, 1, self.anim[self.count], 176, self.w, self.h, 15)
                elif self.d == 3:
                    pyxel.blt(self.x, self.y, 1, self.anim[self.count], 176, -self.w, self.h, 15)
class inimigo:
    def __init__(self, x, y, mov, w=8, h=8, life=1, apa=1, r=40, atqD=3, speed=5):
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.mov = mov
        self.w = w
        self.h = h
        self.life = life
        self.lastLife = life
        self.apa = apa
        self.is_alive = True
        self.dir = 1
        self.animate = 0
        self.count = [0, 0]
        self.anim1 = [0, 16] #Inimigo pequeno
        self.anim2 = [32, 64]
        self.anim3, self.anim4, self.anim5 = [0, 64, 128], [192, 224], [0, 0, 64]
        self.atqD = atqD
        self.speed = speed
        self.atacking = False
        self.g = 0
        self.r = r
        inimigos.append(self)

    def update(self):
        ############
        ### VIDA ###
        ############

        if self.life <= 0:
            self.is_alive = False

        #####################
        ### MOVIMENTAÇÔES ###
        #####################
        # - MOVIMENTAÇÃO HORIZONTAL
        if self.mov == 1:

            if not colide(self.x, self.y, 2, self.h, self.w):
                self.y += 2

            if colide(self.x, self.y, 2, self.h-1, self.w):
                self.y -= 1

            if self.dir == 1 and not colide(self.x, self.y, 1, self.h, self.w) and not colide(self.x, self.y, 1, self.h, self.w, e=1):
                self.x += 1
            else:
                self.dir = 3
            if self.dir == 3 and not (colide(self.x, self.y, 3, self.h, self.w)) and not colide(self.x, self.y, 3, self.h, self.w, e=1):
                self.x -= 1
            else:
                self.dir = 1

        if self.mov == 2:
            pass


        ##############
        ### ATAQUE ###
        ##############

        if self.apa == 3:
            if self.lastLife != self.life and self.is_alive:
                mixer.Sound.play(enemy3TakeDamage)
                self.lastLife = self.life
            if pyxel.frame_count % 120 == 0:
                self.atacking = True

    def draw(self):
        if self.x > telaX - 20 and self.x < telaX + pyxel.width:
            if self.apa == 1:
                if pyxel.frame_count % 30 == 0 and self.count[0] != 2:
                    self.count[0] += 1
                if self.count[0] == 2:
                    self.count[0] = 0
                if self.dir == 3:
                    pyxel.blt(self.x, self.y, 2, self.anim1[self.count[0]], 0, -self.w, self.h, 15)
                elif self.dir == 1:
                    pyxel.blt(self.x, self.y, 2, self.anim1[self.count[0]], 0, self.w, self.h, 15)
            elif self.apa == 2:
                if pyxel.frame_count % 30 == 0 and self.count[0] != 2:
                    self.count[0] += 1
                if self.count[0] == 2:
                    self.count[0] = 0
                if self.dir == 3:
                    pyxel.blt(self.x, self.y, 2, self.anim2[self.count[0]], 0, -self.w, self.h, 15)
                elif self.dir == 1:
                    pyxel.blt(self.x, self.y, 2, self.anim2[self.count[0]], 0, self.w, self.h, 15)
            elif self.apa == 3:
                if not self.atacking:
                    if pyxel.frame_count % 30 == 0 and self.count[0] != 3:
                        self.count[0] += 1
                    if self.count[0] == 3:
                        self.count[0] = 0
                    pyxel.blt(self.x, self.y, 2, self.anim3[self.count[0]], 32, -self.w, self.h, 15)
                elif self.atacking:
                    if pyxel.frame_count % 10 == 0 and self.count[1] != 3:
                        self.count[1] += 1
                    if self.count[1] == 3:
                        ataque(self.x-16, self.y+16, self.atqD, 32, 32, apa=2)
                        mixer.Sound.play(enemy3Attack)
                        self.count[1] = 0
                        self.atacking = False
                    pyxel.blt(self.x, self.y, 2, self.anim5[self.count[1]], 96, -self.w, self.h, 15)
class coletavel:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.is_alive = True
        self.count = 0
        self.anim = [0, 16, 32, 48]
        self.type = type
        coletaveis.append(self)
    def update(self):
        pass
    def draw(self):
        if self.is_alive:
            if self.type == 1:
                if pyxel.frame_count % 45 == 0:
                    self.count += 1
                if self.count == 2:
                    self.count = 0

                pyxel.blt(self.x, self.y, 1, self.anim[self.count], 192, self.w, self.h, 15)
            elif self.type == 2:
                if pyxel.frame_count % 45 == 0:
                    self.count += 1
                if self.count == 2:
                    self.count = 0
                pyxel.blt(self.x, self.y, 1, self.anim[self.count], 208, self.w, self.h, 15)
            elif self.type == 3:
                if pyxel.frame_count % 45 == 0:
                    self.count += 1
                if self.count == 4:
                    self.count = 0
                pyxel.blt(self.x, self.y, 1, self.anim[self.count], 224, self.w, self.h, 15)
class personagem:
    def __init__(self, x, y, w = 8, h= 8, n = 1):
        self.x = x                  # posição x
        self.y = y                  # posição y
        self.n = n                  # número do player. 1 = mathias / 2 = Matilda
        self.spawnx = x             # posicao x do spawn, para possibilitar o respawn
        self.spawny = y             # posição y do spawn
        self.w = w                  # comprimento do sprite
        self.h = h                  # altura do sprite
        self.d = 1                  # direção. 1-Direita, 2-Inferior, 3-Esquerda e 4-Superior
        self.atq = False
        self.life = 3
        self.maxLife = 3
        self.lastLife = self.life
        self.takeDamage = False
        self.is_alive = True        # estado do personagem
        self.count = [0, 0, 0, 0]
        self.animate = 0            # 0=Parado | 1=Correndo | 2=Atacando | 3=Pulando
        self.anim0 = [0, 32, 64, 96]
        self.anim1 = [0, 32, 64, 96]
        self.anim2 = [128, 160, 192]
        self.anim3 = []
        self.atacking = False
        self.immortal = False
        self.cooldown = relogio(0)
        self.in_air = False
        self.energyMax = 150
        self.energy = self.energyMax
        self.jump = True
        self.fall = False
        self.gravity = 0
        self.gravityCoef = 12
        self.gravitySoma = 1

    def spawn(self):  #Respawnar o personagem
        self.is_alive = True
        self.x = self.spawnx
        self.y = self.spawny
        self.atq = False
        self.maxLife = 3
        self.life = 3
        self.lastLife = self.maxLife

    def checkpoint(self, x, y):
        self.spawnx = x
        self.spawny = y

    def update(self):
        if self.is_alive:
            if self.life <= 0:
                self.is_alive = False
                mixer.Sound.play(matsDie)
            if self.lastLife - self.life >= 2:
                self.life = self.lastLife - 1
            if self.takeDamage:
                mixer.Sound.play(matsTakeDamage)
                self.immortal = True
                self.cooldown = relogio(0.2)
                self.lastLife = self.life
                self.life -= 1
                self.takeDamage = False
            if self.cooldown.ativa:
                self.immortal = False
            else:
                self.cooldown.update()

            if self.y > pyxel.height + 5:
                self.life = 0
            if self.n == 1:
                while colide(self.x, self.y - 1, 2, h=self.h, w=self.w) and not colide(self.x, self.y, 4, h=self.h,w=self.w) and not self.jump:
                    self.y -= 1

                #MECANICA PULO | GRAVIDADE
                # Está no chao
                if colide(self.x, self.y, 2, h=self.h, w=self.w):
                    if self.energy > self.energyMax:
                        self.energy = self.energyMax
                    self.fall = False
                    self.jump = False
                    self.gravity = 0
                    if pyxel.sgn(self.energy) == -1:
                        self.energy = 0
                    if self.energy < self.energyMax:
                        self.energy += 75
                    if pyxel.btnp(pyxel.KEY_W):
                        mixer.Sound.play(pulo)
                        self.y -= 2
                        self.jump = True
                # Está caindo
                else:
                    self.fall = True
                    if self.gravity < self.gravityCoef:
                        self.gravity += self.gravitySoma
                if self.fall:
                    self.y += self.gravity // 4
                    if not self.jump:
                        self.jump = True
                        if self.energy > 0:
                            self.energy = 0

                # Se bater no 'teto'
                if colide(self.x, self.y, 4, h=self.h, w=self.w):
                    self.jump = True
                    self.energy = 0

                # Se estiver no processo de pulo
                if self.jump:
                    self.energy -= self.gravity
                    if pyxel.sgn(self.energy) == 1:
                        self.y -= self.energy // 20
                    else:
                        self.y += (self.energy*-1) // 50

                #ANDAR DIREITA
                if pyxel.btn(pyxel.KEY_D) and not colide(self.x, self.y, 1, h=self.h-6, w=self.w) and not self.atacking:
                    if not mixer.get_busy():
                        mixer.Sound.play(matsWalk)
                    self.x += 2
                    self.d = 1
                    self.animate = 1
                #ANDAR ESQUERDA
                elif pyxel.btn(pyxel.KEY_A) and not colide(self.x, self.y, 3, h=self.h-6, w=self.w) and not self.atacking:
                    if not mixer.get_busy():
                        mixer.Sound.play(matsWalk)
                    self.x -= 2
                    self.d = 3
                    self.animate = 1
                elif not self.atacking:
                    self.animate = 0

                ##############
                ### ATAQUE ###
                ##############

                if pyxel.btnp(pyxel.KEY_F) and self.atq:
                    self.animate = 2
                    self.atacking = True
            if self.n == 2:
                if colide(self.x, self.y - 1, 2, h=self.h, w=self.w) and not colide(self.x, self.y, 4, h=self.h,w=self.w) and not self.jump:
                    self.y -= 1
                    if colide(self.x, self.y - 1, 2, h=self.h, w=self.w) and not colide(self.x, self.y, 4, h=self.h,w=self.w) and not self.jump:
                        self.y -= 1
                        if colide(self.x, self.y - 1, 2, h=self.h, w=self.w) and not colide(self.x, self.y, 4, h=self.h,w=self.w) and not self.jump:
                            self.y -= 1


                #MECANICA PULO | GRAVIDADE
                # Está no chao
                if colide(self.x, self.y, 2, h=self.h, w=self.w):
                    if self.energy > self.energyMax:
                        self.energy = self.energyMax
                    self.fall = False
                    self.jump = False
                    self.gravity = 0
                    if pyxel.sgn(self.energy) == -1:
                        self.energy = 0
                    if self.energy < self.energyMax:
                        self.energy += 75
                    if pyxel.btnp(pyxel.KEY_UP):
                        mixer.Sound.play(pulo)
                        self.y -= 2
                        self.jump = True
                # Está caindo
                else:
                    self.fall = True
                    if self.gravity < self.gravityCoef:
                        self.gravity += self.gravitySoma
                if self.fall:
                    self.y += self.gravity // 4
                    if not self.jump:
                        self.jump = True
                        if self.energy > 0:
                            self.energy = 0

                # Se bater no 'teto'
                if colide(self.x, self.y, 4, h=self.h, w=self.w):
                    self.jump = True
                    self.energy = 0

                # Se estiver no processo de pulo
                if self.jump:
                    self.energy -= self.gravity
                    if pyxel.sgn(self.energy) == 1:
                        self.y -= self.energy // 20
                    else:
                        self.y += (self.energy * -1) // 50

                #ANDAR DIREITA
                if pyxel.btn(pyxel.KEY_RIGHT) and not colide(self.x, self.y, 1, h=self.h-6, w=self.w) and not self.atacking:
                    if not mixer.get_busy():
                        mixer.Sound.play(matsWalk)
                    self.x += 2
                    self.d = 1
                    self.animate = 1
                #ANDAR ESQUERDA
                elif pyxel.btn(pyxel.KEY_LEFT) and not colide(self.x, self.y, 3, h=self.h-6, w=self.w) and not self.atacking:
                    if not mixer.get_busy():
                        mixer.Sound.play(matsWalk)
                    self.x -= 2
                    self.d = 3
                    self.animate = 1
                elif not self.atacking:
                    self.animate = 0

                ##############
                ### ATAQUE ###
                ##############

                if pyxel.btnp(pyxel.KEY_SPACE) and self.atq:
                    self.animate = 2
                    self.atacking = True

    def draw(self):
        if self.is_alive:
            if self.n == 1:
                if self.immortal:
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, 224, 0, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, 224, 0, -self.w, self.h, 15)
                elif self.animate == 0:
                    if pyxel.frame_count % 30 == 0 and self.count[0] != 4:
                        self.count[0]+= 1
                    if self.count[0] == 4:
                        self.count[0] = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim0[self.count[0]], 0, self.w, self.h,15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim0[self.count[0]], 0, -self.w, self.h, 15)

                elif self.animate == 1:
                    if pyxel.frame_count % 15 == 0 and self.count[1] != 4:
                        self.count[1] += 1
                    if self.count[1] == 4:
                        self.count[1] = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim1[self.count[1]], 32, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim1[self.count[1]], 32, -self.w, self.h, 15)
                if self.animate == 2:
                    if pyxel.frame_count % 10 == 0 and self.count[2] != 3:
                        self.count[2] += 1
                    if self.count[2] == 3:
                        self.atacking = False
                        mixer.Sound.play(matsShoot)
                        golpe(self.x, self.y+7, self.d, w=16, h=16)
                        self.count[2] = 0
                        self.animate = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim2[self.count[2]], 0, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim2[self.count[2]], 0, -self.w, self.h, 15)
                elif self.animate == 3:
                    pass
            if self.n == 2:
                if self.immortal:
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, 224, 64, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, 224, 64, -self.w, self.h, 15)
                elif self.animate == 0:
                    if pyxel.frame_count % 30 == 0 and self.count[0] != 4:
                        self.count[0] += 1
                    if self.count[0] == 4:
                        self.count[0] = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim0[self.count[0]], 64, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim0[self.count[0]], 64, -self.w, self.h, 15)

                elif self.animate == 1:
                    if pyxel.frame_count % 15 == 0 and self.count[1] != 4:
                        self.count[1] += 1
                    if self.count[1] == 4:
                        self.count[1] = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim1[self.count[1]], 96, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim1[self.count[1]], 96, -self.w, self.h, 15)
                elif self.animate == 2:
                    if pyxel.frame_count % 10 == 0 and self.count[2] != 3:
                        self.count[2] += 1
                    if self.count[2] == 3:
                        self.atacking = False
                        mixer.Sound.play(matsShoot)
                        golpe(self.x, self.y + 7, self.d, w=16, h=16, n=2)
                        self.count[2] = 0
                        self.animate = 0
                    if self.d == 1:
                        pyxel.blt(self.x, self.y, 1, self.anim2[self.count[2]], 64, self.w, self.h, 15)
                    elif self.d == 3:
                        pyxel.blt(self.x, self.y, 1, self.anim2[self.count[2]], 64, -self.w, self.h, 15)
                elif self.animate == 3:
                    pass
class hazard:
    def __init__(self, x, y, type, pos, d=3, r=None):
        self.x, self.y, self.type, self.pos = x, y, type, pos
        self.anim1, self.anim2, self.anim3 = [(192, 80), (224, 72)], [160, 176], [192, 200, 208, 216]
        self.count = 0
        self.is_alive = True
        if self.type == 1: # Espinhos
            if self.pos == 2:
                self.y += 8
            else:
                pass
                #self.y -= 8
            self.h = 8
            self.w = 32
        elif self.type == 2: # Atiradores
            self.h = 16
            self.w = 16
            self.d = d
        elif self.type == 3: # Ball
            self.h = 16
            self.w = 16
            self.r = r
            self.speed = 1.5
            self.indice = 0
            self.x0 = x
            self.y0 = y
        hazards.append(self)
    def update(self):
        if self.x > telaX - 200 and self.x < telaX + pyxel.width + 400:
            if self.type == 1: # Espinhos
                if pyxel.frame_count % 55 == 0:
                    if self.pos == 2:
                        if self.h == 8:
                            mixer.Sound.play(spike)
                            self.y -= 8
                            self.h = 16
                            self.count = 1
                        else:
                            self.y += 8
                            self.h = 8
                            self.count = 0
                    else:
                        if self.h == 8:
                            mixer.Sound.play(spike)
                            self.h = 16
                            self.count = 1
                        else:
                            self.h = 8
                            self.count = 0
            elif self.type == 2:
                if pyxel.frame_count % 60 == 0:
                    if self.count == 0:
                        self.count = 1
                    elif self.count == 1:
                        ataque(self.x-1, self.y, 3,24, 16)
                        mixer.Sound.play(arrowThrow)
                        self.count = 0
            elif self.type == 3:
                self.indice += self.speed
                self.x = self.r*pyxel.cos(self.indice) + self.x0
                self.y = self.r*pyxel.sin(self.indice) + self.y0

    def draw(self):
        if self.is_alive:
            if self.type == 1:
                if self.pos == 2:
                    pyxel.blt(self.x, self.y, 2, self.anim1[self.count][0], self.anim1[self.count][1], self.w, self.h, 15)
                elif self.pos == 4:
                    pyxel.blt(self.x, self.y, 2, self.anim1[self.count][0], self.anim1[self.count][1], self.w, -self.h, 15)
            elif self.type == 2:
                if self.pos == 1:
                    pyxel.blt(self.x, self.y, 2, self.anim2[self.count], self.anim2[self.count], self.w, self.h, 15)
                elif self.pos == 3:
                    pyxel.blt(self.x, self.y, 0, self.anim2[self.count], 48, self.w, self.h, 15)

            elif self.type == 3:
                if pyxel.frame_count % 65 == 0:
                    self.count += 1
                if self.count == 4:
                    self.count = 0
                if self.count == 0:
                    pyxel.blt(self.x, self.y, 0, 224, 32, self.w, self.h, 15)
                    pyxel.blt(self.x0, self.y0, 0, self.anim3[self.count], 32, 8, 8, 15)
                elif self.count == 1:
                    pyxel.blt(self.x, self.y, 0, 224, 32, -self.w, self.h, 15)
                    pyxel.blt(self.x0, self.y0, 0, self.anim3[self.count], 32, 8, 8, 15)
                elif self.count == 2:
                    pyxel.blt(self.x, self.y, 0, 224, 32, -self.w, -self.h, 15)
                    pyxel.blt(self.x0, self.y0, 0, self.anim3[self.count], 32, 8, 8, 15)
                elif self.count == 3:
                    pyxel.blt(self.x, self.y, 0, 224, 32, self.w, -self.h, 15)
                    pyxel.blt(self.x0, self.y0, 0, self.anim3[self.count], 32, 8, 8, 15)
class dead:
    def __init__(self, type, d, x, y):
        global win
        self.type = type
        self.d = d
        self.x = x
        self.y = y
        self.cooldown = relogio(2)
        self.is_alive = True
        deads.append(self)
        if self.type == 1:
            mixer.Sound.play(enemy1Die)
        elif self.type == 2:
            mixer.Sound.play(enemy2Die)
        elif self.type == 3:
            mixer.Sound.play(enemy3Die)
            win = True
    def update(self):
        if self.cooldown.ativa:
            self.is_alive = False
        else:
            self.cooldown.update()
    def draw(self):
        if self.type == 1:
            if self.d == 3:
                pyxel.blt(self.x, self.y, 2, 96, 0, -16, 16, 15)
            elif self.d == 1:
                pyxel.blt(self.x, self.y, 2, 96, 0, 16, 16, 15)
        elif self.type == 2:
            if self.d == 3:
                pyxel.blt(self.x, self.y, 2, 112, 0, -32, 32, 15)
            elif self.d == 1:
                pyxel.blt(self.x, self.y, 2, 112, 0, 32, 32, 15)
        elif self.type == 3:
            if self.d == 3:
                pyxel.blt(self.x, self.y, 2, 128, 96, 56, 64, 15)
            elif self.d == 1:
                pyxel.blt(self.x, self.y, 2, 128, 96, -56, 64, 15)
class app:
    def __init__(self):
        self.menu = 0
        self.aux = True
        self.multiplayer = False
        pyxel.init(512, 320, fps=60)
        #CARREGAR RECURSOS E CONFIGURAÇÕES

        mixer.music.play(-1)

        self.char = personagem(20, 230, h=32, w=32)
        self.char2 = personagem(50, 220, h=32, w=32, n=2)
        pyxel.load("recursos.pyxres")
        pyxel.run(self.update, self.draw)
    def update(self):
        global telaX, win
        if self.menu == 0: #INITIAL
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.menu = 1
                mixer.Sound.play(select)
        elif self.menu == 1: #CHOOSE
            pass
        elif self.menu == 2: #Playing
            pyxel.mouse(False)
            self.char.update()
            self.char2.update()
            spawn(telaX//8)
            if not self.char.is_alive and not self.char2.is_alive:
                self.menu = 4
            for i in coletaveis:
                if colisao(i.x, i.y, i.w, i.h, self.char.x, self.char.y, self.char.w, self.char.h) and i.type == 1:
                    self.char.atq = True
                    i.is_alive = False
                    mixer.Sound.play(power1)
                    if self.multiplayer:
                        self.char2.atq = True
                if colisao(i.x, i.y, i.w, i.h, self.char2.x, self.char2.y, self.char2.w, self.char2.h) and i.type == 1:
                    self.char.atq = True
                    i.is_alive = False
                    mixer.Sound.play(power1)
                    if self.multiplayer:
                        self.char2.atq = True
                if colisao(i.x, i.y, i.w, i.h, self.char.x, self.char.y, self.char.w, self.char.h) and i.type == 2:
                    self.char.maxLife += 1
                    self.char.life += 1
                    i.is_alive = False
                    mixer.Sound.play(power2)
                    if self.multiplayer:
                        self.char2.maxLife += 1
                        self.char2.life += 1
                if colisao(i.x, i.y, i.w, i.h, self.char2.x, self.char2.y, self.char2.w, self.char2.h) and i.type == 2:
                    self.char.maxLife += 1
                    self.char.life += 1
                    i.is_alive = False
                    mixer.Sound.play(power2)
                    if self.multiplayer:
                        self.char2.maxLife += 1
                        self.char2.life += 1
                if colisao(i.x, i.y, i.w, i.h, self.char.x, self.char.y, self.char.w, self.char.h) and i.type == 3:
                    if self.char.life < self.char.maxLife:
                        self.char.life += 1
                        i.is_alive = False
                        mixer.Sound.play(power3)
                if colisao(i.x, i.y, i.w, i.h, self.char2.x, self.char2.y, self.char2.w, self.char2.h) and i.type == 3:
                    if self.multiplayer and self.char2.life < self.char2.maxLife:
                        self.char2.life += 1
                        i.is_alive = False
                        mixer.Sound.play(power3)
            for i in inimigos:
                i.update()
                if colisao(self.char.x, self.char.y, self.char.w, self.char.h, i.x, i.y, i.w, i.h) and not self.char.immortal:
                    self.char.takeDamage = True
                    self.char.immortal = True
                    self.char.update()
                    if i.apa != 3:
                        i.life -= 1
                if colisao(self.char2.x, self.char2.y, self.char2.w, self.char2.h, i.x, i.y, i.w, i.h) and not self.char2.immortal:

                    self.char2.life = True
                    self.char2.immortal = True
                    self.char2.update()
                    if i.apa != 3:
                        i.life -= 1
                for j in golpes:
                    j.update()
                    if colisao(j.x, j.y, j.w, j.h, i.x, i.y, i.w, i.h):
                        j.is_alive = False
                        i.life -= 1
                if not i.is_alive or i.life <= 0:
                    dead(i.apa, i.dir, i.x, i.y)
            for i in hazards:
                i.update()
                if i.type != 2:
                    if colisao(self.char.x, self.char.y, self.char.w, self.char.h, i.x, i.y, i.w, i.h) and not self.char.immortal:
                        self.char.takeDamage = True
                        self.char.update()
                    if colisao(self.char2.x, self.char2.y, self.char2.w, self.char2.h, i.x, i.y, i.w, i.h) and not self.char2.immortal:
                        self.char2.takeDamage = True
                        self.char2.update()
            for i in ataques:
                i.update()
                if colisao(self.char.x, self.char.y, self.char.w, self.char.h, i.x, i.y, i.w, i.h) and not self.char.immortal:
                    self.char.takeDamage = True
                    self.char.update()
                    i.is_alive = False
                if colisao(self.char2.x, self.char2.y, self.char2.w, self.char2.h, i.x, i.y, i.w, i.h) and not self.char2.immortal:
                    self.char2.takeDamage = True
                    self.char2.update()
                    i.is_alive = False
            for i in deads:
                i.update()
            if pyxel.btnr(pyxel.KEY_P):
                self.menu = 3
                mixer.Sound.play(select)
            if ((self.char2.x >= 1980 and self.char2.y > 192) or (self.char.x >= 1980 and self.char.y > 192)) and win:
                self.menu = 5
            limparLista(deads)
            limparLista(ataques)
            limparLista(golpes)
            limparLista(inimigos)
            limparLista(coletaveis)
        elif self.menu == 3: #PAUSE
            if pyxel.btnr(pyxel.KEY_P):
                self.menu = 2
                mixer.Sound.play(select)
        elif self.menu == 4: #GAME OVER
            inimigos.clear()
            hazards.clear()
            coletaveis.clear()
            alreadySpawn.clear()
            deads.clear()
            golpes.clear()
            ataques.clear()
            if pyxel.btn(pyxel.KEY_RETURN):
                self.char.spawn()
                if self.multiplayer:
                    self.char2.spawn()
                self.menu = 2
        elif self.menu == 5: #Credits
            self.char = personagem(20, 230, h=32, w=32)
            self.char2 = personagem(50, 220, h=32, w=32, n=2)
            inimigos.clear()
            hazards.clear()
            coletaveis.clear()
            alreadySpawn.clear()
            deads.clear()
            golpes.clear()
            ataques.clear()
            if pyxel.btn(pyxel.KEY_RETURN):
                self.menu = 0
    def draw(self):
        if self.menu == 0:
            self.draw_initial()
        elif self.menu == 1:
            self.draw_choose()
        elif self.menu == 2:
            self.draw_game()
        elif self.menu == 3:
            self.draw_pause()
        elif self.menu == 4:
            self.draw_gameover()
        elif self.menu == 5:
            self.draw_end()
    def draw_game(self):
        global telaX
        pyxel.cls(15)
        if self.char2.is_alive and self.char.is_alive:
            telaX = max((self.char.x + self.char2.x)//2 , 0)
            if telaX > self.char.x - 100:
                telaX = self.char.x - 100
            if telaX > self.char2.x - 100:
                telaX = self.char2.x - 100
            if telaX < 0:
                telaX = 0
        if telaX > 255 * 8 - pyxel.width:
            telaX = 255 * 8 - pyxel.width
        if self.char.is_alive and not self.char2.is_alive:
            telaX = max(self.char.x - 150, 0)
            if telaX > 255*8 - pyxel.width:
                telaX = 255*8 - pyxel.width
        elif self.char2.is_alive and not self.char.is_alive:
            telaX = max(self.char2.x - 150, 0)
            if telaX > 255 * 8 - pyxel.width:
                telaX = 255 * 8 - pyxel.width
        pyxel.camera(telaX, 0)
        pyxel.bltm(0, 0, 0, 0, 40*8, 255 * 8, pyxel.height)
        pyxel.bltm(0, 0, 0, 0, 0, 255 * 8, pyxel.height, 15)
        self.char.draw()
        if self.multiplayer:
            self.char2.draw()
            if self.char2.is_alive:
                a = 4
                for i in range(self.char2.maxLife):
                    #if i % 2 != 0:
                    pyxel.blt((telaX + a) + pyxel.width // 2, 3, 1, 80, 160, 16, 16, 15)
                    a += 17
                a = 4
                for i in range(self.char2.life):
                    #if i % 2 != 0:
                    pyxel.blt((telaX + a) + pyxel.width // 2, 3, 1, 64, 160, 16, 16, 15)
                    a += 17
        if self.char.is_alive:
            a = 4
            for i in range(self.char.maxLife):
                #if i % 2 != 0:
                pyxel.blt(telaX + a, 3, 1, 80, 160, 16, 16, 15)
                a += 17
            a = 4
            for i in range(self.char.life):
                #if i % 2 != 0:
                pyxel.blt(telaX + a, 3, 1, 64, 176, 16, 16, 15)
                a += 17

        for i in hazards:
            i.draw()
        for i in inimigos:
            i.draw()
        for i in ataques:
            i.draw()
        for i in golpes:
            i.draw()
        for i in coletaveis:
            i.draw()
        for i in deads:
            i.draw()
    def draw_choose(self):
        pyxel.cls(2)
        pyxel.mouse(True)

        pyxel.blt(140, 100, 1, 192, 200, 32, 24, 15)
        pyxel.blt(360, 100, 1, 224, 200, 32, 24, 15)
        pyxel.blt(111, 135, 2, 186, 90,70, 70, 15)
        pyxel.blt(326, 126, 2, 176, 162, 80, 88, 15)
        pyxel.text(125, 250, "COMANDOS:", 0)
        pyxel.text(345, 250, "COMANDOS:", 0)
        pyxel.text(120, 260, "W / A / D - F", 0)
        pyxel.text(340, 260, "W / A / D - F", 0)
        pyxel.text(320, 270, "UP / LEFT / RIGHT - SPACE", 0)
        if colisao(pyxel.mouse_x, pyxel.mouse_y, 2, 2, 111, 135, 70, 70):
            pyxel.blt(111-10, 220, 2, 176, 0, 80, 16, 15)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.menu = 2
                self.char2.is_alive = False
                mixer.Sound.play(select)
        if colisao(pyxel.mouse_x, pyxel.mouse_y, 2, 2, 326, 126, 80, 88):
            pyxel.blt(330 - 10, 220, 2, 176, 0, 80, 16, 15)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.menu = 2
                self.multiplayer = True
                mixer.Sound.play(select)
    def draw_initial(self):
        pyxel.cls(2)
        pyxel.mouse(True)
        pyxel.blt(pyxel.width//2 - 80, 70, 1, 96, 136, 160, 62, 15)
        if colisao(pyxel.mouse_x, pyxel.mouse_y, 2, 2, pyxel.width//2 - 30, 190, 60, 24):
            pyxel.blt(pyxel.width//2 - 40, 215, 1, 88,240, 76, 8, 15)
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.menu = 1
                mixer.Sound.play(select)
        pyxel.blt(pyxel.width//2 - 30, 190, 1, 96, 216, 60, 24, 15)
        pyxel.blt(70, 165, 2, 186, 90,70, 70, 15)
    def draw_pause(self):
        global telaX
        pyxel.mouse(False)
        pyxel.rect(telaX+(pyxel.width//2)-40, (pyxel.height//2)-60, 80, 80, 3)
        pyxel.blt(telaX+(pyxel.width//2)-14, (pyxel.height//2)-50, 1, 96, 200, 32, 9, 15)
        pyxel.blt(telaX + (pyxel.width // 2) - 16, (pyxel.height // 2) - 25, 1, 128, 200, 35, 9, 15)
        pyxel.blt(telaX + (pyxel.width // 2) - 10, (pyxel.height // 2) - 5, 1, 163, 200, 21, 9, 15)
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.KEY_W) or pyxel.btnp(pyxel.KEY_S):
            self.aux = not self.aux
        if self.aux == True:
            pyxel.blt(telaX + (pyxel.width // 2) - 16, (pyxel.height // 2) - 15, 1, 127, 210, 36, 7, 15)
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.menu = 2
                mixer.Sound.play(select)
        else:
            pyxel.blt(telaX + (pyxel.width // 2) - 12, (pyxel.height // 2) + 5, 1, 166, 210, 25, 8, 15)
            if pyxel.btnp(pyxel.KEY_RETURN):
                mixer.Sound.play(select)
                pyxel.quit()
    def draw_gameover(self):
        pyxel.camera(0, 0)
        pyxel.cls(2)
        pyxel.mouse(True)
        if colisao(pyxel.mouse_x, pyxel.mouse_y, 2, 2, pyxel.width // 2 - 65, 190, 130, 24):
            pyxel.blt(pyxel.width // 2 - 40, 215, 1, 88, 240, 76, 8, 15)
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                inimigos.clear()
                hazards.clear()
                coletaveis.clear()
                alreadySpawn.clear()
                deads.clear()
                golpes.clear()
                ataques.clear()
                self.char.spawn()
                if self.multiplayer:
                    self.char2.spawn()
                self.menu = 2
                mixer.Sound.play(select)
        pyxel.blt(pyxel.width // 2 - 65, 190, 1, 96, 216, 60, 24, 15)
        pyxel.blt(pyxel.width // 2 , 190, 1, 182, 223, 70, 24, 15)
        pyxel.blt(pyxel.width//2 - 92, 100, 2, 0, 160, 88, 32, 15)
        pyxel.blt(pyxel.width//2 - 2, 100, 2, 0, 192, 90, 32, 15)
        pyxel.blt(70, 165, 2, 89, 160,85, 90, 15)
    def draw_end(self):
        pyxel.cls(8)
        pyxel.camera(0, 0)
        pyxel.text(pyxel.width//2 - 16, 50, "PARABENS", pyxel.frame_count % 8)
        pyxel.text(pyxel.width//2 - 36, 60, "Obrigado por jogar", pyxel.frame_count % 8)
        pyxel.text(pyxel.width//2 - 26, 100, "ARTE E DESIGN", 4)
        pyxel.text(pyxel.width//2 - 28, 120, "Juliana Acunha", 4)
        pyxel.text(pyxel.width//2 - 16, 160, "SOFTWARE", 4)
        pyxel.text(pyxel.width//2 - 24, 180, "Pedro Caurio", 4)
        pyxel.blt(70, 165, 2, 186, 90, 70, 70, 15)
app()