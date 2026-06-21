# 1.Imports:
import pygame
import random

# 2.Iniciação e Janela:
pygame.init()

x, y = 512, 1024
window = pygame.display.set_mode((x, y))
pygame.display.set_caption('Space Striker')

clock = pygame.time.Clock()
loop = True

# 3.Cenario:
Cenario = pygame.image.load('Cenario/Cenario.webp')
Cenario = pygame.transform.scale(Cenario, (x, y))

# 4.A)Sprite da nave do player:
NavePlayer    = pygame.image.load('SpriterPlayerNave/Nave_Player.png').convert_alpha()
NaveDireita1  = pygame.image.load('SpriterPlayerNave/Nave_Player_Direita_1.png').convert_alpha()
NaveDireita2  = pygame.image.load('SpriterPlayerNave/Nave_Player_Direita_2.png').convert_alpha()
NaveEsquerda1 = pygame.image.load('SpriterPlayerNave/Nave_Player_Esquerda_1.png').convert_alpha()
NaveEsquerda2 = pygame.image.load('SpriterPlayerNave/Nave_Player_Esquerda_2.png').convert_alpha()
NaveEntrada1  = pygame.image.load('SpriterPlayerNave/Nave_Player_Entrada_1.png').convert_alpha()
NaveEntrada2  = pygame.image.load('SpriterPlayerNave/Nave_Player_Entrada_2.png').convert_alpha()
NaveEntrada3  = pygame.image.load('SpriterPlayerNave/Nave_Player_Entrada_3.png').convert_alpha()
NaveEntrada4  = pygame.image.load('SpriterPlayerNave/Nave_Player_Entrada_4.png').convert_alpha()
NaveDano = pygame.image.load('SpriterPlayerNave/Nave_Player_Dano_Recebido.png').convert_alpha()
NaveDano = pygame.transform.scale(NaveDano, (NavePlayer.get_width(), NavePlayer.get_height()))

# 4.B) Sprite da barra de vida:
BarraVida = pygame.image.load('Nível de Barra de Vida\Barra_De_Vida.png').convert_alpha()
BarraVida = pygame.transform.scale(BarraVida, (260, 55))

# 4.C) Frames da explosão:
Explosao1 = pygame.image.load('Efeito de explosão\Explosao_1.png').convert_alpha()
Explosao2 = pygame.image.load('Efeito de explosão\Explosao_2.png').convert_alpha()
Explosao3 = pygame.image.load('Efeito de explosão\Explosao_3.png').convert_alpha()
Explosao4 = pygame.image.load('Efeito de explosão\Explosao_4.png').convert_alpha()
Explosao5 = pygame.image.load('Efeito de explosão\Explosao_5.png').convert_alpha()
Explosao6 = pygame.image.load('Efeito de explosão\Explosao_6.png').convert_alpha()
explosao_frames = [Explosao1, Explosao2, Explosao3, Explosao4, Explosao5, Explosao6]

# 4.D) Sprite do inimigo
Dash = pygame.image.load('InimigoDash\Dash.png').convert_alpha()
Dash = pygame.transform.scale(Dash, (80, 31))

# 5.Estado do jogo:

# (Fonte utilizada no jogo):
fonte = pygame.font.Font('Fonte/PressStart2P-Regular.ttf', 24)

# 5.A) Pontuação:
pontos = 0

# 5.B) Player:
nave_largura = NavePlayer.get_width()
nave_altura = NavePlayer.get_height()
nave_x = (x - nave_largura) // 2
nave_y = y
NAVE_Y_FINAL = y - nave_altura - 50
VEL_NAVE = 16
VEL_ENTRADA = 4
RITMO_ANIMACAO = 6
nave_entrada  = [NaveEntrada1, NaveEntrada2, NaveEntrada3, NaveEntrada4]
frame_entrada = 0
contador_entrada = 0
nave_parada   = [NavePlayer]
nave_direita  = [NaveDireita1, NaveDireita2]
nave_esquerda = [NaveEsquerda1, NaveEsquerda2]
animacao_atual = nave_parada
frame_atual = 0
contador = 0

# 5.C) Tiros do Player:
tiros = []
VEL_TIRO = 16
cooldown_tiro = 0
COOLDOWN_TIRO = 23

# 5.D) Inimigos:
inimigos = []
LIMITE_INIMIGOS = 6
inimigo_largura = 80
inimigo_altura = 31
VEL_INIMIGO = 6
INIMIGO_ALVO_MIN = 80
INIMIGO_ALVO_MAX = 260
VEL_PATRULHA = 5

# 5.E) Vida do Player:
vidas = 5
VIDA_MAX = 5
BARRA_X  = 10
BARRA_Y  = 85
PAD_X    = 8
PAD_Y    = 6
MIOLO_W  = 210
MIOLO_H  = 24

# 5.F) Estado do jogo:
estado = "entrada"
PONTOS_VITORIA = 2000

# 5.G) Tiro do inimigo:
tiros_inimigos = []
VEL_TIRO_INI = 8

# 5.H) Animação do cenário:
fundo_y = 0
VEL_FUNDO = 5

# 5.I) Explosões:
RITMO_EXPLOSAO = 4 
explosoes = []

# 5.J) i-frames
invencivel = False
tempo_invencivel = 0
DURACAO_IFRAME = 90
RITMO_PISCA = 6 

# 6.Funções:
def animar(animacao_atual, frame_atual, contador):
    contador += 1
    if contador >= RITMO_ANIMACAO:
        contador = 0
        frame_atual += 1
    frame_atual = frame_atual % len(animacao_atual)
    return animacao_atual[frame_atual], frame_atual, contador

class Inimigo:
    def __init__(self):                                     
        self.rect = pygame.Rect(0, 0, inimigo_largura, inimigo_altura)
        self.nascer()

    def nascer(self):
        self.rect.x = random.randint(0, x - inimigo_largura)
        self.rect.y = random.randint(-300, -inimigo_altura)
        self.alvo_y = random.randint(INIMIGO_ALVO_MIN, INIMIGO_ALVO_MAX)
        self.parou = False
        self.dir = random.choice([-1, 1])
        self.cooldown = random.randint(30, 120)

    def atualizar(self):
        if not self.parou:
            self.rect.y += VEL_INIMIGO
            if self.rect.y >= self.alvo_y:
                self.rect.y = self.alvo_y
                self.parou = True
        else:
            self.rect.x += self.dir * VEL_PATRULHA
            if self.rect.x <= 0:
                self.rect.x = 0
                self.dir = 1
            elif self.rect.x >= x - inimigo_largura:
                self.rect.x = x - inimigo_largura
                self.dir = -1
    
class Explosao:
    def __init__(self, cx, cy):
            self.cx = cx
            self.cy = cy
            self.frame_atual = 0
            self.contador = 0
            self.acabou = False

    def atualizar(self):
        self.contador += 1
        if self.contador >= RITMO_EXPLOSAO:
            self.contador = 0
            self.frame_atual += 1
            if self.frame_atual >= len(explosao_frames):
                self.acabou = True

    def desenhar(self, tela):
        if not self.acabou:
            img = explosao_frames[self.frame_atual]
            tela.blit(img, img.get_rect(center=(self.cx, self.cy)))

# 7.Laço Principal:
while loop:
    # 7.A) Eventos:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            loop = False
        if estado != "jogando":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    pontos = 0
                    vidas = 5
                    nave_x = (x - nave_largura) // 2
                    nave_y = y
                    frame_entrada = 0
                    contador_entrada = 0
                    tiros.clear()
                    inimigos.clear()
                    tiros_inimigos.clear()
                    explosoes.clear()
                    estado = "entrada"
                    invencivel = False
                    tempo_invencivel = 0

    # ===== ESTADO: JOGANDO =====
    if estado == "jogando":
        #7.B) ativar o i-frames
        if invencivel:
            tempo_invencivel -= 1
            if tempo_invencivel <= 0:
                invencivel = False 
        # 7.C) mover a nave + prender na tela
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_a]: nave_x -= VEL_NAVE
        if teclas[pygame.K_d]: nave_x += VEL_NAVE
        if teclas[pygame.K_w]: nave_y -= VEL_NAVE
        if teclas[pygame.K_s]: nave_y += VEL_NAVE
        if nave_x < 0: nave_x = 0
        if nave_x > x - nave_largura: nave_x = x - nave_largura
        if nave_y < 0: nave_y = 0
        if nave_y > y - nave_altura: nave_y = y - nave_altura
        
        if teclas[pygame.K_a]:
            animacao_atual = nave_esquerda
        elif teclas[pygame.K_d]:
            animacao_atual = nave_direita
        else:
            animacao_atual = nave_parada
        imagem_nave, frame_atual, contador = animar(animacao_atual, frame_atual, contador)

        
        fundo_y += VEL_FUNDO
        if fundo_y >= y:
            fundo_y = 0

        # 7.D) atirar
        if cooldown_tiro > 0:
            cooldown_tiro -= 1
        botoes = pygame.mouse.get_pressed()
        
        if botoes[0] and cooldown_tiro == 0:
            tiros.append(pygame.Rect(nave_x + nave_largura // 2, nave_y, 4, 16))
            cooldown_tiro = COOLDOWN_TIRO
        
        for tiro in tiros[:]:
            tiro.y -= VEL_TIRO
            if tiro.y < 0:
                tiros.remove(tiro)

        # 7.E) inimigos
        if len(inimigos) < LIMITE_INIMIGOS:
            inimigos.append(Inimigo())
        
        for inimigo in inimigos:
            inimigo.atualizar()

        # 7.F) colisões
        nave_rect = pygame.Rect(nave_x, nave_y, nave_largura, nave_altura)
        for inimigo in inimigos:
            if nave_rect.colliderect(inimigo.rect):
                inimigo.nascer()
                if not invencivel:
                    vidas -= 1
                    invencivel = True
                    tempo_invencivel = DURACAO_IFRAME
            
            for tiro in tiros[:]:
                if tiro.colliderect(inimigo.rect):
                    tiros.remove(tiro)
                    explosoes.append(Explosao(inimigo.rect.centerx, inimigo.rect.centery))
                    inimigo.nascer()
                    pontos += 10
                    break

        for ex in explosoes[:]:
            ex.atualizar()
            if ex.acabou:
                explosoes.remove(ex)

        # 7.G) inimigo atira
        for inimigo in inimigos:
            if inimigo.parou:
                inimigo.cooldown -= 1
                if inimigo.cooldown <= 0:
                    bala = pygame.Rect(inimigo.rect.centerx - 2, inimigo.rect.bottom, 4, 16)
                    tiros_inimigos.append(bala)
                    inimigo.cooldown = random.randint(60, 150)

        for bala in tiros_inimigos[:]:
            bala.y += VEL_TIRO_INI
            if bala.y > y:
                tiros_inimigos.remove(bala)
            elif bala.colliderect(nave_rect):
               tiros_inimigos.remove(bala)
               if not invencivel:
                    vidas -= 1
                    invencivel = True
                    tempo_invencivel = DURACAO_IFRAME

        # 7.H) verificação do fim de jogo
        if pontos >= PONTOS_VITORIA: estado = "venceu"
        if vidas <= 0: estado = "perdeu"

        # 7.J) desenhos
        window.blit(Cenario, (0, fundo_y)) 
        window.blit(Cenario, (0, fundo_y - y))
        imagem_desenhar = imagem_nave
        if invencivel and (tempo_invencivel // RITMO_PISCA) % 2 == 0:
            imagem_desenhar = NaveDano
        window.blit(imagem_desenhar, (nave_x, nave_y))
        for inimigo in inimigos:
            window.blit(Dash, inimigo.rect)
            for ex in explosoes:
                ex.desenhar(window)
        for tiro in tiros:
            pygame.draw.rect(window, (0, 255, 255), tiro)
        for bala in tiros_inimigos:
            pygame.draw.rect(window, (255, 150, 0), bala)

        window.blit(fonte.render(f'Pontos: {pontos}', True, (255, 255, 255)), (10, 10))
        window.blit(BarraVida, (BARRA_X, BARRA_Y))
        largura_verde = int(MIOLO_W * vidas / VIDA_MAX)
        if largura_verde > 0:
            pygame.draw.rect(window, (0, 220, 90),(BARRA_X + PAD_X, BARRA_Y + PAD_Y, largura_verde, MIOLO_H))

    # ===== ESTADO: ENTRADA =====
    elif estado == "entrada":
        fundo_y += VEL_FUNDO
        if fundo_y >= y:
            fundo_y = 0
        if nave_y > NAVE_Y_FINAL:
            nave_y -= VEL_ENTRADA
        else:
            nave_y = NAVE_Y_FINAL
            estado = "jogando"
        
        contador_entrada += 1
        if contador_entrada >= RITMO_ANIMACAO:
            contador_entrada = 0
            if frame_entrada < len(nave_entrada) - 1:
                frame_entrada += 1
        window.blit(Cenario, (0, fundo_y))
        window.blit(Cenario, (0, fundo_y - y))
        window.blit(nave_entrada[frame_entrada], (nave_x, nave_y))

    # ===== ESTADO: VENCEU =====
    elif estado == "venceu":
        window.fill((0, 20, 0))
        msg = fonte.render('VOCE VENCEU!', True, (0, 255, 100))
        window.blit(msg, (x // 2 - msg.get_width() // 2, y // 2 - 50))
        dica = fonte.render('Aperte R', True, (255, 255, 255))
        window.blit(dica, (x // 2 - dica.get_width() // 2, y // 2 + 20))

    # ===== ESTADO: PERDEU =====
    elif estado == "perdeu":
        window.fill((20, 0, 0))
        msg = fonte.render('GAME OVER', True, (255, 50, 50))
        window.blit(msg, (x // 2 - msg.get_width() // 2, y // 2 - 50))
        dica = fonte.render('Aperte R', True, (255, 255, 255))
        window.blit(dica, (x // 2 - dica.get_width() // 2, y // 2 + 20))

    pygame.display.update()
    clock.tick(60)

pygame.quit()