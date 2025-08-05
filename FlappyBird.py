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
        self.imagem = self.IMGS[0] # imagem inicial do pássaro

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo #S = so + vot + at*2/2

        #restringir o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        #angulo do passaro (corrigido operador de comparação)
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # definir qual imagem do passaro vou usar
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        else:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # se o passaro tiver caindo, não bate asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(imagem_rotacionada, retangulo.topleft)

    # colisão de pixel perfeita / mask - retangulo de cada pixel
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x): # y é gerado aleatoriamente
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False


class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0: # se o bloco 1 saiu da tela
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


def desenhar_tela(tela, passaro, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos} ", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def tela_game_over(tela, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))

    texto_game_over = FONTE_PONTOS.render("GAME OVER", True, (255, 0, 0))
    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", True, (255, 255, 255))
    texto_restart = pygame.font.SysFont('comicsans', 30).render("Pressione ESPAÇO para reiniciar", True, (255, 255, 255))

    centro_y = TELA_ALTURA // 2
    espaco = 50  # distância entre Game Over e Pontuação
    espaco_extra = 90  # distância maior antes do "Pressione Espaço"

    tela.blit(texto_game_over, (TELA_LARGURA // 2 - texto_game_over.get_width() // 2, centro_y - espaco * 2))
    tela.blit(texto_pontos, (TELA_LARGURA // 2 - texto_pontos.get_width() // 2, centro_y))
    tela.blit(texto_restart, (TELA_LARGURA // 2 - texto_restart.get_width() // 2, centro_y + espaco_extra))

    pygame.display.update()

    esperando = True
    while esperando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                esperando = False


def main():
    passaro = Passaro(230, 350)
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        #interação com o usuário
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    passaro.pular()

        #mover as coisas
        passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            if cano.colidir(passaro):
                tela_game_over(tela, pontos)
                return
            if not cano.passou and passaro.x > cano.x:
                cano.passou = True
                adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
            tela_game_over(tela, pontos)
            return

        desenhar_tela(tela, passaro, canos, chao, pontos)


if __name__ == "__main__":
    while True:  # loop para reiniciar o jogo
        main()
