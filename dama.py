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
        self.panacikovia = []
        self.inv = []

hrac1 = Hrac('Michael', (255, 125, 0))
hrac2 = Hrac('Ondrej', (255, 255, 0))
# hrac2.inv = [1,1,1,1,1,1,1,1,1,1,] # 10 panacikov

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
        self.position = position
        self.size = size
        self.farba = farba
        self.is_clicked = False

    def __str__(self):
        return f'Panacik: {x, y}'

    def draw(self):
        pg.draw.ellipse(SCREEN, self.farba, ((x*100 +15,y*100+15), self.size))

    def is_clicked(self):
        self.is_clicked = True if self.is_clicked == False else False

class Dama:
    ...

class Sachovnica:
    def __init__(self, n=8):
        self.running = True
        self.n = n

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
                        self.matica[i].append(1)
                        # hrac1.panacikovia.append(Panacik(i, j, (70,70), hrac1.farba))
                    elif i >= self.n - 3:
                        self.matica[i].append(2)
                        # hrac2.panacikovia.append(Panacik(i, j, (70,70), hrac2.farba))
                    else:
                        self.matica[i].append(0)
        
        # for riadok in self.matica:
        #     print(riadok)

    def vytvor_texty(self):
        self.texty = []
        self.texty.append(Text('DAMA', (WIDTH - 150, 25), 50, (255, 255, 255)))
        self.texty.append(Text(f'{hrac1.meno}: {12-len(hrac2.inv)}', (WIDTH - 190, 75), 40, hrac1.farba))
        self.texty.append(Text(f'{hrac2.meno}: {12-len(hrac1.inv)}', (WIDTH - 190, 115), 40, hrac2.farba))
        self.texty.append(Text('Na tahu: ', (WIDTH - 150, 155), 40, (255, 255, 255)))
        self.texty.append(Text('hrac1', (WIDTH - 150, 195), 30, (255, 255, 255)))
        self.texty.append(Text('STATUS:', (WIDTH - 150, 225), 40, (255, 255, 255)))
        self.texty.append(Text('klikni na panacika', (WIDTH - 190, 265), 30, (255, 255, 255)))
    
    def clicked(self, pos:tuple):
        x, y = pos
        x = x // 100
        y = y // 100

        # kvoli chybovym hlaskam
        try:
            self.sachovnica[y + self.n * x].update_color((0, 255, 0)) # zmeni farbu stvorca na zeleno
            
        except:
            print('Klikol si mimo sachovnice')
            self.texty[6].update('klikol si mimo sachovnice')
        
    def debug(self):
        print('debug')
        for i in range(self.n):
            for j in range(self.n):
                print(self.matica[j][i], end=' ')
            print()

        print('hrac1: ', hrac1.panacikovia)
        print('hrac2: ', hrac2.panacikovia)

    def run(self):
        while(self.running):

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # vykona sa funkcia, ktora zisti, ktory stvorec bol kliknuty, nasledovne sa vykreslia mozne miesta pohybu (sede kruhy)
                        self.clicked(pg.mouse.get_pos())

            # pozadie
            SCREEN.fill((125, 125, 125))
            for stvorec in self.sachovnica:
                stvorec.draw()

            # texty
            for text in self.texty:
                text.draw()

            # texty update - hraci
            # self.texty[4].update(f'{hrac1.meno}: {12-len(hrac2.inv)}', hrac1.farba)

            # panacikovia
            for i in range(self.n):
                for j in range(self.n):
                    if self.matica[j][i] == 1:
                        pg.draw.ellipse(SCREEN, hrac1.farba, (i * 100 + 15, j * 100 + 15, 70,70)) #platno, farba, (x, y, sirka, vyska)
                    elif self.matica[j][i] == 2:
                        pg.draw.ellipse(SCREEN, hrac2.farba, (i * 100 + 15, j * 100 + 15, 70,70))
                    elif self.matica[j][i] == 3:
                        pg.draw.ellipse(SCREEN, (125,125,125), (i * 100 + 25, j * 100 + 25, 50,50))

            # for panacik in hrac1.panacikovia:
            #     print("dsa")
            #     panacik.draw()
            
            # for panacik in hrac2.panacikovia:
            #     panacik.draw()

            pg.display.flip()

if __name__ == '__main__':
    sachovnica = Sachovnica(8)
    sachovnica.run()
    # sachovnica.debug()
    pg.quit()
