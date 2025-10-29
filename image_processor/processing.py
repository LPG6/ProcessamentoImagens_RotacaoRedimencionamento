import cv2
import numpy as np
import math

def rotacionar_imagem(imagem, angulo):
    """Rotaciona uma imagem. Um ângulo positivo resulta em rotação no sentido horário."""
    if imagem is None or angulo == 0:
        return imagem
    (h, w) = imagem.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, -angulo, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nova_w = int((h * sin) + (w * cos))
    nova_h = int((h * cos) + (w * sin))
    M[0, 2] += (nova_w / 2) - centro[0]
    M[1, 2] += (nova_h / 2) - centro[1]
    border_value = (255, 255, 255, 0) if len(imagem.shape) > 2 and imagem.shape[2] == 4 else (255, 255, 255)
    return cv2.warpAffine(imagem, M, (nova_w, nova_h), borderValue=border_value)

def rotacao_automatica(imagem):
    """Detecta a inclinação de uma imagem e a corrige."""
    print("\n--- [DEBUG ROTAÇÃO] INICIANDO ROTAÇÃO AUTOMÁTICA ---")
    if imagem is None: return imagem

    img_para_analise = imagem if len(imagem.shape) == 2 or imagem.shape[2] == 3 else cv2.cvtColor(imagem, cv2.COLOR_BGRA2BGR)
    cinza = cv2.cvtColor(img_para_analise, cv2.COLOR_BGR2GRAY)
    cinza = cv2.GaussianBlur(cinza, (5, 5), 0)
    bordas = cv2.Canny(cinza, 50, 150, apertureSize=3)
    
    linhas = cv2.HoughLinesP(bordas, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    if linhas is None: return imagem
        
    angulos = [math.degrees(math.atan2(l[0][3] - l[0][1], l[0][2] - l[0][0])) for l in linhas]
    angulo_mediano = np.median(angulos)
    print(f"[DEBUG ROTAÇÃO] Ângulo mediano calculado: {angulo_mediano:.2f} graus.")

    if abs(angulo_mediano) < 1.0:
        print("[DEBUG ROTAÇÃO] Ângulo dentro da 'zona morta'. Nenhuma rotação aplicada.")
        return imagem
    else:
        print(f"[DEBUG ROTAÇÃO] Aplicando rotação de {-angulo_mediano:.2f} graus.")
        return rotacionar_imagem(imagem, -angulo_mediano)

def corte_automatico(imagem):
    """Corta a imagem criando um retângulo delimitador ao redor do maior objeto."""
    print("\n--- [DEBUG CORTE RETANGULAR] INICIANDO CORTE ---")
    h_orig, w_orig = imagem.shape[:2]
    img_para_analise = imagem if len(imagem.shape) == 2 or imagem.shape[2] == 3 else cv2.cvtColor(imagem, cv2.COLOR_BGRA2BGR)
    cinza = cv2.cvtColor(img_para_analise, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contornos, _ = cv2.findContours(cv2.copyMakeBorder(thresh, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=0), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos: return imagem

    maior_contorno = max(contornos, key=cv2.contourArea)
    x_pad, y_pad, w_pad, h_pad = cv2.boundingRect(maior_contorno)
    x, y = max(0, x_pad - 1), max(0, y_pad - 1)
    w, h = min(w_orig - x, w_pad), min(h_orig - y, h_pad)

    if (w * h) > 0.98 * (w_orig * h_orig): return imagem
    return imagem[y:y+h, x:x+w]

def corte_com_remocao_fundo(imagem):
    """Remove o fundo de uma imagem usando a detecção do maior contorno."""
    print("\n--- [DEBUG REMOÇÃO DE FUNDO] INICIANDO ---")
    img_para_analise = imagem if len(imagem.shape) == 2 or imagem.shape[2] == 3 else cv2.cvtColor(imagem, cv2.COLOR_BGRA2BGR)
    imagem_bgra = cv2.cvtColor(img_para_analise, cv2.COLOR_BGR2BGRA)
    cinza = cv2.cvtColor(img_para_analise, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(cinza, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos: return imagem

    maior_contorno = max(contornos, key=cv2.contourArea)
    mascara = np.zeros(img_para_analise.shape[:2], dtype=np.uint8)
    cv2.drawContours(mascara, [maior_contorno], -1, (255), thickness=cv2.FILLED)
    
    cv2.imwrite("debug_mascara_gerada.png", mascara)
    print("[DEBUG REMOÇÃO DE FUNDO] MÁSCARA SALVA: 'debug_mascara_gerada.png'.")
    
    imagem_bgra[:, :, 3] = mascara
    x, y, w, h = cv2.boundingRect(maior_contorno)
    return imagem_bgra[y:y+h, x:x+w]

def redimensionar_imagem_alta_qualidade(imagem, nova_largura, nova_altura, manter_proporcao):
    if imagem is None: return None
    altura_original, largura_original = imagem.shape[:2]
    nova_largura = int(nova_largura) if nova_largura else 0
    nova_altura = int(nova_altura) if nova_altura else 0
    if nova_largura == 0 and nova_altura == 0: return imagem
    
    if manter_proporcao:
        if nova_largura > 0: nova_altura = int(altura_original * (nova_largura / largura_original))
        elif nova_altura > 0: nova_largura = int(largura_original * (nova_altura / altura_original))
    else:
        if nova_largura == 0: nova_largura = largura_original
        if nova_altura == 0: nova_altura = altura_original
            
    interpolacao = cv2.INTER_AREA if nova_largura * nova_altura < largura_original * altura_original else cv2.INTER_CUBIC
    return cv2.resize(imagem, (nova_largura, nova_altura), interpolation=interpolacao)
