import pygame
import sys
import random

DIFICULDADES = {
    'facil':         {'bola': 2.6, 'erro': 120, 'freq': 20, 'vel_ia': 1.5},
    'medio':         {'bola': 3.38, 'erro': 100, 'freq': 30, 'vel_ia': 2.0},
    'dificil':       {'bola': 4.39, 'erro': 70,  'freq': 40, 'vel_ia': 2.3},
    'muito_dificil': {'bola': 5.71, 'erro': 40,  'freq': 50, 'vel_ia': 2.7},
}

som_ativado = True
musica_ativada = True
largura_tela, altura_tela = 640, 480

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
    def __init__(self, velocidade):
        self.rect = pygame.Rect(largura_tela // 2 - 15, altura_tela // 2 - 15, 30, 30)
        self.velocidade_x = random.choice((velocidade, -velocidade))
        self.velocidade_y = random.choice((velocidade, -velocidade))

    def mover(self):
        self.rect.x += self.velocidade_x
        self.rect.y += self.velocidade_y

        if self.rect.top <= 0 or self.rect.bottom >= altura_tela:
            self.velocidade_y = -self.velocidade_y

        if self.rect.left <= 0:
            paleta2.pontuacao += 1
            self.velocidade_x = -self.velocidade_x
        elif self.rect.right >= largura_tela:
            paleta1.pontuacao += 1
            self.velocidade_x = -self.velocidade_x

def desenhar_texto(texto, tamanho, cor, y, fonte_custom=None, alinhamento_centro=True):
    fonte = pygame.font.Font(fonte_custom or None, tamanho)
    superficie = fonte.render(texto, True, cor)
    if alinhamento_centro:
        rect = superficie.get_rect(center=(largura_tela // 2, y))
    else:
        rect = superficie.get_rect(topleft=(10, y))
    tela.blit(superficie, rect)

def tocar_som(nome):
    if som_ativado:
        try:
            pygame.mixer.Sound(f"{nome}.wav").play()
        except Exception as e:
            print(f"Erro ao tocar som '{nome}':", e)

def tocar_musica():
    if musica_ativada:
        try:
            pygame.mixer.music.load("musica.ogg")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Erro ao carregar música: {e}")
    else:
        pygame.mixer.music.stop()

def jogar(nivel):
    config = DIFICULDADES[nivel]
    global paleta1, paleta2
    paleta1 = Paleta(50, altura_tela // 2 - 70)
    paleta2 = Paleta(largura_tela - 60, altura_tela // 2 - 70)
    bola = Bola(config['bola'])
    clock = pygame.time.Clock()
    erro_ia = random.randint(-config['erro'], config['erro'])

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]: paleta1.mover("cima")
        if teclas[pygame.K_DOWN]: paleta1.mover("baixo")

        alvo_ia = bola.rect.centery + erro_ia
        if alvo_ia < paleta2.rect.centery:
            paleta2.rect.y -= config['vel_ia']
        elif alvo_ia > paleta2.rect.centery:
            paleta2.rect.y += config['vel_ia']

        if random.randint(0, config['freq']) == 1:
            erro_ia = random.randint(-config['erro'], config['erro'])

        bola.mover()

        if bola.rect.colliderect(paleta1.rect) or bola.rect.colliderect(paleta2.rect):
            bola.velocidade_x = -bola.velocidade_x
            tocar_som("ping")

        tela.fill((10, 0, 20))
        pygame.draw.rect(tela, (255, 255, 0), paleta1.rect)
        pygame.draw.rect(tela, (0, 255, 255), paleta2.rect)
        pygame.draw.ellipse(tela, (255, 255, 255), bola.rect)
        desenhar_texto(f"{paleta1.pontuacao}   x   {paleta2.pontuacao}", 48, (255, 0, 255), 40)
        desenhar_texto("ENTER ou ESPAÇO para voltar ao menu", 20, (180, 180, 180), 460)
        pygame.display.flip()
        clock.tick(60)
def tela_configuracoes():
    global som_ativado, musica_ativada
    botao_som = pygame.Rect(220, 200, 250, 40)
    botao_musica = pygame.Rect(220, 250, 250, 40)
    botao_voltar = pygame.Rect(10, 10, 120, 35)
    while True:
        tela.fill((10, 10, 25))
        desenhar_texto("CONFIGURAÇÕES", 40, (255, 255, 0), 100, "arcade.ttf")
        pygame.draw.rect(tela, (60, 60, 100), botao_som)
        pygame.draw.rect(tela, (60, 60, 100), botao_musica)
        estado_som = "Ativado" if som_ativado else "Desativado"
        estado_musica = "Ativada" if musica_ativada else "Desativada"
        desenhar_texto(f"Som: {estado_som}", 24, (255, 255, 255), 215)
        desenhar_texto(f"Música: {estado_musica}", 24, (255, 255, 255), 265)
        desenhar_texto("Clique para alternar ou pressione ESC para voltar", 20, (180, 180, 180), 400)
        pygame.draw.rect(tela, (80, 80, 120), botao_voltar)
        desenhar_texto("Voltar", 20, (255, 255, 255), 15, alinhamento_centro=False)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if botao_som.collidepoint(e.pos):
                    som_ativado = not som_ativado
                    tocar_som("click")
                if botao_musica.collidepoint(e.pos):
                    musica_ativada = not musica_ativada
                    tocar_som("click")
                    tocar_musica()
                if botao_voltar.collidepoint(e.pos):
                    tocar_som("click")
                    return

def tela_dificuldade():
    botoes = [
        {'texto': 'Fácil', 'nivel': 'facil', 'rect': pygame.Rect(220, 180, 200, 40)},
        {'texto': 'Médio', 'nivel': 'medio', 'rect': pygame.Rect(220, 230, 200, 40)},
        {'texto': 'Difícil', 'nivel': 'dificil', 'rect': pygame.Rect(220, 280, 200, 40)},
        {'texto': 'Muito Difícil', 'nivel': 'muito_dificil', 'rect': pygame.Rect(220, 330, 200, 40)}
    ]
    while True:
        tela.fill((15, 15, 25))
        desenhar_texto("SELECIONE A DIFICULDADE", 28, (255, 255, 0), 100, "arcade.ttf")
        for botao in botoes:
            cor = (90, 30, 100) if botao['rect'].collidepoint(pygame.mouse.get_pos()) else (50, 20, 60)
            pygame.draw.rect(tela, cor, botao['rect'])
            desenhar_texto(botao['texto'], 24, (255, 255, 255), botao['rect'].y + 20)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    if botao['rect'].collidepoint(e.pos):
                        tocar_som("click")
                        return botao['nivel']
            if e.type == pygame.KEYDOWN:
                if e.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return

def tela_inicial():
    piscando = True
    timer = 0
    fonte = "arcade.ttf"
    botoes = [
        {'texto': 'Jogar', 'acao': 'jogar', 'rect': pygame.Rect(250, 250, 140, 40)},
        {'texto': 'Configurações', 'acao': 'config', 'rect': pygame.Rect(250, 310, 140, 40)}
    ]
    while True:
        tela.fill((0, 0, 0))
        if piscando:
            desenhar_texto("RETRO PONG", 48, (255, 0, 255), 120, fonte)
        timer += 1
        if timer % 40 == 0:
            piscando = not piscando

        for botao in botoes:
            cor = (80, 0, 120) if botao['rect'].collidepoint(pygame.mouse.get_pos()) else (50, 0, 90)
            pygame.draw.rect(tela, cor, botao['rect'])
            desenhar_texto(botao['texto'], 28, (255, 255, 255), botao['rect'].y + 20, fonte)
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    if botao['rect'].collidepoint(e.pos):
                        tocar_som("click")
                        return botao['acao']

def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    global tela
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Retro Pong")
    tocar_musica()

    while True:
        escolha = tela_inicial()
        if escolha == 'config':
            tela_configuracoes()
        elif escolha == 'jogar':
            nivel = tela_dificuldade()
            if nivel:
                jogar(nivel)

if __name__ == '__main__':
    main()
