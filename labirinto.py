import os, pygame, random, constantes


class Labirinto:
    def __init__(self):
        spritesheet = pygame.image.load(constantes.SPRITESHEET_PATH).convert_alpha()
        x0, y0, largura, altura = constantes.LABIRINTO_SEM_BOLINHAS
        self.imagem = spritesheet.subsurface((x0, y0, largura, altura))
        self.imagem = pygame.transform.scale(self.imagem, (largura * 2, altura * 2))

        self.horizontais = {
            #linha: [(faixa que ele pode andar), (outra faixa)]          
            70: [(10, 184), (232, 409)],
            133: [(10, 409)],
            181: [(10, 88), (136, 184), (232, 280), (328, 409)],
            229: [(136, 280)],
            280: [(-29, 136), (280, 442)],
            328: [(136, 280)],
            373: [(10, 184), (232, 409)],
            421: [(10, 40), (88, 328), (376, 409)],
            469: [(10, 88), (136, 184), (232, 280), (328, 409)],
            517: [(10, 409)]
        }

        self.verticais = {
            #coluna: [(faixa que ele pode andar), (outra faixa)]          
            10: [(70, 181), (373, 421), (469, 517)],
            40: [(421, 469)],
            88: [(70, 469)],
            136: [(133, 181), (229, 373), (421, 469)],
            184: [(70, 133), (181, 229), (373, 421), (469, 517)],
            232: [(70, 133), (181, 229), (373, 421), (469, 517)],
            280: [(133, 181), (229, 373), (421, 469)],
            328: [(70, 469)],
            376: [(421, 469)],
            409: [(70, 181), (373, 421), (469, 517)],
        }

        self.fichas = []


    def gerar_fichas(self):
        while len(self.fichas) < 3:
            pos = self.posicao_aleatoria()
            if pos not in self.fichas:
                self.fichas.append(pos)


    def pegou_ficha(self, pacman):
        for x, y in self.fichas:
            if x - 23 <= pacman.x <= x + 23 and y - 23 <= pacman.y <= y + 23:
                self.fichas.remove((x, y))
                pygame.mixer.Sound(os.path.join("audios", constantes.SOM_PEGOU_FICHA)).play()
                return 1
        return 0


    def posicao_aleatoria(self):
        if random.choice([True, False]):
            y = random.choice(list(self.horizontais.keys()))
            intervalo = random.choice(self.horizontais[y])
            x = random.randint(intervalo[0], intervalo[1])
        else:
            x = random.choice(list(self.verticais.keys()))
            intervalo = random.choice(self.verticais[x])
            y = random.randint(intervalo[0], intervalo[1])

        return x, y


    def desenhar(self, surface):
        surface.blit(self.imagem, (0, 60))


    def pode_andar_horizontal(self, px, py):
        if py in self.horizontais:
            for inicio, fim in self.horizontais[py]:
                if inicio <= px <= fim:
                    return inicio, fim   # intervalo do corredor horiz
        return None

    def pode_andar_vertical(self, px, py):
        if px in self.verticais:
            for inicio, fim in self.verticais[px]:
                if inicio <= py <= fim:
                    return inicio, fim  #intervalo do corredor vertical
        return None


