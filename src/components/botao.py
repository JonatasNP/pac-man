import pygame
import src.constantes as constantes
import os


class Botao:
    def __init__(self, x, y, largura, altura, texto, cor_fundo, cor_texto, fonte_nome=constantes.FONTE, fonte_tamanho=24):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor_fundo = cor_fundo
        self.cor_texto = cor_texto
        self.fonte = pygame.font.SysFont(fonte_nome, fonte_tamanho)

    def desenhar(self, tela):
        pygame.draw.rect(tela, self.cor_fundo, self.rect, border_radius=8)

        texto_surface = self.fonte.render(self.texto, True, self.cor_texto)
        texto_rect = texto_surface.get_rect(center=self.rect.center)
        tela.blit(texto_surface, texto_rect)

    def foi_clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect.collidepoint(evento.pos):
                pygame.mixer.Sound(os.path.join("audios", constantes.SOM_CLIQUE)).play()
                return True
        return False
