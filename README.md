# Turtle Draw - Pipeline de Visão Computacional com ROS 2

Projeto desenvolvido para transformar uma imagem em trajetórias desenhadas no turtlesim utilizando técnicas de visão computacional e ROS 2.

A pipeline realiza:

- Carregamento da imagem
- Pré-processamento
- Detecção de bordas
- Extração de pontos
- Geração de trajetórias para o turtlesim

A imagem utilizada no projeto é uma fotografia de um cachorro fornecida previamente para a atividade.

---

## 🎥 Vídeo de Demonstração

[Vídeo de Demonstração](https://drive.google.com/file/d/1fNkmfGqEcH8nqpywwZXsP5OaCd49m4Nm/view?usp=sharing)

---

## 📁 Estrutura do Projeto


```text
turtle-draw/
├── ros2_ws/
│   └── src/
|       └── turtle_draw/
│           ├── package.xml
│           ├── setup.py
│           ├── setup.cfg
│           ├── resource/
│           │   └── turtle_draw
│           └── turtle_draw/
│               ├── __init__.py
│               └── draw_turtle.py
├── assets/
│   └── dog.png
├── edge-detection.ipynb
├── points.csv
├── relatorio.md
├── requirements.txt
└── README.md

```

---

## 📄 Arquivos Principais

### `edge-detection.ipynb`

Notebook localizado na raiz contendo toda a pipeline de visão computacional:

* Conversão RGB → Grayscale
* Filtros de suavização
* Detecção de bordas com Sobel
* Limiarização
* Extração de pontos e amostragem
* Geração do arquivo CSV


### `ros2_ws/src/turtle_draw/turtle_draw/draw_turtle.py`

Nó ROS 2 responsável por:

* Ler os pontos do CSV
* Converter coordenadas da imagem
* Normalizar escala e centralizar o desenho
* Controlar o turtlesim e desenhar os pontos extraídos utilizando os serviços `/turtle1/teleport_absolute` e `/turtle1/set_pen`

### Outros Arquivos

* **`points.csv`**: Arquivo gerado pelo notebook contendo as coordenadas prontas para o turtlesim.
* **`relatório.md`**: Relatório técnico detalhando decisões de implementação, justificativas e dificuldades encontradas.

---

## ⚙️ Dependências

### Python

Recomenda-se utilizar um ambiente virtual (`venv`).

```bash
# Criar e ativar ambiente virtual (Linux)
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

```

### ROS 2

O projeto utiliza o **ROS 2 Jazzy** e o pacote `turtlesim`.

```bash
sudo apt install ros-jazzy-turtlesim

```

---

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/stefannevictoria/turtle-draw.git
cd turtle-draw

```

### 2. Buildar o pacote ROS 2

Estando na pasta `ros2_ws`, execute o build:

```bash
cd ros2_ws
colcon build

```

### 3. Fazer source do workspace

```bash
source install/setup.bash

```

### 4. Iniciar o turtlesim

Em um terminal separado (lembre-se de realizar o source no novo terminal), inicie o simulador:

```bash
ros2 run turtlesim turtlesim_node

```

### 5. Executar o nó de desenho

Volte ao terminal onde você buildou o projeto e execute o nó:

```bash
ros2 run turtle_draw draw_turtle

```

O turtlesim começará a desenhar os pontos extraídos da imagem imediatamente.

---

## 📊 Resultados

A pipeline foi capaz de:

* Detectar os contornos principais do cachorro
* Preservar detalhes faciais relevantes
* Reduzir ruídos da imagem
* Gerar uma representação desenhável no turtlesim

![Imagem turtlesim](https://res.cloudinary.com/dwewomj84/image/upload/v1779495897/d851e310-3bf0-4cca-881f-d9ac308220e8.png)
