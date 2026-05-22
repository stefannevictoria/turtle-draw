import rclpy
from rclpy.node import Node

from turtlesim.srv import TeleportAbsolute
from turtlesim.srv import SetPen

import csv
import time


class TurtleDrawer(Node):

    def __init__(self):

        super().__init__('turtle_drawer')

        # Serviço teleport
        self.teleport_client = self.create_client(
            TeleportAbsolute,
            '/turtle1/teleport_absolute'
        )

        # Serviço caneta
        self.pen_client = self.create_client(
            SetPen,
            '/turtle1/set_pen'
        )

        while not self.teleport_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando teleport...')

        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando set_pen...')

        self.draw_image()


    def set_pen(self, off):

        request = SetPen.Request()

        request.r = 255
        request.g = 255
        request.b = 255

        request.width = 2

        request.off = off

        future = self.pen_client.call_async(request)

        rclpy.spin_until_future_complete(self, future)


    def teleport_turtle(self, x, y):

        request = TeleportAbsolute.Request()

        request.x = float(x)
        request.y = float(y)
        request.theta = 0.0

        future = self.teleport_client.call_async(request)

        rclpy.spin_until_future_complete(self, future)


    def draw_image(self):

        points = []

        with open('points.csv', 'r') as file:

            reader = csv.reader(file)

            next(reader)

            for row in reader:

                x = int(row[0])
                y = int(row[1])

                points.append((x, y))


        image_width = 1280
        image_height = 720


        for point in points:

            x_img, y_img = point

            # Normaliza coordenadas da imagem para o espaço do turtlesim
            scale = 10
            turtle_x = (x_img / image_width) * scale
            turtle_y = scale - ((y_img / image_height) * (scale * image_height / image_width))

            # Desliga caneta
            self.set_pen(True)

            # Teleporta
            self.teleport_turtle(turtle_x, turtle_y)

            # Liga caneta
            self.set_pen(False)

            # Mini movimento pra criar ponto
            self.teleport_turtle(
                turtle_x + 0.01,
                turtle_y + 0.01
            )

            time.sleep(0.001)


def main(args=None):

    rclpy.init(args=args)

    TurtleDrawer()

    rclpy.shutdown()


if __name__ == '__main__':
    main()