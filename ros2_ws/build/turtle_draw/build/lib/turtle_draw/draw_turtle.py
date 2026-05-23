import os

import rclpy
from rclpy.node import Node

from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen

import csv
import time


# Classe principal do nó ROS2
class TurtleDrawer(Node):

    def __init__(self):

        # Inicializa o nó ROS2
        super().__init__('turtle_drawer')

        # Cliente responsável por teleportar a tartaruga
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

        # Cliente responsável por controlar a caneta
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')

        # Espera os serviços ficarem disponíveis
        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando teleport...')

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando set_pen...')

        # Inicia desenho
        self.draw_image()


    # Liga ou desliga a caneta
    def set_pen(self, off):

        request = SetPen.Request()

        # Cor da caneta (branco)
        request.r = 255
        request.g = 255
        request.b = 255

        # Espessura da linha
        request.width = 2

        # True = desligada
        # False = ligada
        request.off = off

        future = self.pen_client.call_async(request)

        rclpy.spin_until_future_complete(self, future)


    # Teleporta tartaruga para coordenada específica
    def teleport_turtle(self, x, y):

        request = TeleportAbsolute.Request()

        request.x = float(x)
        request.y = float(y)

        # Orientação da tartaruga
        request.theta = 0.0

        future = self.teleport_client.call_async(request)

        rclpy.spin_until_future_complete(self, future)


    # Função principal de desenho
    def draw_image(self):

        points = []

        # Ler pontos salvos no CSV

        REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..', '..'))
        csv_path = os.path.join(REPO_ROOT, 'points.csv')

        with open(csv_path, 'r') as file:

            reader = csv.reader(file)

            # Ignora cabeçalho
            next(reader)

            # Salva coordenadas em lista
            for row in reader:

                x = int(row[0])
                y = int(row[1])

                points.append((x, y))


        # Dimensões originais da imagem
        image_width = 1280
        image_height = 720


        # Percorre todos os pontos
        for point in points:

            x_img, y_img = point


            # Conversão imagem -> turtlesim

            # Largura do desenho no turtlesim
            drawing_width = 10

            # Mantém proporção da imagem
            drawing_height = (image_height / image_width) * drawing_width

            # Centraliza desenho na tela
            offset_x = (11 - drawing_width) / 2
            offset_y = (11 - drawing_height) / 2


            # Converte coordenada X
            turtle_x = ((x_img / image_width) * drawing_width) + offset_x


            # Converte coordenada Y e inverte eixo vertical
            turtle_y = drawing_height - ((y_img / image_height) * drawing_height)
            turtle_y += offset_y


            # Desenho do ponto

            self.set_pen(True) # Desliga caneta
            self.teleport_turtle(turtle_x, turtle_y) # Teleporta sem desenhar linha
            self.set_pen(False) # Liga caneta

            # Pequeno movimento para criar ponto
            self.teleport_turtle(turtle_x + 0.01, turtle_y + 0.01)

            # Pequena pausa
            time.sleep(0.001)


# Função principal
def main(args=None):

    rclpy.init(args=args) # Inicializa ROS2
    TurtleDrawer() # Cria nó e inicia desenho
    rclpy.shutdown() # Finaliza ROS2


# Executa programa
if __name__ == '__main__':
    main()