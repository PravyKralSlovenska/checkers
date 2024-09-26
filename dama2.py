import pygame as pg

pg.init()

WIDTH, HEIGHT = 1000, 800
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Dama")

COLOR0 = (0, 0, 0)           # Black
COLOR1 = (255, 0, 0)         # Red
COLOR1A = (139, 0, 0)        # Dark Red
COLOR2 = (0, 255, 0)         # Green
COLOR3 = (0, 0, 255)         # Blue
COLOR4 = (255, 255, 0)       # Yellow
COLOR5 = (0, 255, 255)       # Cyan
COLOR6 = (255, 0, 255)       # Magenta
COLOR7 = (192, 192, 192)     # Silver
COLOR8 = (128, 128, 128)     # Gray
COLOR9 = (128, 0, 0)         # Maroon
COLOR10 = (128, 128, 0)      # Olive
COLOR11 = (0, 128, 0)        # Dark Green
COLOR12 = (128, 0, 128)      # Purple
COLOR13 = (0, 128, 128)      # Teal
COLOR14 = (0, 0, 128)        # Navy
COLOR15 = (255, 165, 0)      # Orange
COLOR16 = (255, 20, 147)     # Deep Pink
COLOR17 = (75, 0, 130)       # Indigo
COLOR18 = (240, 230, 140)    # Khaki
COLOR19 = (173, 216, 230)    # Light Blue
COLOR20 = (255, 105, 180)    # Hot Pink
COLOR21 = (255, 215, 0)      # Gold
COLOR22 = (123, 63, 0)       # Chocolate Brown
COLOR23 = (234, 221, 202)    # Beige

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

HRAC1 = Hrac('Matej', COLOR1)
HRAC2 = Hrac('Jakub', COLOR3)

class Panacik:
    def __init__(self, x,y, size, team: int):
        self.x = x
        self.y = y
        self.size = size
        self.team = team
        self.is_dama = False

    def __repr__(self):
        return f"{self.team}"

    def draw(self):
        SCREEN.blit()

    def change_to_dama(self):
        self.is_dama = True

class Sachovnica:
    def __init__(self, n=8):
        self.run = True
        self.n = n
        self.slovnik = {1: HRAC1, 2: HRAC2, HRAC1: 1, HRAC2: 2, 0: 0}
        self.hrac_na_rade = HRAC1
        self.klik = 0
        self.kliknuty_panacik = None

        self.vytvor_sachovnicu()
        self.vytvor_mapu()
        self.vytvor_texty()

    def vytvor_sachovnicu(self):
        self.sachovnica = [[Stvorec(i, j, 100, COLOR22) if (i+j) % 2 == 0 else Stvorec(i,j, 100, COLOR23) for j in range(self.n)] for i in range(self.n)]

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
            Text('DAMA', (WIDTH-190, 25), 50, (255,255,255)),
            Text(f"{HRAC1.meno}: {HRAC1.body}", (WIDTH-190, 80), 40, HRAC1.farba),
            Text(f"{HRAC2.meno}: {HRAC2.body}", (WIDTH-190, 120), 40, HRAC2.farba),
            Text('na tahu: ', (WIDTH-190, 200), 40, (255,255,255)),
            Text(f"{self.hrac_na_rade.meno}", (WIDTH-190, 230), 30, self.hrac_na_rade.farba),
            Text('status: ', (WIDTH-190, 300), 40, (255,255,255)),
            Text('Vyber si panacika', (WIDTH-190, 330), 25, (255,255,255))
        ]

    def kliknutie(self, pozicia):
        x, y = pozicia
        riadok, stlpec = y // 100, x // 100

        try:
            if self.klik == 0:
                if self.mapa[riadok][stlpec] == 0 or self.mapa[riadok][stlpec] != self.slovnik[self.hrac_na_rade]:
                    self.texty[6].update('Klikni na svoju figurku', (255,0,0))

                elif self.slovnik[self.mapa[riadok][stlpec]] == self.hrac_na_rade:
                    self.mozne_pohyby_pre_panacika(riadok, stlpec)
                    self.kliknuty_panacik = (riadok, stlpec)
                    self.texty[6].update('Vyber kam sa chces pohnut', (0,255,0))
                    self.klik += 1

                else:
                    self.remove_mozne_pohyby_pre_panacika()
                    self.texty[6].update('neviem kedy sa toto splni?', (255,125,125))
            else:
                if self.mapa[riadok][stlpec] == 3:
                    self.mapa[riadok][stlpec] = self.slovnik[self.hrac_na_rade]
                    self.mapa[self.kliknuty_panacik[0]][self.kliknuty_panacik[1]] = 0
                    self.change_player()
                    self.remove_mozne_pohyby_pre_panacika()
                
                elif self.mapa[riadok][stlpec] == 4:
                    self.mapa[riadok][stlpec] = self.slovnik[self.hrac_na_rade]
                    self.mapa[self.kliknuty_panacik[0]][self.kliknuty_panacik[1]] = 0
                    self.mapa[self.panacik_na_vyhodenie[0]][self.panacik_na_vyhodenie[1]] = 0
                    self.change_player()
                    self.remove_mozne_pohyby_pre_panacika()
                
                elif self.slovnik[self.mapa[riadok][stlpec]] == self.hrac_na_rade:
                    self.remove_mozne_pohyby_pre_panacika()
                    self.mozne_pohyby_pre_panacika(riadok, stlpec)
                    self.kliknuty_panacik = (riadok, stlpec)
                    self.texty[6].update('Vyber kam sa chces pohnut', (0,255,0))

                else:
                    self.texty[6].update('Vyber si panacika', (255,255,255))
                    self.remove_mozne_pohyby_pre_panacika()
                    self.klik = 0

        except Exception as e:
            self.texty[6].update('Klikaj na sachovnicu', (255,0,0))
            print(e)

    def change_player(self):
        self.hrac_na_rade = HRAC1 if self.hrac_na_rade == HRAC2 else HRAC2
        self.klik = 0
        self.texty[4].update(f"{self.hrac_na_rade.meno}", self.hrac_na_rade.farba)
        self.texty[6].update('Vyber si panacika', (255,255,255))

    def pohyby_dama(self, x:int, y:int):
        smery = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Všetky 4 diagonálne smery
        mozne_pohyby_list = []

        for dx, dy in smery:
            novy_x, novy_y = x + dx, y + dy
            while 0 <= novy_x < self.n and 0 <= novy_y < self.n and self.mapa[novy_x][novy_y] == 0:
                mozne_pohyby_list.append((novy_x, novy_y))
                novy_x += dx
                novy_y += dy

        for policko in mozne_pohyby_list:
            self.mapa[policko[0]][policko[1]] = 3  # Označ políčko ako dostupné

    def mozne_pohyby_pre_panacika(self, x:int, y:int):
        mozne_pohyby_list = []
        
        # Skontroluj možné pohyby pre aktuálneho hráča (vpred pre HRAC1 a vzad pre HRAC2)
        if self.hrac_na_rade == HRAC1:
            smery = [(1, 1), (1, -1)]  # HRAC1 sa pohybuje smerom nadol po doske
        else:
            smery = [(-1, 1), (-1, -1)]  # HRAC2 sa pohybuje smerom nahor po doske

        # Pre každý smer skontroluj, či je pohyb možný
        for dx, dy in smery:
            novy_x, novy_y = x + dx, y + dy
            if 0 <= novy_x < self.n and 0 <= novy_y < self.n:  # Skontroluj, či je v rámci dosky
                if self.mapa[novy_x][novy_y] == 0:  # Skontroluj, či je políčko voľné
                    mozne_pohyby_list.append((novy_x, novy_y, 'S'))

        # Skontroluj skoky cez súpera
        for dx, dy in smery:
            skok_x, skok_y = x + 2 * dx, y + 2 * dy
            medzi_x, medzi_y = x + dx, y + dy
            if 0 <= skok_x < self.n and 0 <= skok_y < self.n:
                if self.mapa[medzi_x][medzi_y] == self.slovnik[self.hrac_na_rade] % 2 + 1 and self.mapa[skok_x][skok_y] == 0:
                    self.panacik_na_vyhodenie = (medzi_x, medzi_y)
                    mozne_pohyby_list.append((skok_x, skok_y, 'N'))

        # Označ možné pohyby na mape
        for policko in mozne_pohyby_list:
            if policko[2] == 'N':
                self.mapa[policko[0]][policko[1]] = 4  # Označ políčko ako dostupné
            else:
                self.mapa[policko[0]][policko[1]] = 3  # Označ políčko ako dostupné

    def spocitaj_body(self, hrac):
        for i in range(self.n):
            for j in range(self.n):
                if self.mapa[i][j] == self.slovnik[hrac]:
                    hrac.body += 1
    
    def remove_mozne_pohyby_pre_panacika(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.mapa[i][j] == 3 or self.mapa[i][j] == 4:
                    self.mapa[i][j] = 0

    def check_game_over(self):
        if HRAC1.body == 0:
            self.texty[6].update(f"{HRAC2.meno} vyhral", COLOR21)
            self.run = False
        
        elif HRAC2.body == 0:
            self.texty[6].update(f"{HRAC1.meno} vyhral", COLOR21)
            self.run = False

    def run_func(self):
        while self.run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.run = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.kliknutie(pg.mouse.get_pos())

            SCREEN.fill(COLOR22)

            # Vykreslenie sachovnice, pozadie
            for i in range(self.n):
                for j in range(self.n):
                    self.sachovnica[i][j].draw()

            # Vykreslenie textov
            for text in self.texty:
                text.draw()

            # Vykreslenie panacikov
            for i in range(self.n):
                for j in range(self.n):
                    if self.mapa[i][j] == 1: #hrac1
                        pg.draw.circle(SCREEN, HRAC1.farba, (j*100+50, i*100+50), 40)
                    elif self.mapa[i][j] == 2: #hrac2
                        pg.draw.circle(SCREEN, HRAC2.farba, (j*100+50, i*100+50), 40)
                    elif self.mapa[i][j] == 3: #dostupne policko
                        pg.draw.circle(SCREEN, COLOR8, (j*100+50, i*100+50), 20)
                    elif self.mapa[i][j] == 4: #dostupne policko kde zabijes hraca
                        pg.draw.circle(SCREEN, COLOR1A, (j*100+50, i*100+50), 20)
                    elif self.mapa[i][j] == 5: #dama hrac1?
                        pg.draw.circle(SCREEN, (0,255,0), (j*100+50, i*100+50), 40)
                    else:
                        pass
            
            # Aktualizuj skore
            self.spocitaj_body(HRAC1)
            self.spocitaj_body(HRAC2)

            # Skontroluj koniec hry
            self.check_game_over()

            pg.display.update()

if __name__ == '__main__':
    sachovnica = Sachovnica()
    sachovnica.run_func()