# 🖼️ Processador de Imagens com Rotação e Recorte Automático

Este é um projeto em Python que utiliza as bibliotecas **OpenCV** para processamento de imagem e **Gradio** para criar uma interface web interativa. A ferramenta permite que usuários façam upload de imagens e apliquem diversas transformações, como rotação, redimensionamento e recorte, tanto de forma manual quanto automática.

A aplicação é ideal para tarefas rápidas de edição, como endireitar fotos tortas, recortar objetos de seus fundos ou padronizar o tamanho de um lote de imagens.

## ✨ Funcionalidades Principais

*   **Interface Web Interativa:** Graças ao Gradio, não é necessário ter conhecimento de programação para usar a ferramenta. Basta executar o script e abrir o link no navegador.
*   **Rotação Manual e Automática:**
    *   **Manual:** Um slider permite girar a imagem em qualquer ângulo de -180° a 180°.
    *   **Automática:** Utiliza a Transformada de Hough para detectar as linhas predominantes na imagem e corrigir sua inclinação automaticamente. Possui uma "zona morta" para evitar a rotação desnecessária de imagens que já estão retas.
*   **Redimensionamento com Preservação de Proporção:** Defina a nova largura ou altura em pixels e escolha se deseja manter a proporção original da imagem para evitar distorções.
*   **Múltiplos Métodos de Recorte (ROI):**
    *   **Contorno Retangular:** Detecta o objeto principal na imagem (baseado no contraste com o fundo) e o recorta em uma caixa delimitadora. Ideal para produtos em fundos simples.
    *   **Remoção de Fundo:** Vai um passo além do recorte retangular, criando uma máscara para remover completamente o fundo e torná-lo transparente (requer salvamento em PNG).
*   **Pré-visualização em Tempo Real:** Veja o resultado das suas transformações na interface antes de fazer o download.
*   **Exportação em Múltiplos Formatos:** Baixe a imagem processada nos formatos **PNG** ou **JPG**.

## 🚀 Como Executar o Projeto

### Pré-requisitos
*   Python 3.x instalado.

### 1. Instalação das Dependências
Abra seu terminal ou prompt de comando e instale as bibliotecas necessárias com o seguinte comando:

```bash
pip install gradio opencv-python-headless pillow numpy
```

### 2. Executando o Script
1.  Salve o código completo em um arquivo chamado `processador_de_imagens.py`.
2.  Navegue até a pasta onde você salvou o arquivo pelo terminal.
3.  Execute o script com o comando:

    ```bash
    python processador_de_imagens.py
    ```4.  O terminal exibirá mensagens de inicialização e, por fim, um URL local (geralmente `http://127.0.0.1:7860`) e um URL público (share link). Abra qualquer um desses links no seu navegador.

## 🔧 Como Utilizar a Ferramenta

A interface é dividida em um painel de controle à esquerda e uma área de pré-visualização à direita.

1.  **Faça o Upload da Imagem:** Arraste e solte uma imagem ou clique na caixa "Imagem Original" para selecionar um arquivo.
2.  **Ajuste a Rotação (Seção 1):**
    *   **Manual:** Deixe a opção "Manual" selecionada e mova o slider "Ângulo".
    *   **Automática:** Selecione a opção "Automática" para que o script endireite a imagem.
3.  **Escolha o Método de Corte (Seção 2):**
    *   **Nenhum:** Mantém a imagem sem recorte.
    *   **Contorno Retangular:** Ideal para objetos com fundo de alto contraste. Ele recortará um retângulo ao redor do objeto.
    *   **Remoção de Fundo:** Remove o fundo, deixando-o transparente. **Atenção:** Isso forçará o formato de saída para PNG.
4.  **Defina o Redimensionamento (Seção 3):**
    *   Insira a nova largura ou altura desejada em pixels.
    *   Marque/desmarque a caixa "Manter Proporção" conforme sua necessidade.
5.  **Selecione o Formato de Saída (Seção 4):**
    *   Escolha entre PNG (suporta transparência) e JPG.
6.  **Aplique e Baixe:**
    *   Clique no botão **"Aplicar Transformações"**.
    *   A imagem processada aparecerá na área de pré-visualização à direita.
    *   Clique em **"Baixar Imagem Processada"** para salvar o arquivo final.

## ⚙️ Detalhes Técnicos e Depuração

*   **Rotação Automática:** O algoritmo utiliza `cv2.HoughLinesP` para detectar segmentos de linha, calcula a mediana de seus ângulos e aplica uma rotação corretiva.
*   **Detecção de Contornos:** Para os métodos de corte, a imagem é convertida para escala de cinza e binarizada usando o método de Otsu (`cv2.THRESH_OTSU`) para separar o objeto do fundo. Em seguida, `cv2.findContours` localiza a forma do objeto principal (o maior contorno por área).
*   **Depuração:** Durante o processo de remoção de fundo, o script gera automaticamente um arquivo chamado `debug_mascara_gerada.png` na mesma pasta. Este arquivo mostra a silhueta em preto e branco que foi usada para criar a transparência, sendo muito útil para diagnosticar por que um recorte pode não ter saído como o esperado.
