import pygame
import constantes
import os
import random


# Classe base sprites
class SpriteBase(pygame.sprite.Sprite):
    def __init__(self, imagem_inicial):
        super().__init__()
        self.image = imagem_inicial
        self.rect = self.image.get_rect()


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

        self.bolinhas = []
        #for linha in range(1, 4):
        #    self.bolinhas.append((linha, 1))


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


    def comer_bolinha(self, linha, coluna):
        if (linha, coluna) in self.bolinhas:
            self.bolinhas.remove((linha, coluna))

    def desenhar(self, surface):
        surface.blit(self.imagem, (0, 60))

        for linha, coluna in self.bolinhas:
            x = coluna * constantes.TILE_SIZE + constantes.TILE_SIZE // 2
            y = linha * constantes.TILE_SIZE + constantes.TILE_SIZE // 2
            pygame.draw.circle(surface, constantes.AMARELO, (x, y), 3)


class Pacman(SpriteBase):
    def __init__(self, x=0, y=0, animacao_velocidade=3, velocidade=3):
        self.movendo = False
        self.velocidade = velocidade
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0

        # animação
        self.frame_atual = 0
        self.contador_frame = 0
        self.animacao_velocidade = animacao_velocidade

        spritesheet = pygame.image.load(constantes.SPRITESHEET_PATH).convert_alpha()

        # carrega frames usando constantes
        self.frame_parado = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                            (constantes.TILE_SIZE, constantes.TILE_SIZE))
                     for rect in constantes.PACMAN_FRAMES["parado"]]

        self.frames_direita = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.PACMAN_FRAMES["direita"]]

        self.frames_esquerda = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                                for rect in constantes.PACMAN_FRAMES["esquerda"]]

        self.frames_cima = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.PACMAN_FRAMES["cima"]]

        self.frames_baixo = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.PACMAN_FRAMES["baixo"]]


        self.frames = self.frame_parado
        super().__init__(self.frames[0])
        self.rect.topleft = (x, y)


    def update(self):
        #movimento
        self.rect.x += self.dx
        self.x += self.dx
        
        self.rect.y += self.dy
        self.y += self.dy

        #animacao
        if self.movendo:
            self.contador_frame += 1
            if self.contador_frame >= self.animacao_velocidade:
                self.contador_frame = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                
                if self.frame_atual == 0:
                    pygame.mixer.Sound('audios/munch_1.wav').play()
                elif self.frame_atual == len(self.frames) - 1:
                    pygame.mixer.Sound('audios/munch_2.wav').play()
                
                self.image = self.frames[self.frame_atual]
        else:
            self.image = self.frame_parado[0]


    def cima(self):
        self.frames = self.frames_cima
        self.dx, self.dy = 0, -self.velocidade
        self.movendo = True
    
    def baixo(self):
        self.frames = self.frames_baixo
        self.dx, self.dy = 0, self.velocidade
        self.movendo = True

    def esquerda(self):
        self.frames = self.frames_esquerda
        self.dx, self.dy = -self.velocidade, 0
        self.movendo = True    

    def direita(self):
        self.frames = self.frames_direita
        self.dx, self.dy = self.velocidade, 0
        self.movendo = True

    def parar(self):
        self.frames = self.frame_parado
        self.dx, self.dy = 0, 0
        self.movendo = False


class Fantasma(SpriteBase):
    def __init__(self, cor, x=0, y=0, animacao_velocidade=2, velocidade=3, labirinto=None, pacman=None):
        super().__init__(pygame.Surface((constantes.TILE_SIZE, constantes.TILE_SIZE)))  
        self.movendo = False
        self.ultimos_movs = []
        self.cor = cor
        self.velocidade = velocidade
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0

        self.labirinto = labirinto
        self.pacman = pacman

        # animacao
        self.frame_atual = 0
        self.contador_frame = 0
        self.animacao_velocidade = animacao_velocidade

        spritesheet = pygame.image.load(constantes.SPRITESHEET_PATH).convert_alpha()
        
        self.frames_direita = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                            (constantes.TILE_SIZE, constantes.TILE_SIZE))
                     for rect in constantes.FANTASMA_FRAMES[cor]["direita"]]

        self.frames_esquerda = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.FANTASMA_FRAMES[cor]["esquerda"]]

        self.frames_cima = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                                for rect in constantes.FANTASMA_FRAMES[cor]["cima"]]

        self.frames_baixo = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.FANTASMA_FRAMES[cor]["baixo"]]

        self.frames = self.frames_cima
        self.image = self.frames[0]
        self.rect.topleft = (x, y)


    def update(self):
        pacman = self.pacman
        labirinto = self.labirinto

        if False:
            self.movimentacao_inteligente(pacman, labirinto)
        else:
            self.movimentacao_aleatoria(labirinto)

        self.rect.x += self.dx
        self.rect.y += self.dy
        self.x += self.dx
        self.y += self.dy

        #mudar frames da animacao
        if self.movendo:
            self.contador_frame += 1
            if self.contador_frame >= self.animacao_velocidade:
                self.contador_frame = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                self.image = self.frames[self.frame_atual]


    def movimentacao_aleatoria(self, labirinto):
        direcoes_possiveis = []
        px, py = self.rect.x, self.rect.y

        intervalo_h = labirinto.pode_andar_horizontal(px, py)
        if intervalo_h:
            inicio, fim = intervalo_h
            
            if inicio < px == fim:
                direcoes_possiveis.append("LEFT")
            if inicio == px < fim:
                direcoes_possiveis.append("RIGHT")

        intervalo_v = labirinto.pode_andar_vertical(px, py)
        if intervalo_v:
            inicio, fim = intervalo_v

            # inicio e fim tao trocados pq inicio é a posicao mais em cima na tela
            if inicio < py == fim:
                direcoes_possiveis.append("UP")
            if inicio == py < fim:
                direcoes_possiveis.append("DOWN")

        if direcoes_possiveis:
            escolha = random.choice(direcoes_possiveis)

            self.mudar_direcao(escolha)
        

    def movimentacao_inteligente(self, pacman, labirinto): # NÃO TÁ FUNCIONANDO AINDA!!!!!!!
        dx = pacman.rect.x - self.rect.x
        dy = pacman.rect.y - self.rect.y
        
        if abs(dx) > abs(dy):
            if dx > 0 and labirinto.pode_andar_horizontal(self.rect.x, self.rect.y):
                self.direita()
            elif dx < 0 and labirinto.pode_andar_horizontal(self.rect.x, self.rect.y):
                self.esquerda()
        elif abs(dx) < abs(dy):
            if dy > 0 and labirinto.pode_andar_vertical(self.rect.x, self.rect.y):
                self.baixo()
            elif dy < 0 and labirinto.pode_andar_vertical(self.rect.x, self.rect.y):
                self.cima()
        else:
            self.parar()

    
    def mudar_direcao(self, direcao):
        if direcao == "UP":
            if len(self.ultimos_movs) == 3: self.ultimos_movs.pop(0)
            self.ultimos_movs.append("UP")    
            self.cima()
        elif direcao == "DOWN":
            if len(self.ultimos_movs) == 3: self.ultimos_movs.pop(0)
            self.ultimos_movs.append("DOWN")
            self.baixo()
        elif direcao == "LEFT":
            if len(self.ultimos_movs) == 3: self.ultimos_movs.pop(0)
            self.ultimos_movs.append("LEFT")
            self.esquerda()
        elif direcao == "RIGHT":
            if len(self.ultimos_movs) == 3: self.ultimos_movs.pop(0)
            self.ultimos_movs.append("RIGHT")
            self.direita()
        
        print("Fantasma:", self.x, self.y)
        print("Ultimos movimentos:", self.ultimos_movs)



    def cima(self):
        self.frames = self.frames_cima
        self.dx, self.dy = 0, -self.velocidade
        self.movendo = True

    def baixo(self):
        self.frames = self.frames_baixo
        self.dx, self.dy = 0, self.velocidade
        self.movendo = True

    def esquerda(self):
        self.frames = self.frames_esquerda
        self.dx, self.dy = -self.velocidade, 0
        self.movendo = True

    def direita(self):
        self.frames = self.frames_direita
        self.dx, self.dy = self.velocidade, 0
        self.movendo = True

    def parar(self):
        self.dx, self.dy = 0, 0
        self.movendo = False