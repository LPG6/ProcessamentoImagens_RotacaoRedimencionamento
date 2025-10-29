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

## 📂 Estrutura do Projeto

Este projeto segue uma estrutura modular para facilitar a manutenção e escalabilidade:

```
seu-repositorio/
│
├── image_processor/
│   ├── __init__.py        # Torna a pasta um "pacote" Python
│   ├── processing.py      # Contém toda a lógica de processamento de imagem (OpenCV)
│   └── ui.py              # Contém toda a lógica da interface do usuário (Gradio)
│
├── main.py                # Ponto de entrada principal para iniciar a aplicação
├── requirements.txt       # Lista todas as bibliotecas necessárias para o projeto
└── README.md              # Esta documentação
```

## 🚀 Como Executar

Você pode executar este projeto de duas maneiras: localmente em sua máquina ou diretamente no Google Colab.

### A. Executando Localmente

**Pré-requisitos:**
*   [Git](https://git-scm.com/) instalado.
*   [Python 3.x](https://www.python.org/downloads/) instalado.

**Passos:**

1.  **Clone o repositório:**
    Abra seu terminal e clone este repositório do GitHub.
    ```bash
    git clone https://github.com/LPG6/ProcessamentoImagens_RotacaoRedimencionamento.git
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd ProcessamentoImagens_RotacaoRedimencionamento
    ```

3.  **Instale as dependências:**
    O arquivo `requirements.txt` contém todas as bibliotecas necessárias. Instale-as com um único comando:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    Inicie o script principal.
    ```bash
    python main.py
    ```

5.  **Acesse a interface:**
    O terminal exibirá um URL. Abra este link no seu navegador para usar a ferramenta.

### B. Executando no Google Colab

Esta é a maneira mais fácil de testar o projeto sem precisar instalar nada em sua máquina.

1.  **Abra um novo notebook no Google Colab.**

2.  **Célula 1: Clone o repositório**
    Copie e cole o seguinte comando na primeira célula.
    ```python
    # Clona o seu projeto para o ambiente do Colab
    !git clone https://github.com/LPG6/ProcessamentoImagens_RotacaoRedimencionamento.git
    ```

3.  **Célula 2: Instale as dependências**
    Navegue para a pasta do projeto e instale as bibliotecas a partir do `requirements.txt`.
    ```python
    # Entra na pasta do projeto
    %cd ProcessamentoImagens_RotacaoRedimencionamento

    # Instala todas as bibliotecas necessárias
    !pip install -r requirements.txt
    ```

4.  **Célula 3: Execute a aplicação**
    Inicie o script principal para lançar a interface do Gradio.
    ```python
    # Executa a aplicação
    !python main.py
    ```
    Ao executar esta célula, o Colab fornecerá um **URL público** (`...gradio.live`). Clique nesse link para abrir e usar a ferramenta.

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

## 🧪 Casos de Teste e Demonstração

Esta seção demonstra o comportamento da aplicação em diferentes cenários, destacando suas forças e limitações. Para replicar estes testes, você pode salvar as imagens de exemplo em uma pasta e utilizá-las na ferramenta.

| Cenário de Teste | Imagem de Exemplo | Funcionalidades a Utilizar | Resultado Esperado e Análise |
| :--- | :--- | :--- | :--- |
