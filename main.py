# /*******************************************************************************
# Autor: Renan Pires Andrade
# Componente Curricular: Algoritmos I
# Concluido em: 18/10/2011
# Declaro que este código foi elaborado por mim de forma individual e não contém nenhum
# trecho de código de outro colega ou de outro autor, tais como provindos de livros e
# apostilas, e páginas ou documentos eletrônicos da Internet. Qualquer trecho de código
# de outra autoria que não a minha está destacado com uma citação para o autor e a fonte
# do código, e estou ciente que estes trechos não serão considerados para fins de avaliação.
# ******************************************************************************************/

import pygame
import sys
import random

# ESTADOS DO JOGO
estado_atual = "MENU"
dificuldade = ""
FPS = 60
TAMANHO_CELULA = 45 # 40x40 pixels
angulo = 0

# CORES
preto = (0, 0, 0)
branco = (255, 255, 255)
VERDE_ESCURO = (0, 150, 0) # 2: Cabeça Cobra
VERDE_CLARO = (50, 200, 50) # 1: Corpo Cobra
vermelho = (255, 0, 0) # 4: Fruta Ruim
verde = (0, 255, 0) # 3: Fruta Boa
azul = (34, 75, 117)
verde_faixa = (25, 64, 18)
bege_faixa = (117, 91, 34)

pygame.init()

# SOM
pygame.mixer.init()
pygame.mixer.music.load('sons\hot-mean-192400.mp3')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
som_fruta_boa = pygame.mixer.Sound(r'sons\Acquire.wav')
som_fruta_ruim = pygame.mixer.Sound(r'sons\retro_you_lose.wav')

largura, altura = 800, 700
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snakeee")
clock = pygame.time.Clock()

# IMAGENS
imagem_fundo = pygame.image.load(r'imagens\menu-backgound.png').convert_alpha()
imagem_grama = pygame.image.load(r'imagens\fundo-grama-jogo.png').convert_alpha()
imagem_fruta_boa = pygame.image.load(r'imagens\fruta-boa.png').convert_alpha()
imagem_fruta_ruim = pygame.image.load(r'imagens\fruta-ruim.png').convert_alpha()
imagem_corpo_cobra = pygame.image.load(r'imagens\corpo_cobra.png').convert_alpha()
imagem_cabeca_cobra = pygame.image.load(r'imagens\cabeca-cobra.png').convert_alpha()
img_fruta_boa = pygame.transform.scale(imagem_fruta_boa, (TAMANHO_CELULA, TAMANHO_CELULA))
img_fruta_ruim = pygame.transform.scale(imagem_fruta_ruim, (TAMANHO_CELULA, TAMANHO_CELULA))
img_corpo_cobra = pygame.transform.scale(imagem_corpo_cobra, (TAMANHO_CELULA, TAMANHO_CELULA))
img_cabeca_cobra = pygame.transform.scale(imagem_cabeca_cobra, (TAMANHO_CELULA, TAMANHO_CELULA))

# FONTES
fonte_padrao = pygame.font.SysFont(None, 72)
fonte_comic = pygame.font.SysFont('Comic Sans MS', 60)
fonte_menus = pygame.font.SysFont(None, 52)

cor_fundo=(60, 60, 60)
cor_borda=(200, 200, 200)
cor_texto=(255, 255, 255)

def criar_botao(texto, posicao_y, largura_botao=250, altura_botao=60):
    x_centro = largura // 2

    # cria retangulo botao
    botao_rect = pygame.Rect(0, 0, largura_botao, altura_botao)
    botao_rect.center = (x_centro, posicao_y)

    # fundo do botao
    pygame.draw.rect(tela, cor_fundo, botao_rect, border_radius=12)
    # borda
    pygame.draw.rect(tela, cor_borda, botao_rect, width=2, border_radius=12)

    texto_renderizado = fonte_menus.render(texto, True, cor_texto)
    texto_rect = texto_renderizado.get_rect(center=botao_rect.center)
    tela.blit(texto_renderizado, texto_rect)

    return texto_renderizado, botao_rect

def gerar_matriz(largura, altura, matriz_tabuleiro):
    # Eixo (Y, X)
    for y in range(altura):
        linha = []
        for x in range(largura):
            linha.append(0)
        matriz_tabuleiro.append(linha)

def gerar_cobra(matriz_tabuleiro, matriz_cobra):
    matriz_cobra.append([0, 0])
    matriz_cobra.append([0, 1])
    matriz_tabuleiro[0][1] = 2
    matriz_tabuleiro[0][0] = 1

def gerar_fruto(largura, altura, matriz_tabuleiro, tipo_fruta):
    while True:
        fruto_x = random.randint(0, largura - 1)
        fruto_y = random.randint(0, altura - 1)
        if matriz_tabuleiro[fruto_y][fruto_x] == 0:
            matriz_tabuleiro[fruto_y][fruto_x] = tipo_fruta;
            return

def desenhar_tabuleiro(celulas_por_coluna, celulas_por_linha, matriz_tabuleiro):
    largura_total_tabuleiro = celulas_por_linha * TAMANHO_CELULA + celulas_por_linha
    altura_total_tabuleiro = celulas_por_coluna * TAMANHO_CELULA + celulas_por_coluna
    margem_x = (largura - largura_total_tabuleiro) // 2
    margem_y = (altura - altura_total_tabuleiro) // 2
    cor_borda = branco
    espessura_borda = 1
    for linha in range(celulas_por_coluna):
        for coluna in range(celulas_por_linha):
            x = margem_x + coluna * TAMANHO_CELULA
            y = margem_y + linha * TAMANHO_CELULA
            celula = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
            cor_interior = preto
            match matriz_tabuleiro[linha][coluna]:
                case 0:
                    pass
                case 1:
                    cor_interior = VERDE_CLARO
                    tela.blit(img_corpo_cobra, celula)
                case 2:
                    cor_interior = VERDE_ESCURO
                    img_cabeca_cobra_rotacionada = pygame.transform.rotate(img_cabeca_cobra, angulo)
                    tela.blit(img_cabeca_cobra_rotacionada, celula)
                case 3:
                    cor_interior = verde
                    tela.blit(img_fruta_boa, celula)
                case 4:
                    cor_interior = vermelho
                    tela.blit(img_fruta_ruim, celula)
            # BORDA TABULEIRO
            # pygame.draw.rect(tela, cor_borda, celula, espessura_borda)

def movimentar_cobra(direcao, matriz_cobra, matriz, CELULAS_X, CELULAS_Y):
    """Retorna o status do jogo"""
    primeiro_y, primeiro_x = matriz_cobra[0] 
    ultimo_y, ultimo_x = matriz_cobra[-1]
    novo_y, novo_x = ultimo_y, ultimo_x

    match direcao:
        case 'a':
            novo_x = ultimo_x - 1
        case 'd':
            novo_x = ultimo_x + 1
        case 'w':
            novo_y = ultimo_y - 1
        case 's':
            novo_y = ultimo_y + 1

    # CHECAR COLISÕES
    # parede
    if (novo_x < 0 or novo_x >= CELULAS_X) or (novo_y < 0 or novo_y >= CELULAS_Y):
        return "GAME_OVER"
    # Guarda o valor do proximo elemento da matriz
    valor_proximo_elemento = matriz[novo_y][novo_x]
    # bateu no proprio corpo
    if valor_proximo_elemento == 1:
        return "GAME_OVER"

    status = "OK" # retorno padrão

    # FRUTAS
    if valor_proximo_elemento == 3: # BOA
        # Não apaga a cauda
        matriz_cobra.append([novo_y, novo_x])
        status = "FRUTA_BOA"

    elif valor_proximo_elemento == 4: # RUIM
        matriz_cobra.append([novo_y, novo_x])

        for c in range(3):
            if len(matriz_cobra) > 1:
                y, x = matriz_cobra.pop(0)
                matriz[y][x] = 0
            else:
                return "GAME_OVER"
            
        if len(matriz_cobra) <= 1:
            return "GAME_OVER"
        status = "FRUTA_RUIM"

    elif valor_proximo_elemento == 0:
        matriz_cobra.append([novo_y, novo_x])
        matriz[primeiro_y][primeiro_x] = 0
        del matriz_cobra[0]

    for y in range(len(matriz)):
        for x in range(len(matriz[y])):
            if matriz[y][x] in (1, 2):
                matriz[y][x] = 0

    # INSERE COBRA NA MATRIZ
    for i in range(len(matriz_cobra)):
        y, x = matriz_cobra[i]
        if i == len(matriz_cobra) -1:
            matriz[y][x] = 2
        else:
            matriz[y][x] = 1
    return status

def verificar_vitoria(matriz, pontos, max_pontos):
    # matriz cheia
    if not any(0 in linha for linha in matriz):
        return True
    # atingiu max pontos
    if pontos >= max_pontos:
        return True
    return False

# TIMER
def velocidade_cobra(velocidade_cobra):
    intervalo_movimento = 1000 / velocidade_cobra
    return intervalo_movimento
ultimo_movimento_tempo = 0


# MATRIZ TABULEIRO
# 0 = espaço vazio
# 1 = Corpo/calda cobra
# 2 = Cabeça cobra
# 3 = Fruto bom
# 4 = Fruto ruim
# eixos: (y, X)
CELULAS_Y, CELULAS_X = 0, 0
tecla = 'd'
matriz_tabuleiro = []
matriz_cobra = []
contador_pontos = 0

rodando = True
while rodando:
    clock.tick(FPS) 
    tela.fill(preto)

    tela.blit(imagem_fundo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # LOGICAS
        if estado_atual == "MENU":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_iniciar_rect.collidepoint(evento.pos):
                    estado_atual = "MENU_DIFICULDADE"
                if botao_sair_rect.collidepoint(evento.pos):
                    rodando = False

        elif estado_atual == "MENU_DIFICULDADE":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_dificuldade_facil_rect.collidepoint(evento.pos):
                    dificuldade = "facil"
                    CELULAS_Y, CELULAS_X = 12, 12
                    max_pontos = 5
                    vel_cobra = 3
                if botao_dificuldade_media_rect.collidepoint(evento.pos):
                    dificuldade = "media"
                    CELULAS_Y, CELULAS_X = 8, 8
                    max_pontos = 20
                    vel_cobra = 5
                if botao_dificuldade_dificil_rect.collidepoint(evento.pos):
                    dificuldade = "dificil"
                    CELULAS_Y, CELULAS_X = 8, 8
                    max_pontos = 10
                    vel_cobra = 8
                estado_atual = "PREJOGO"

        elif estado_atual == "JOGO":
            if evento.type == pygame.KEYDOWN:
                count_jogadas += 1
                if evento.key == pygame.K_ESCAPE:
                    print('pause')
                    estado_atual = "PAUSE"
                if evento.key == pygame.K_a:
                    print('tecla a')
                    tecla = 'a'
                    angulo = 180
                elif evento.key == pygame.K_w:
                    print('tecla w')
                    tecla = 'w'
                    angulo = 90
                elif evento.key == pygame.K_s:
                    print('tecla s')
                    tecla = 's'
                    angulo = 270
                elif evento.key == pygame.K_d:
                    print('tecla d')
                    tecla = 'd'
                    angulo = 0

        elif estado_atual == "PAUSE":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado_atual = "JOGO"
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_continuar_rect.collidepoint(evento.pos):
                    estado_atual = "JOGO"
                if botao_novamente_rect.collidepoint(evento.pos):
                    estado_atual = "MENU_DIFICULDADE"
                if botao_sair_rect.collidepoint(evento.pos):
                    estado_atual = "MENU"

        elif estado_atual == "GAME_OVER":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_novamente_rect.collidepoint(evento.pos):
                    estado_atual = "MENU_DIFICULDADE"
                if botao_sair_rect.collidepoint(evento.pos):
                    estado_atual = "MENU"
        
        elif estado_atual == "WINNER":
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_novamente_rect.collidepoint(evento.pos):
                    estado_atual = "MENU_DIFICULDADE"
                if botao_sair_rect.collidepoint(evento.pos):
                    estado_atual = "MENU"

    # LOGICA ESTADOS JOGO
    if estado_atual == "MENU":
        titulo_menu = fonte_comic.render("SNAKEEE", True, branco)
        titulo_menu_rect = titulo_menu.get_rect(midtop = (largura // 2, altura // 5))
        tela.blit(titulo_menu, titulo_menu_rect)

        botao_iniciar_texto, botao_iniciar_rect = criar_botao("Iniciar", altura // 2)
        botao_sair_texto, botao_sair_rect = criar_botao("Sair", altura // 2 + 70)

    elif estado_atual == "MENU_DIFICULDADE":
        tela.blit(titulo_menu, titulo_menu_rect)

        botao_dificuldade_facil_texto, botao_dificuldade_facil_rect = criar_botao("Fácil", altura // 2.5 + 30)
        botao_dificuldade_media_texto, botao_dificuldade_media_rect = criar_botao("Média", altura // 2.5 + 100)
        botao_dificuldade_dificil_texto, botao_dificuldade_dificil_rect = criar_botao("Difícil", altura // 2.5 + 170)
    
    elif estado_atual == "PREJOGO":
        count_jogadas = 0
        tecla = 'd'
        angulo = 0
        matriz_tabuleiro.clear()
        matriz_cobra.clear()
        gerar_matriz(CELULAS_X, CELULAS_Y, matriz_tabuleiro)
        gerar_cobra(matriz_tabuleiro, matriz_cobra)

        for i in range(5):
            gerar_fruto(CELULAS_X, CELULAS_Y, matriz_tabuleiro, 3)
            gerar_fruto(CELULAS_X, CELULAS_Y, matriz_tabuleiro, 4)
        for linha in matriz_tabuleiro:
            print(f"{linha}\n")

        ultimo_movimento_tempo = pygame.time.get_ticks() # reinicia o timer
        contador_pontos = 0

        largura_tabuleiro = CELULAS_X * TAMANHO_CELULA + CELULAS_X
        altura_tabuleiro = CELULAS_Y * TAMANHO_CELULA + CELULAS_Y 
        img_fundo_grama = pygame.transform.scale(imagem_grama, (largura_tabuleiro, altura_tabuleiro))
        img_fundo_grama_rect = img_fundo_grama.get_rect()
        img_fundo_grama_rect.center = (largura // 2, altura // 2)

        estado_atual = "JOGO"

    elif estado_atual == "JOGO":
        tempo_agora = pygame.time.get_ticks()

        if (tempo_agora - ultimo_movimento_tempo) > velocidade_cobra(vel_cobra):
            status = movimentar_cobra(tecla, matriz_cobra, matriz_tabuleiro, CELULAS_X, CELULAS_Y)
            ultimo_movimento_tempo = tempo_agora

            if status == "FRUTA_BOA":
                gerar_fruto(CELULAS_X, CELULAS_Y, matriz_tabuleiro, 3)
                som_fruta_boa.play()
                contador_pontos += 1
            elif status == "FRUTA_RUIM":
                gerar_fruto(CELULAS_X, CELULAS_Y, matriz_tabuleiro, 4)
                som_fruta_ruim.play()
                contador_pontos -= 2
            if verificar_vitoria(matriz_tabuleiro, contador_pontos, max_pontos):
                estado_atual = 'WINNER'
            elif status == "GAME_OVER":
                estado_atual = "GAME_OVER"

        contador_pontos_texto = fonte_padrao.render(f'Pontos: {contador_pontos}/{max_pontos}', True, branco)
        contador_pontos_rect = contador_pontos_texto.get_rect(topright = (largura - 50, 15))

        tela.blit(img_fundo_grama, img_fundo_grama_rect)
        desenhar_tabuleiro(CELULAS_Y, CELULAS_X, matriz_tabuleiro)
        tela.blit(contador_pontos_texto, contador_pontos_rect)

    elif estado_atual == "PAUSE":
        tela.blit(img_fundo_grama, img_fundo_grama_rect)
        desenhar_tabuleiro(CELULAS_Y, CELULAS_X, matriz_tabuleiro)
        tela.blit(contador_pontos_texto, contador_pontos_rect)

        faixa_pause_rect = (0, altura // 4 + 50, largura, 400)
        pygame.draw.rect(tela, bege_faixa, faixa_pause_rect)

        texto_pause = fonte_comic.render("PAUSE", True, azul)
        texto_pause_rect = texto_pause.get_rect(center=(largura // 2, altura // 2 - 50))
        tela.blit(texto_pause, texto_pause_rect)

        botao_continuar_texto, botao_continuar_rect = criar_botao("Continuar", altura // 2 + 50)
        botao_novamente_texto, botao_novamente_rect = criar_botao("Tentar Novamente", altura // 2 + 130, 350)
        botao_sair_texto, botao_sair_rect = criar_botao("Sair", altura // 2 + 210)

    elif estado_atual == "GAME_OVER":
        tela.blit(img_fundo_grama, img_fundo_grama_rect)
        tela.blit(contador_pontos_texto, contador_pontos_rect)
        desenhar_tabuleiro(CELULAS_Y, CELULAS_X, matriz_tabuleiro)

        contador_jogadas_texto = fonte_padrao.render(f'Jogadas: {count_jogadas}', True, branco)
        contador_jogadas_rect = contador_jogadas_texto.get_rect(topleft = (50, 15))
        tela.blit(contador_jogadas_texto, contador_jogadas_rect)

        faixa_game_over_rect = (0, altura // 4 + 50, largura, 300)
        pygame.draw.rect(tela, verde_faixa, faixa_game_over_rect)

        texto_game_over = fonte_padrao.render("GAME OVER", True, vermelho)
        texto_game_over_rect = texto_game_over.get_rect(center=(largura // 2, altura // 2 - 50))
        tela.blit(texto_game_over, texto_game_over_rect)

        botao_novamente_texto, botao_novamente_rect = criar_botao("Tentar Novamente", altura // 2 + 50, 350)
        botao_sair_texto, botao_sair_rect = criar_botao("Sair", altura // 2 + 120)
    
    elif estado_atual == 'WINNER':
        tela.blit(img_fundo_grama, img_fundo_grama_rect)
        tela.blit(contador_pontos_texto, contador_pontos_rect)
        desenhar_tabuleiro(CELULAS_Y, CELULAS_X, matriz_tabuleiro)

        contador_jogadas_texto = fonte_padrao.render(f'Jogadas: {count_jogadas}', True, branco)
        contador_jogadas_rect = contador_jogadas_texto.get_rect(topleft = (50, 15))
        tela.blit(contador_jogadas_texto, contador_jogadas_rect)

        faixa_winner_rect = (0, altura // 4 + 50, largura, 300)
        pygame.draw.rect(tela, verde_faixa, faixa_winner_rect)

        texto_winner = fonte_padrao.render("VOÇÊ VENCEU!", True, verde)
        texto_winner_rect = texto_winner.get_rect(center=(largura // 2, altura // 2 - 50))
        tela.blit(texto_winner, texto_winner_rect)

        botao_novamente_texto, botao_novamente_rect = criar_botao("Tentar Novamente", altura // 2 + 50, 350)
        botao_sair_texto, botao_sair_rect = criar_botao("Sair", altura // 2 + 120)

    pygame.display.flip()

pygame.quit()
sys.exit()
