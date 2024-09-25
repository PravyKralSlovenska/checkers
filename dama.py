# import random
import pygame as pg

pg.init()
 
WIDTH, HEIGHT = 1000, 800
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Dama")

class Hrac:
    def __init__(self, meno, farba:tuple):
        self.meno = meno
        self.farba = farba
        self.panacikovia = [1,1,1,1,1,1,1,1,1,1,1,1]
        self.inv = []
        self.kliknuty_panacik = None

    def __str__(self):
        return f'Hrac: {self.meno}'

hrac1 = Hrac('Michael', (255, 125, 0))
hrac2 = Hrac('Ondrej', (255, 255, 0))

class Text:
    def __init__(self, text, position: tuple[int,int], size: int, farba: tuple[int,int,int]):
        self.text = text
        self.position = position
        self.size = size
        self.farba = farba
        self.font = pg.font.Font(None, self.size)
    
    def draw(self):
        text = self.font.render(self.text, True, self.farba)
        SCREEN.blit(text, self.position)
    
    def update(self, text, farba:tuple = None):
        self.text = text
        if farba:
            self.farba = farba
    
class Stvorec:
    def __init__(self, position: tuple[int,int], size: tuple[int,int], farba: tuple[int,int,int]):
        self.position = position
        self.size = size
        self.farba = farba
    
    def draw(self):
        pg.draw.rect(SCREEN, self.farba, (self.position, self.size))

    def update_color(self, farba:tuple):
        self.farba = farba

class Panacik:
    def __init__(self, x: int,y: int, size: tuple[int,int], farba: tuple[int,int,int]):
        self.x = x
        self.y = y
        self.size = size
        self.farba = farba
        self.mozne_pohyby = []
        self.is_clicked = False

    def __str__(self):
        return f'Panacik: {self.x, self.y}'
    
    def __repr__(self):
        return f'Panacik: {self.x, self.y}'

    def draw(self):
        pg.draw.ellipse(SCREEN, self.farba, ((self.x*100 +15,self.y*100+15), self.size))

    def is_clicked_func(self):
        self.is_clicked = True if self.is_clicked == False else False

    def pohyb(self, x:int, y:int):
        self.x = x
        self.y = y

class Dama:
    ...

class Sachovnica:
    def __init__(self, n=8):
        self.running = True
        self.n = n
        self.hrac_na_rade = hrac1
        self.slovnik = {1: hrac1, 2: hrac2}
        self.klik = 0
        
        # metody
        self.vytvor_sachovnicu_a_maticu()
        self.vytvor_texty()

    def vytvor_sachovnicu_a_maticu(self):
        self.sachovnica = []
        self.matica = []

        for i in range(self.n):
            self.matica.append([])
            for j in range(self.n):
                if (i + j) % 2 == 0:
                    # biely stvorec
                    self.sachovnica.append(Stvorec((i * 100, j * 100), (100, 100), (234, 221, 202)))
                    self.matica[i].append(0)
                else:
                    # cierny stvorec
                    self.sachovnica.append(Stvorec((i * 100, j * 100), (100, 100), (123, 63, 0)))
                    if i < 3:
                        self.matica[i].append(Panacik(j, i, (70,70), hrac1.farba))
                    elif i >= self.n - 3:
                        self.matica[i].append(Panacik(j, i, (70,70), hrac2.farba))
                    else:
                        self.matica[i].append(0)
        
        # for riadok in self.matica:
        #     print(riadok)

    def vytvor_texty(self):
        self.texty = []
        # 0. text
        self.texty.append(Text('DAMA', (WIDTH - 150, 25), 50, (255, 255, 255)))
        # 1. text
        self.texty.append(Text(f'{hrac1.meno}: {12-len(hrac2.inv)}', (WIDTH - 190, 75), 40, hrac1.farba))
        # 2. text
        self.texty.append(Text(f'{hrac2.meno}: {12-len(hrac1.inv)}', (WIDTH - 190, 115), 40, hrac2.farba))
        # 3. text
        self.texty.append(Text('Na tahu: ', (WIDTH - 150, 155), 40, (255, 255, 255)))
        # 4. text 
        self.texty.append(Text(self.hrac_na_rade.meno, (WIDTH - 150, 195), 30, self.hrac_na_rade.farba))
        # 5. text
        self.texty.append(Text('STATUS:', (WIDTH - 150, 225), 40, (255, 255, 255)))
        # 6. text
        self.texty.append(Text('klikni na panacika', (WIDTH - 190, 265), 30, (255, 255, 255)))
        # 7. text podpis autora :D
        # self.texty.append(Text('Jakub J. Stefancik', (WIDTH - 190, HEIGHT-30), 30, (255, 255, 255)))
    
    def print_matica(self):
        for riadok in self.matica:
            print(riadok)

    # musi ist diagolanlne o 1
    # moze preskocit panacika, a aj viac, ale musi byt miesto za nim volne
    # ak je na konci sachovnice, tak sa zmeni na dama
    def mozne_pohyby(self, x:int, y:int):
        start_bod = (x,y)
        manual = [(1,1), (-1,1), (1,-1), (-1,-1)]

        try:
            if self.hrac_na_rade == hrac1:
                for i in range(4):
                    if self.matica[y+1][x-1] == 0:
                        self.matica[y+1][x-1] = 3
                    elif self.matica[y+1][x+1] == 0:
                        self.matica[y+1][x+1] = 3
                    elif self.matica[y+1][x-1] == hrac2:
                        if self.matica[y+2][x-2] == 0:
                            self.matica[y+2][x-2] = 3
                    elif self.matica[y+1][x+1] == hrac2:
                        if self.matica[y+2][x+2] == 0:
                            self.matica[y+2][x+2] = 3

            elif self.hrac_na_rade == hrac2:
                for i in range(4):
                    if self.matica[y-1][x-1] == 0:
                        self.matica[y-1][x-1] = 3
                    elif self.matica[y-1][x+1] == 0:
                        self.matica[y-1][x+1] = 3
                    elif self.matica[y-1][x-1] == hrac1:
                        if self.matica[y-2][x-2] == 0:
                            self.matica[y-2][x-2] = 3
                    elif self.matica[y-1][x+1] == hrac1:
                        if self.matica[y-2][x+2] == 0:
                            self.matica[y-2][x+2] = 3
        except IndexError:
            pass
                    

    def change_player(self):
        self.hrac_na_rade = hrac2 if self.hrac_na_rade == hrac1 else hrac1
        self.texty[4].update(self.hrac_na_rade.meno, self.hrac_na_rade.farba)
        self.texty[6].update('klikni na panacika')
        self.remove_mozne_pohyby_z_matice()

    def remove_mozne_pohyby_z_matice(self):
        for riadok in self.matica:
            for i in range(len(riadok)):
                if riadok[i] == 3:
                    riadok[i] = 0

    def clicked(self, pos:tuple):
        x, y = pos
        x = x // 100
        y = y // 100

        if self.matica[x][y] == 0:
            return False

        if self.klik == 0:            
            if self.matica[y][x].farba == self.hrac_na_rade.farba:
                self.hrac_na_rade.kliknuty_panacik = self.matica[y][x]
                self.texty[6].update('klikni na ciel')
                self.mozne_pohyby(x, y)
                self.klik += 1

            else:
                self.texty[6].update('klikni na svojho panacika')

        
        elif self.klik == 1:
            if self.matica[y][x] == 3:
                self.hrac_na_rade.kliknuty_panacik.pohyb(x,y)
                self.change_player()

            else:
                self.remove_mozne_pohyby_z_matice()
                self.texty[6].update('klikni na panacika')
                self.klik = 0

        self.print_matica()

    def run(self):
        while(self.running):

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicked(pg.mouse.get_pos())

            # pozadie
            SCREEN.fill((125, 125, 125))
            for stvorec in self.sachovnica:
                stvorec.draw()

            # texty
            for text in self.texty:
                text.draw()

            # panacikovia
            for i in range(self.n):
                for j in range(self.n):
                    # try:
                        if self.matica[i][j] == self.hrac_na_rade.kliknuty_panacik:
                            pg.draw.ellipse(SCREEN, (255,255,255), (j * 100 + 10, i * 100 + 10, 80, 80))
                            pg.draw.ellipse(SCREEN, self.matica[i][j].farba, (j * 100 + 15, i * 100 + 15, 70, 70))

                        elif self.matica[i][j].farba == hrac1.farba:
                            pg.draw.ellipse(SCREEN, hrac1.farba, (j * 100 + 15, i * 100 + 15, 70,70))

                        elif self.matica[i][j].farba == hrac2.farba:
                            pg.draw.ellipse(SCREEN, hrac2.farba, (j * 100 + 15, i * 100 + 15, 70,70))

                        elif self.matica[i][j] == 3:
                            pg.draw.ellipse(SCREEN, (125,125,125), (j * 100 + 25, i * 100 + 25, 50, 50))

                        else:
                            print("???")

                    # except AttributeError:
                    #     pass
                    # finally:
                    #     pass

            pg.display.flip()

if __name__ == '__main__':
    sachovnica = Sachovnica(8)
    sachovnica.run()
    pg.quit()
