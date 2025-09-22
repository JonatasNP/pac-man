import pygame


# OFFSETS
OFFSET_X = 20
OFFSET_Y = 80

# DIMENSÕES DA TELA
LARGURA = 448
ALTURA = 600

# TÍTULO DO JOGO
TITULO_JOGO = "PACMAN"

# FPS
FPS = 30

# CORES
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
AMARELO = (244, 233, 51)
VERMELHO = (255, 0, 0)

# IMAGENS
SPRITSHEET = "spritesheet.png"
PACMAN_START_LOGO = "pacman-logo-1.png"

# FONTE
FONTE = "Courier"

# ÁUDIOS
MUSICA_START = "intermission.wav"
TECLA_START = "munch_1.wav"
MUSICA_INICIO = "start.wav"
SOM_FALECIMENTO1 = "death_0.wav"
SOM_FALECIMENTO2 = "death_1.wav"
MUSICA_GAME_OVER = "game_over.mp3"

#PATHS
SPRITESHEET_PATH='imagens/spritesheet.png'


#FRAMES------
PACMAN_FRAMES = {
    "parado": [(487, 0, 16, 16)],
    "direita": [(455 + i*16, 0, 16, 16) for i in range(3)],
    "esquerda": [(455 + i*16, 16, 16, 16) for i in range(2)] + [(487, 0, 16, 16)],
    "cima": [(455 + i*16, 32, 16, 16) for i in range(2)] + [(487, 0, 16, 16)],
    "baixo": [(455 + i*16, 48, 16, 16) for i in range(2)] + [(487, 0, 16, 16)],
    
    "falecendo": [(487 + i*16, 0, 16, 16) for i in range(12)],
}
TILE_SIZE = 28
LABIRINTO_COM_BOLINHAS = (0, 0, 224, 248)
LABIRINTO_SEM_BOLINHAS = (228, 0, 224, 248)


FANTASMA_FRAMES = {
    "vermelho": {
        "direita": [(455 + i*16, 64, 16, 16) for i in range(2)],
        "esquerda": [(487 + i*16, 64, 16, 16) for i in range(2)],
        "cima": [(519 + i*16, 64, 16, 16) for i in range(2)],
        "baixo": [(551 + i*16, 64, 16, 16) for i in range(2)]
    },
    "rosa": {
        "direita": [(455 + i*16, 80, 16, 16) for i in range(2)],
        "esquerda": [(487 + i*16, 80, 16, 16) for i in range(2)],
        "cima": [(519 + i*16, 80, 16, 16) for i in range(2)],
        "baixo": [(551 + i*16, 80, 16, 16) for i in range(2)]
    },
    "azul": {
        "direita": [(455 + i*16, 96, 16, 16) for i in range(2)],
        "esquerda": [(487 + i*16, 96, 16, 16) for i in range(2)],
        "cima": [(519 + i*16, 96, 16, 16) for i in range(2)],
        "baixo": [(551 + i*16, 96, 16, 16) for i in range(2)]
    },
    "amarelo": {
        "direita": [(455 + i*16, 112, 16, 16) for i in range(2)],
        "esquerda": [(487 + i*16, 112, 16, 16) for i in range(2)],
        "cima": [(519 + i*16, 112, 16, 16) for i in range(2)],
        "baixo": [(551 + i*16, 112, 16, 16) for i in range(2)]
    }
}