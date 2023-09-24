import pygame
import sys
import random

class Paleta:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 140)
        self.velocidade = 5
        self.pontuacao = 0

    def mover(self, direcao):
        if direcao == "cima" and self.rect.top > 0:
            self.rect.y -= self.velocidade
        elif direcao == "baixo" and self.rect.bottom < altura_tela:
            self.rect.y += self.velocidade

class Bola:
    def __init__(self):
        self.rect = pygame.Rect(largura_tela // 2 - 15, altura_tela // 2 - 15, 30, 30)
        self.velocidade_x = random.choice((1.5, -1.5))
        self.velocidade_y = random.choice((1.5, -1.5))

    def mover(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

    def reiniciar(self):
        self.rect.x = largura_tela // 2 - 15
        self.rect.y = altura_tela // 2 - 15
        self.velocidade_x = random.choice((1.5, -1.5))
        self.velocidade_y = random.choice((1.5, -1.5))

def desenhar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.Font(None, tamanho)
    superficie_texto = fonte.render(texto, True, cor)
    tela.blit(superficie_texto, (x, y))

pygame.init()

largura_tela = 640
altura_tela = 480
cor_fundo = (0, 0, 0)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Ping Pong")

cor_branca = (255, 255, 255)

paleta1 = Paleta(50, altura_tela // 2 - 70)
paleta2 = Paleta(largura_tela - 60, altura_tela // 2 - 70)
bola = Bola()


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]:
        paleta1.mover("cima")
    if teclas[pygame.K_DOWN]:
        paleta1.mover("baixo")

    
    if bola.rect.centery < paleta2.rect.centery:
        paleta2.mover("cima")
    elif bola.rect.centery > paleta2.rect.centery:
        paleta2.mover("baixo")

    bola.mover()


    if paleta1.rect.collidepoint(bola.rect.center):
        bola.velocidade_x = -bola.velocidade_x
        bola.velocidade_x *= 1.1  
        paleta1.pontuacao += 1

    if paleta2.rect.collidepoint(bola.rect.center):
        bola.velocidade_x = -bola.velocidade_x
        bola.velocidade_x *= 1.1  
        paleta2.pontuacao += 1


    if bola.rect.top <= 0 or bola.rect.centery >= altura_tela:
        bola.velocidade_y = -bola.velocidade_y

    if bola.rect.left <= 0:
        paleta2.pontuacao += 1
        bola.reiniciar()

    if bola.rect.right >= largura_tela:
        paleta1.pontuacao += 1
        bola.reiniciar()

    tela.fill(cor_fundo)
    pygame.draw.rect(tela, cor_branca, paleta1.rect)
    pygame.draw.rect(tela, cor_branca, paleta2.rect)
    pygame.draw.ellipse(tela, cor_branca, bola.rect)


    desenhar_texto(f'Pontuação: {paleta1.pontuacao}', 36, cor_branca, 10, 10)
    desenhar_texto(f'Pontuação: {paleta2.pontuacao}', 36, cor_branca, largura_tela - 200, 10)

    pygame.display.flip()
