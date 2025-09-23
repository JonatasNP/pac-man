import pygame


class SpriteBase(pygame.sprite.Sprite):
    def __init__(self, imagem_inicial):
        super().__init__()
        self.image = imagem_inicial
        self.rect = self.image.get_rect()