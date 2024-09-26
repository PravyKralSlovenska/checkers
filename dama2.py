import pygame as pg

pg.init()

WIDTH, HEIGHT = 1000, 800
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Dama")

class Stvorec:
    def __init__(self, x,y, size, farba):
        self.x = x
        self.y = y
        self.size = size
        self.farba = farba
    
    def draw(self):
        pg.draw.rect(SCREEN, self.farba, (self.x*100, self.y*100, self.size, self.size))

class Text:
    def __init__(self, text, position, size, farba):
        self.text = text
        self.position = position
        self.size = size
        self.farba = farba
        self.font = pg.font.Font(None, self.size)

    def update(self, text, farba=None):
        self.text = text
        if farba:
            self.farba = farba
    
    def draw(self):
        text = self.font.render(self.text, True, self.farba)
        SCREEN.blit(text, self.position)
    

class Hrac:
    def __init__(self, meno, farba):
        self.meno = meno
        self.farba = farba
        self.body = 12

    def __str__(self):
        return f'{self.meno}'

HRAC1 = Hrac('Matej', (255, 125, 0))
HRAC2 = Hrac('Jakub', (255, 255, 0))

class Sachovnica:
    def __init__(self, n=8):
        self.run = True
        self.n = n
        self.slovnik = {1: HRAC1, 2: HRAC2}
        self.hrac_na_rade = HRAC1

        self.vytvor_sachovnicu()
        self.vytvor_mapu()
        self.vytvor_texty()

    def vytvor_sachovnicu(self):
        self.sachovnica = [[Stvorec(i, j, 100, (0,0,0)) if (i+j) % 2 == 0 else Stvorec(i,j, 100, (255,255,255)) for j in range(self.n)] for i in range(self.n)]

    def vytvor_mapu(self):
        self.mapa = []
        for i in range(self.n):
            self.mapa.append([])
            for j in range(self.n):
                if (i+j) % 2 == 0 and i < 3:
                    self.mapa[i].append(1)
                elif (i+j) % 2 == 0 and i > self.n - 4:
                    self.mapa[i].append(2)
                else:
                    self.mapa[i].append(0)

    def vytvor_texty(self):
        self.texty = [
            Text('DAMA', (WIDTH-150, 25), 50, (255,255,255)),
            Text(f"{HRAC1.meno}: {HRAC1.body}", (WIDTH-190, 100), 40, HRAC1.farba),
            Text(f"{HRAC2.meno}: {HRAC2.body}", (WIDTH-190, 150), 40, HRAC2.farba),
            Text('Na tahu: ', (WIDTH-190, 200), 40, (255,255,255)),
            Text('', (WIDTH-190, 250), 30, (255,255,255)),
            Text('STATUS: ', (WIDTH-190, 300), 40, (255,255,255)),
            Text('', (WIDTH-190, 350), 30, (255,255,255))
        ]

    def klik(self, pozicia):
        x, y = pozicia
        riadok, stlpec = y // 100, x // 100

        if self.klik == 0:
            if self.slovnik[self.mapa[riadok][stlpec]] == self.hrac_na_rade:
                self.mapa[riadok][stlpec] = 3
                self.texty[4].update(self.hrac_na_rade.meno)
                self.texty[4].farba = self.hrac_na_rade.farba
            else:
                ...
        else:
            if ...:
                self.klik = 0
            else:
                ...

    def pohyb(self, x:int, y:int):
        ...

    def pohyby_dama(self, x:int, y:int):
        ...

    def mozne_pohyby(self, x:int, y:int):
        ...

    def spocitaj_body(self):
        ...

    def run_func(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.klik(pg.mouse.get_pos())

            SCREEN.fill((125,125,125))

            # Vykreslenie sachovnice, pozadie
            for i in range(self.n):
                for j in range(self.n):
                    self.sachovnica[i][j].draw()

            # Vykreslenie textov
            for text in self.texty:
                text.draw()

            for i in range(self.n):
                for j in range(self.n):
                    if self.mapa[i][j] == 1:
                        pg.draw.circle(SCREEN, HRAC1.farba, (j*100+50, i*100+50), 40)
                    elif self.mapa[i][j] == 2:
                        pg.draw.circle(SCREEN, HRAC2.farba, (j*100+50, i*100+50), 40)
                    elif self.mapa[i][j] == 3:
                        pg.draw.circle(SCREEN, (125,125,125), (j*100+50, i*100+50), 40)
                    else:
                        pass

            pg.display.update()

if __name__ == '__main__':
    sachovnica = Sachovnica()
    sachovnica.run_func()