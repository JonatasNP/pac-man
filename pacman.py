import pygame
import constantes
from spritebase import SpriteBase



class Pacman(SpriteBase):
    def __init__(self, x=10, y=80, animacao_velocidade=3, velocidade=3):
        self.visivel = True #para a possível habilidade "invisibilidade"

        self.movendo = False
        self.morrendo = False
        self.velocidade = velocidade
        self.x, self.y = x, y
        self.dx, self.dy = 0, 0

        self.frame_atual = 0
        self.contador_frame = 0
        self.animacao_velocidade = animacao_velocidade

        spritesheet = pygame.image.load(constantes.SPRITESHEET_PATH).convert_alpha()

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
        

        self.frames_falecendo = [pygame.transform.scale(spritesheet.subsurface(rect), 
                                                    (constantes.TILE_SIZE, constantes.TILE_SIZE))
                            for rect in constantes.PACMAN_FRAMES["falecendo"]]


        self.frames = self.frame_parado
        super().__init__(self.frames[0])
        self.rect.topleft = (x, y)


    def update(self):
        self.rect.x += self.dx
        self.x += self.dx
        
        self.rect.y += self.dy
        self.y += self.dy

        if self.movendo:
            self.morrendo = False
            self.contador_frame += 1
            if self.contador_frame >= self.animacao_velocidade:
                self.contador_frame = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)
                
                if self.frame_atual == 0:
                    pygame.mixer.Sound('audios/munch_1.wav').play()
                elif self.frame_atual == len(self.frames) - 1:
                    pygame.mixer.Sound('audios/munch_2.wav').play()
                
                self.image = self.frames[self.frame_atual]

        elif self.morrendo:
            self.contador_frame += 1
            if self.contador_frame >= self.animacao_velocidade:
                self.contador_frame = 0
                self.frame_atual = (self.frame_atual + 1) % len(self.frames)

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
    
    def falecer(self):
        self.frames = self.frames_falecendo
        self.frame_atual = 0
        self.movendo = False
        self.morrendo = True
        self.dx, self.dy = 0, 0