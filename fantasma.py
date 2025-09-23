import pygame
import constantes
import random
from spritebase import SpriteBase


class Fantasma(SpriteBase):
    def __init__(self, cor, x=10, y=409, animacao_velocidade=2, velocidade=3, labirinto=None, pacman=None):
        super().__init__(pygame.Surface((constantes.TILE_SIZE, constantes.TILE_SIZE)))  
        self.movendo = False
        self.ultimos_movs = [None]
        self.cor = cor
        self.velocidade = velocidade
        self.x_inicial, self.y_inicial = x, y
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

        if pacman:
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


    def movimentacao_inteligente(self, pacman, labirinto):
        px, py = self.rect.x, self.rect.y

        intervalo_h = labirinto.pode_andar_horizontal(px, py)
        intervalo_v = labirinto.pode_andar_vertical(px, py)

        if intervalo_h and intervalo_h[0] <= pacman.x <= intervalo_h[1] and pacman.y == py:
            inicio_x, fim_x = intervalo_h
            if inicio_x <= pacman.x < px <= fim_x:
                self.mudar_direcao("LEFT")
            if inicio_x <= px < pacman.x <= fim_x:
                self.mudar_direcao("RIGHT")

        elif intervalo_v and intervalo_v[0] <= pacman.y <= intervalo_v[1] and pacman.x == px:
            # inicio e fim tao trocados pq inicio é a posicao mais em cima na tela
            inicio_y, fim_y = intervalo_v
            if inicio_y <= pacman.y < py <= fim_y:
                self.mudar_direcao("UP")
            if inicio_y <= py < pacman.y <= fim_y:
                self.mudar_direcao("DOWN")

        else:
            self.movimentacao_aleatoria(labirinto)

    
    def movimentacao_aleatoria(self, labirinto):
        direcoes_possiveis = []
        px, py = self.rect.x, self.rect.y

        intervalo_h = labirinto.pode_andar_horizontal(px, py)
        intervalo_v = labirinto.pode_andar_vertical(px, py)

        if intervalo_h:
            inicio_x, fim_x = intervalo_h
            if inicio_x < px == fim_x or (intervalo_v and intervalo_v[0] <= py <= intervalo_v[1] and inicio_x < px <= fim_x):
                direcoes_possiveis.append("LEFT")
            if inicio_x == px < fim_x or (intervalo_v and intervalo_v[0] <= py <= intervalo_v[1] and inicio_x <= px < fim_x):
                direcoes_possiveis.append("RIGHT")

        if intervalo_v:
            # inicio e fim tao trocados pq inicio é a posicao mais em cima na tela
            inicio_y, fim_y = intervalo_v
            if inicio_y < py == fim_y or (intervalo_h and intervalo_h[0] <= px <= intervalo_h[1] and inicio_y < py <= fim_y):
                direcoes_possiveis.append("UP")
            if inicio_y == py < fim_y or (intervalo_h and intervalo_h[0] <= px <= intervalo_h[1] and inicio_y <= py < fim_y):
                direcoes_possiveis.append("DOWN")

        if direcoes_possiveis:
            opostas = {"LEFT":"RIGHT","RIGHT":"LEFT","UP":"DOWN","DOWN":"UP"}

            if len(self.ultimos_movs) > 1 and len(direcoes_possiveis) > 1 and opostas[self.ultimos_movs[-1]] in direcoes_possiveis:
                direcoes_possiveis.remove(opostas[self.ultimos_movs[-1]])
            
            escolha = random.choice(direcoes_possiveis)

            self.mudar_direcao(escolha)

    
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


