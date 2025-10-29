import gradio as gr
from PIL import Image
import cv2

# Importa as funções de processamento do outro arquivo
from .processing import (
    rotacionar_imagem,
    rotacao_automatica,
    corte_automatico,
    corte_com_remocao_fundo,
    redimensionar_imagem_alta_qualidade
)

# --- FUNÇÕES HANDLER ---

def processar_imagem(imagem_original, tipo_rotacao, angulo_rotacao, metodo_corte, nova_largura, nova_altura, manter_proporcao, formato_saida):
    if imagem_original is None:
        raise gr.Error("Por favor, faça o upload de uma imagem primeiro!")

    imagem_processada = cv2.cvtColor(imagem_original, cv2.COLOR_RGB2BGR)

    if tipo_rotacao == 'Automática':
        imagem_processada = rotacao_automatica(imagem_processada)
    else:
        imagem_processada = rotacionar_imagem(imagem_processada, angulo_rotacao)
    
    if metodo_corte == 'Contorno Retangular (Objetos)':
        imagem_processada = corte_automatico(imagem_processada)
    elif metodo_corte == 'Remoção de Fundo (Objetos)':
        imagem_processada = corte_com_remocao_fundo(imagem_processada)
        
    imagem_processada = redimensionar_imagem_alta_qualidade(imagem_processada, nova_largura, nova_altura, manter_proporcao)

    if len(imagem_processada.shape) == 3 and imagem_processada.shape[2] == 4:
        imagem_final = cv2.cvtColor(imagem_processada, cv2.COLOR_BGRA2RGBA)
        img_pil = Image.fromarray(imagem_final, 'RGBA')
    else:
        imagem_final = cv2.cvtColor(imagem_processada, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(imagem_final, 'RGB')

    caminho_arquivo = f"imagem_processada.{formato_saida.lower()}"
    if formato_saida == 'PNG':
        img_pil.save(caminho_arquivo, format='PNG')
    elif formato_saida == 'JPG':
        if img_pil.mode == 'RGBA':
            img_pil = img_pil.convert('RGB')
        img_pil.save(caminho_arquivo, format='JPEG', quality=95)

    return imagem_final, caminho_arquivo

def atualizar_controles_rotacao(tipo_rotacao):
    return gr.update(interactive=(tipo_rotacao == 'Manual'), value=0)

def atualizar_estado_altura(manter_proporcao_ativo):
    return gr.update(interactive=not manter_proporcao_ativo, value=0 if manter_proporcao_ativo else None)

def atualizar_formato_saida(metodo_corte):
    if metodo_corte == 'Remoção de Fundo (Objetos)':
        return gr.update(value='PNG', interactive=False)
    else:
        return gr.update(interactive=True)

# --- DEFINIÇÃO DA INTERFACE ---

def criar_interface():
    custom_css = """#altura_input_box input:disabled, #formato_output_box input:disabled { background-color: #e9ecef; cursor: not-allowed; }"""

    with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
        gr.Markdown("# Sistema de Análise de Padrões - Módulo de Rotação e Redimensionamento")
        with gr.Row():
            with gr.Column(scale=1):
                imagem_input = gr.Image(label="Imagem Original", type="numpy")
                gr.Markdown("### 1. Rotação")
                tipo_rotacao_input = gr.Radio(['Manual', 'Automática'], value='Manual', label="Tipo")
                angulo_input = gr.Slider(minimum=-180, maximum=180, value=0, step=1, label="Ângulo", interactive=True)
                gr.Markdown("### 2. Corte Automático")
                metodo_corte_input = gr.Radio(['Nenhum', 'Contorno Retangular (Objetos)', 'Remoção de Fundo (Objetos)'], value='Nenhum', label="Método")
                gr.Markdown("### 3. Redimensionamento")
                proporcao_input = gr.Checkbox(label="Manter Proporção", value=True)
                with gr.Row():
                    largura_input = gr.Number(label="Largura (px)", value=0)
                    altura_input = gr.Number(label="Altura (px)", value=0, interactive=False, elem_id="altura_input_box")
                gr.Markdown("### 4. Formato de Saída")
                formato_output = gr.Radio(['PNG', 'JPG'], value='PNG', label="Formato", elem_id="formato_output_box")
                submit_btn = gr.Button("Aplicar Transformações", variant="primary")
            with gr.Column(scale=2):
                imagem_output = gr.Image(label="Imagem Processada", type="numpy")
                download_output = gr.File(label="Baixar Imagem")

        tipo_rotacao_input.change(fn=atualizar_controles_rotacao, inputs=tipo_rotacao_input, outputs=angulo_input)
        proporcao_input.change(fn=atualizar_estado_altura, inputs=proporcao_input, outputs=altura_input)
        metodo_corte_input.change(fn=atualizar_formato_saida, inputs=metodo_corte_input, outputs=formato_output)
        submit_btn.click(fn=processar_imagem, inputs=[imagem_input, tipo_rotacao_input, angulo_input, metodo_corte_input, largura_input, altura_input, proporcao_input, formato_output], outputs=[imagem_output, download_output])
    
    return demo
