# Relatório: Turtle Draw

O projeto Turtle Draw teve como objetivo desenvolver uma pipeline de visão computacional capaz de transformar uma imagem em trajetórias desenhadas no turtlesim utilizando ROS 2. A proposta envolveu etapas de processamento de imagem, detecção de bordas, extração de coordenadas e conversão dessas coordenadas para o sistema do turtlesim. 

A imagem utilizada foi uma fotografia de um cachorro, fornecida previamente. Para garantir a compreensão detalhada de cada etapa, a pipeline foi desenvolvida do zero, utilizando estritamente NumPy para operações matriciais, OpenCV apenas para carregamento e Matplotlib para visualização, conforme os requisitos técnicos exigidos.

---

## 1. Desenvolvimento da Pipeline

### 1.1. Pré-processamento da Imagem

Inicialmente, a imagem foi carregada e convertida do padrão BGR para RGB. Em seguida, foi realizada a conversão para **escala de cinza (grayscale)**, reduzindo a imagem a um único canal de intensidade. Essa etapa foi fundamental para simplificar o processamento computacional e focar apenas nas variações de luminosidade, que são a base da detecção de bordas.

Para lidar com ruídos e texturas internas que poderiam gerar falsas bordas, testou-se o Filtro de Média e o Filtro Gaussiano:
* **Filtro de Média:** Apresentou boa redução de ruído, mas causou um borramento excessivo das estruturas principais quando o tamanho do *kernel* era aumentado.
* **Filtro Gaussiano (3x3):** Foi a técnica escolhida. Diferente da média simples, o kernel gaussiano atribui maior peso aos pixels centrais da vizinhança. Isso resultou em uma suavização eficiente do ruído sem comprometer a nitidez dos contornos principais do animal.

### 1.2 Detecção de Bordas

A extração de características foi feita através do **Operador de Sobel**, implementado manualmente por meio da convolução da imagem com os kernels horizontais e verticais. O Sobel foi escolhido por oferecer um excelente custo-benefício entre simplicidade algorítmica e robustez na identificação de gradientes de intensidade.

Após calcular a magnitude do gradiente combinando os eixos X e Y, aplicou-se a **limiarização (*thresholding*)** para binarizar a imagem. A escolha do valor de threshold exigiu análise:

* **Valores baixos (ex: 50):** Preservavam ruídos e detalhes indesejados da textura do pelo.
* **Valores altos (ex: 100):** Rompiam a continuidade do contorno principal.
* **Valor escolhido (75):** Apresentou o melhor equilíbrio. Decidiu-se manter propositalmente alguns detalhes faciais internos (como olhos e focinho), pois eles enriquecem o resultado visual e tornam o desenho final mais reconhecível.

### 1.3 Extração e Armazenamento dos Pontos

Com a imagem binarizada, os pixels de borda (valor 255) foram extraídos como coordenadas (x, y). Como a extração bruta gerava um volume de dados excessivamente denso, aplicou-se uma etapa de **amostragem** (coletando 1 ponto a cada 5 originais). Isso reduziu drasticamente a complexidade da trajetória sem deformar a silhueta. Os pontos finais foram salvos em um arquivo CSV para facilitar a leitura pelo nó de controle.

### 1.4 Integração com ROS 2 e Turtlesim
O nó desenvolvido (`turtle_drawer`) atua como cliente dos serviços `/turtle1/teleport_absolute` e `/turtle1/set_pen`. A integração exigiu três transformações matemáticas fundamentais nas coordenadas extraídas do CSV:

1. **Escala e Proporção:** A imagem original (720x1280) foi redimensionada para caber no limite padrão do turtlesim (~11x11), fixando a largura em 10 e calculando a altura proporcionalmente para evitar distorções.
2. **Centralização:** Foram aplicados *offsets* nos eixos X e Y para garantir que o desenho ficasse centralizado no canvas.
3. **Inversão do Eixo Y:** Como matrizes de imagem têm a origem (0,0) no canto superior esquerdo e o turtlesim no canto inferior esquerdo, o eixo Y precisou ser invertido matematicamente.

---

## 2. Dificuldades Encontradas e Soluções

A primeira grande dificuldade envolveu a Visão Computacional, especificamente calibrar o trade-off entre remoção de ruído e preservação de bordas contínuas, o que foi solucionado combinando o Filtro Gaussiano com um threshold empírico de 75. A diferença de sistemas de coordenadas (a necessidade de inverter o eixo Y) também exigiu atenção durante a transposição dos dados.

No entanto, o maior desafio técnico ocorreu no controle robótico. O comportamento padrão do turtlesim é desenhar linhas contínuas durante o teletransporte. Como os pontos extraídos da imagem não formam necessariamente uma trajetória sequencial ininterrupta, isso gerava riscos indesejados cruzando a tela inteira. 

A solução arquitetural encontrada foi desenvolver uma abordagem de "pontilhismo". A lógica implementada utiliza o serviço `SetPen` para desligar a caneta antes de mover a tartaruga para a nova coordenada. Uma vez posicionada, a caneta é reativada e um micro-movimento (+0.01 nos eixos) é comandado via `TeleportAbsolute`, efetivamente "carimbando" o ponto na tela sem deixar rastros indesejados entre coordenadas distantes.