import pygame
import os
from . import constantes, settings

from components.botao import Botao
from .labirinto import Labirinto
from .pacman import Pacman
from .fantasma import Fantasma


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

        self.fichas = 0
        self.vidas = 3


    def novo_jogo(self):
        self.labirinto = Labirinto()
        self.labirinto.gerar_fichas()
        self.pacman = Pacman(
            x=10,
            y=70,
            animacao_velocidade=3,
            velocidade=3
        )
        self.todas_as_sprites = pygame.sprite.Group()

        self.todas_as_sprites.add(self.pacman)
        i = 0
        for pos_ini, cor_fantasma in [
            ((136,229), "vermelho"),
            ((280,229), "azul"),
            ((136,328), "amarelo"),
            ((280,328), "rosa"),
        ]:
            fantasma = Fantasma(
                cor=cor_fantasma,
                x=pos_ini[0],
                y=pos_ini[1],
                animacao_velocidade=2,
                velocidade=3,
                labirinto=self.labirinto,
                pacman=self.pacman
            )
            self.todas_as_sprites.add(fantasma)

            i += 1
            if i >= settings.QUANT_FANTASMAS: break
        
        pygame.mixer.Sound(os.path.join("audios", constantes.MUSICA_INICIO)).play()
        self.rodar()
    

    def rodar(self):
        self.jogando = True
        pygame.mixer.music.load(os.path.join("audios", constantes.MUSICA_INICIO))
        pygame.mixer.music.play()

        self.relogio.tick(constantes.FPS)
        self.eventos()
        self.atualizar_sprites()
        self.desenhar_sprites()
        pygame.time.delay(4500)

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

        self.fichas += self.labirinto.pegou_ficha(self.pacman)
            

    def atualizar_sprites(self):
        self.todas_as_sprites.update()

        for sprite in self.todas_as_sprites:
            if isinstance(sprite, Fantasma):
                if sprite.x - 23 <= self.pacman.x <= sprite.x + 23 and sprite.y - 23 <= self.pacman.y <= sprite.y + 23:
                    self.perder_vida()
        
        self.labirinto.gerar_fichas()
                

    def desenhar_sprites(self):
        self.tela.fill(constantes.PRETO)
        self.labirinto.desenhar(self.tela)
        self.todas_as_sprites.draw(self.tela)

        fonte = pygame.font.SysFont("Segoe UI Emoji", 20)
        txt_vidas = fonte.render(f"❤️ {self.vidas}", True, constantes.VERMELHO)
        txt_fichas = fonte.render(f"✅ {self.fichas}", True, constantes.VERDE)
        ficha_txt = fonte.render("✅", True, constantes.VERDE)

        self.tela.blit(txt_vidas, (10, 20))
        self.tela.blit(txt_fichas, (90, 17))

        for x, y in self.labirinto.fichas:
            self.tela.blit(ficha_txt, (x, y))

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

        botao_jogar = Botao((constantes.LARGURA - 200) // 2, 300, 200, 40, "Jogar", constantes.AMARELO, constantes.PRETO)
        botao_instrucoes = Botao((constantes.LARGURA - 200) // 2, 350, 200, 40, "Instruções", constantes.AZUL, constantes.PRETO)
        botao_sair = Botao((constantes.LARGURA - 200) // 2, 400, 200, 40, "Sair", constantes.VERMELHO, constantes.PRETO)

        esperando = True
        while esperando and self.esta_rodando:
            self.relogio.tick(constantes.FPS)
            self.tela.fill(constantes.PRETO)

            self.mostrar_start_logo(constantes.LARGURA // 2, 20)
            botao_jogar.desenhar(self.tela)
            botao_instrucoes.desenhar(self.tela) 
            botao_sair.desenhar(self.tela)
            self.mostrar_texto(
                'Desenvolvido por jonatas.cunha',
                14,
                constantes.BRANCO,
                constantes.LARGURA // 2,
                570
            )
            pygame.display.flip()

            for event in pygame.event.get():
                if botao_jogar.foi_clicado(event):
                    esperando = False
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound(os.path.join(self.diretorio_audios, constantes.TECLA_START)).play()
                if botao_instrucoes.foi_clicado(event):
                    self.mostrar_tela_instrucoes()
                if botao_sair.foi_clicado(event) or event.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False

                if event.type == pygame.KEYUP:
                    pass


    def mostrar_tela_instrucoes(self):
        botao_voltar = Botao((constantes.LARGURA - 200) // 2, constantes.ALTURA - 60, 200, 40, "Voltar", constantes.CINZA, constantes.PRETO)

        spritesheet = pygame.image.load(constantes.SPRITESHEET_PATH).convert_alpha()
        fonte = pygame.font.SysFont("Segoe UI Emoji", 18)

        txt_instrucoes = [
            fonte.render("👉 Mova-se no labirinto usando as setas ← ↑ ↓ →", True, constantes.BRANCO),
            fonte.render("do seu teclado.", True, constantes.BRANCO),
            fonte.render("", True, constantes.BRANCO),
            fonte.render("✅ Sua missão é pegar as fichas que estarão em", True, constantes.BRANCO),
            fonte.render("posições aleatórias no labirinto.", True, constantes.BRANCO),
            fonte.render("", True, constantes.BRANCO),
            fonte.render("👻 Fique longe dos fantasmas! Se você estiver em", True, constantes.BRANCO),
            fonte.render("um mesmo corredor que eles, eles vão ver você e", True, constantes.BRANCO),
            fonte.render("te perseguir!", True, constantes.BRANCO),
            fonte.render("", True, constantes.BRANCO),
            fonte.render("🧱 Se perceber que um fantasma viu você, tente", True, constantes.BRANCO),
            fonte.render("despistá-lo usando as paredes do labirinto!", True, constantes.BRANCO),
            fonte.render("", True, constantes.BRANCO),
            fonte.render("⚠️ Evite pegar fichas que estão muito próximas de", True, constantes.BRANCO),
            fonte.render("fantasmas.", True, constantes.BRANCO),
            fonte.render("", True, constantes.BRANCO),
            fonte.render("☠️ Cuidado! Se suas vidas zerarem, você perde!", True, constantes.BRANCO),
        ]

        mostrando = True
        while mostrando:
            self.relogio.tick(constantes.FPS)
            self.tela.fill(constantes.PRETO)

            self.mostrar_texto(
                'Instruções:',
                22,
                constantes.AMARELO,
                constantes.LARGURA // 2,
                20
            )
            for i in range(len(txt_instrucoes)):
                self.tela.blit(txt_instrucoes[i], (20, 60 + i * 20))

            self.mostrar_texto(
                'Boa gameplay!',
                18,
                constantes.AMARELO,
                constantes.LARGURA // 2,
                constantes.ALTURA - 100
            )

            botao_voltar.desenhar(self.tela)

            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mostrando = False
                    self.esta_rodando = False
                if botao_voltar.foi_clicado(event):
                    mostrando = False
                    

    def reposicionar_sprites(self):
        for sprite in self.todas_as_sprites:
            if isinstance(sprite, Fantasma):
                sprite.parar()
                sprite.rect.topleft = (sprite.x_inicial, sprite.y_inicial)
                sprite.x, sprite.y = sprite.x_inicial, sprite.y_inicial

        self.pacman.rect.topleft = (10, 70)
        self.pacman.x, self.pacman.y = 10, 70
        self.pacman.frames = self.pacman.frame_parado
        self.pacman.image = self.pacman.frames[0]
            
        self.atualizar_sprites()
        self.desenhar_sprites()
        pygame.time.delay(2000)


    def perder_vida(self):
        self.pacman.falecer()

        pygame.mixer.Sound(os.path.join(self.diretorio_audios, constantes.SOM_FALECIMENTO1)).play()
        tempo = pygame.time.get_ticks()
        while pygame.time.get_ticks() - tempo < 1200:
            self.relogio.tick(constantes.FPS)
            self.pacman.image = self.pacman.frames[self.pacman.frame_atual]
            self.pacman.update()
            self.desenhar_sprites()
        pygame.mixer.Sound(os.path.join(self.diretorio_audios, constantes.SOM_FALECIMENTO2)).play()

        self.direcao_atual = None
        self.direcao_desejada = None

        self.vidas -= 1
        if self.vidas > 0:
            self.reposicionar_sprites()
        else:
            self.jogando = False


    def mostrar_tela_game_over(self):
        self.tela.fill(constantes.PRETO)
        pygame.mixer.music.load(os.path.join("audios", constantes.MUSICA_GAME_OVER))
        pygame.mixer.music.play()

        self.mostrar_texto(
            'VOCÊ PERDEU TODAS AS VIDAS...',
            24,
            constantes.VERMELHO,
            constantes.LARGURA // 2,
            260,
        )
        self.mostrar_texto(
            f"{self.fichas} FICHAS OBTIDAS",
            20,
            constantes.AMARELO,
            constantes.LARGURA // 2,
            300
        )
        
        botao_jogar_novamente = Botao((constantes.LARGURA - 300) // 2, constantes.ALTURA - 60, 300, 40, "Jogar novamente", constantes.AMARELO, constantes.PRETO)
        botao_jogar_novamente.desenhar(self.tela)

        pygame.display.flip()

        esperando = True
        while esperando:
            self.relogio.tick(constantes.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    self.esta_rodando = False
                if botao_jogar_novamente.foi_clicado(event):
                    esperando = False
                    self.jogando = False
                    break


def main():
    g = Game()
    g.mostrar_tela_start()

    while g.esta_rodando:
        g.novo_jogo()

        if not g.esta_rodando: break

        g.mostrar_tela_game_over()

        if not g.esta_rodando: break

        g = Game()
        

if __name__ == "__main__":
    main()