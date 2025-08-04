import pygame
import os
import random

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('comicsans', 50)


class Passaro:
    IMGS = IMAGENS_PASSARO # como esse valor é igual para todos os pássaros, ele é colocado como atributo da classe, não do objeto
    # animações da rotação -->  valores que são compartilhados por todos os objetos do tipo Passaro.
    ROTACAO_MAXIMA = 25 # quando ele sobe, ele se inclina para cima (até 25°), depois rotaciona para baixo
    VELOCIDADE_ROTACAO = 20 # velocidade com que o pássaro vira para baixo
    TEMPO_ANIMACAO = 5 #tempo que cada imagem do pássaro deve permanecer antes de trocar para a próxima

    def __init__(self, x, y):
        self.x = x # posição horizontal do pássaro
        self.y = y # posição vertical do pássaro
        self.angulo = 0  # ângulo de rotação inicial
        self.velocidade = 0 # velocidade inicial (queda)
        self.altura = self.y # altura inicial do último pulo
        self.tempo = 0 #tempo que demora pra completar a parábola; equação do "sorvetão"
        self.contagem_imagem = 0 # controle da animação das asas
        self.imagem = Passaro.IMGS[0] # imagem inicial do pássaro

    def pular(self):
        self.velocidade = - 10.5
        self.tempo = 0



class Cano:
    pass

class Chao:
    pass