import pygame
import constantes
import sprites
import os
from sprites import Pacman, Labirinto


class Game:
    def __init__(self):
        # Criando a tela do jogo
        pygame.init()
        pygame.mixer.init()
        self.tela = pygame.display.set_mode((constantes.LARGURA, constantes.ALTURA))
        pygame.display.set_caption(constantes.TITULO_JOGO)
        self.relogio = pygame.time.Clock()
        self.esta_rodando = True
        self.fonte = pygame.font.match_font(constantes.FONTE)
        self.carregar_arquivos()

        self.direcao_atual = None
        self.direcao_desejada = None


    def novo_jogo(self):
        self.labirinto = Labirinto()
        self.pacman = Pacman(
            x=10,
            y=70,
            animacao_velocidade=3,
            velocidade=3
        )
        self.todas_as_sprites = pygame.sprite.Group()
        self.todas_as_sprites.add(self.pacman)
        pygame.mixer.Sound(os.path.join("audios", constantes.MUSICA_INICIO)).play()
        self.rodar()
    

    def rodar(self):
        self.jogando = True
        pygame.mixer.music.load(os.path.join("audios", constantes.MUSICA_INICIO))
        pygame.mixer.music.play()
        while self.jogando:    
            self.relogio.tick(constantes.FPS)
            self.eventos()
            self.atualizar_sprites()
            self.desenhar_sprites()


    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.jogando:
                    self.jogando = False
                self.esta_rodando = False
            
            if event.type == pygame.KEYDOWN:
                print(self.pacman.x, self.pacman.y)
                if event.key == pygame.K_UP:
                    self.direcao_desejada = "UP"
                elif event.key == pygame.K_DOWN:
                    self.direcao_desejada = "DOWN"
                elif event.key == pygame.K_LEFT:
                    self.direcao_desejada = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    self.direcao_desejada = "RIGHT"
        
        if self.direcao_desejada:
            self.mover_pacman()

    
    def mover_pacman(self):
        px = self.pacman.x
        py = self.pacman.y
        velocidade = self.pacman.velocidade

        #tentar mudar para a direcao desejada
        if self.direcao_desejada:
            if self.direcao_desejada in ("LEFT", "RIGHT"):
                intervalo = self.labirinto.pode_andar_horizontal(px, py)
                if intervalo:
                    inicio, fim = intervalo
                    novo_x = self.pacman.rect.x - velocidade if self.direcao_desejada == "LEFT" else self.pacman.rect.x + velocidade
                    if inicio <= novo_x <= fim:
                        self.direcao_atual = self.direcao_desejada 
            elif self.direcao_desejada in ("UP", "DOWN"):
                intervalo = self.labirinto.pode_andar_vertical(px, py)
                if intervalo:
                    inicio, fim = intervalo
                    novo_y = self.pacman.rect.y - velocidade if self.direcao_desejada == "UP" else self.pacman.rect.y + velocidade
                    if inicio <= novo_y <= fim:
                        self.direcao_atual = self.direcao_desejada

        #aplicar o movimento na direcao atual
        if self.direcao_atual in ("LEFT", "RIGHT"):
            intervalo = self.labirinto.pode_andar_horizontal(px, py)
            if intervalo:
                inicio, fim = intervalo
                novo_x = self.pacman.rect.x - velocidade if self.direcao_atual == "LEFT" else self.pacman.rect.x + velocidade
                if novo_x < inicio:
                    self.pacman.rect.x = inicio
                    self.pacman.parar()
                    self.direcao_atual = None
                elif novo_x > fim:
                    self.pacman.rect.x = fim
                    self.pacman.parar()
                    self.direcao_atual = None
                else:
                    if self.direcao_atual == "LEFT":
                        self.pacman.esquerda()
                    else:
                        self.pacman.direita()
            else:
                self.pacman.parar()
                self.direcao_atual = None

        elif self.direcao_atual in ("UP", "DOWN"):
            intervalo = self.labirinto.pode_andar_vertical(px, py)
            if intervalo:
                inicio, fim = intervalo
                novo_y = self.pacman.rect.y - velocidade if self.direcao_atual == "UP" else self.pacman.rect.y + velocidade
                if novo_y < inicio:
                    self.pacman.rect.y = inicio
                    self.pacman.parar()
                    self.direcao_atual = None
                elif novo_y > fim:
                    self.pacman.rect.y = fim
                    self.pacman.parar()
                    self.direcao_atual = None
                else:
                    if self.direcao_atual == "UP":
                        self.pacman.cima()
                    else:
                        self.pacman.baixo()
            else:
                self.pacman.parar()
                self.direcao_atual = None
            

    def atualizar_sprites(self):
        self.todas_as_sprites.update()



        linha = self.pacman.rect.centery // constantes.TILE_SIZE
        coluna = self.pacman.rect.centerx // constantes.TILE_SIZE
        self.labirinto.comer_bolinha(linha, coluna)


    def desenhar_sprites(self):
        self.tela.fill(constantes.PRETO)
        self.labirinto.desenhar(self.tela)
        self.todas_as_sprites.draw(self.tela)
        pygame.display.flip()


    def carregar_arquivos(self):
        diretorio_imagens = os.path.join(os.getcwd(), 'imagens')
        self.diretorio_audios = os.path.join(os.getcwd(), 'audios')
        self.spritesheet = os.path.join(diretorio_imagens, constantes.SPRITSHEET)
        self.pacman_start_logo = os.path.join(diretorio_imagens, constantes.PACMAN_START_LOGO)
        self.pacman_start_logo = pygame.image.load(self.pacman_start_logo).convert()


    def mostrar_texto(self, texto, tamanho, cor, x, y):
        fonte = pygame.font.Font(self.fonte, tamanho)
        texto = fonte.render(texto, True, cor)
        texto_rect = texto.get_rect()
        texto_rect.midtop = (x, y)
        self.tela.blit(texto, texto_rect)

    
    def mostrar_start_logo(self, x, y):
        start_logo_rect = self.pacman_start_logo.get_rect()
        start_logo_rect.midtop = (x, y)
        self.tela.blit(self.pacman_start_logo, start_logo_rect)


    def mostrar_tela_start(self):
        pygame.mixer.music.load(os.path.join("audios", constantes.MUSICA_START))
        pygame.mixer.music.play()

        self.mostrar_start_logo(constantes.LARGURA / 2, 20)

        self.mostrar_texto(
            'Pressione uma tecla para jogar',
            22,
            constantes.AMARELO,
            constantes.LARGURA / 2,
            320
        )
        self.mostrar_texto(
            'Desenvolvido por jonatas.cunha',
            14,
            constantes.BRANCO,
            constantes.LARGURA / 2,
            570
        )

        pygame.display.flip()
        self.esperar_por_jogador()
    

    def esperar_por_jogador(self):
        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
                if event.type == pygame.KEYUP:
                    esperando = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.diretorio_audios, constantes.TECLA_START)).play()


    def mostrar_tela_game_over(self):
        pass


g = Game()
g.mostrar_tela_start()


while g.esta_rodando:
    g.novo_jogo()
    g.mostrar_tela_game_over()

