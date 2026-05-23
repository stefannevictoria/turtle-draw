import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/inteli/Documentos/codigos/2026/M06-Inteli2026/turtle-draw/ros2_ws/install/turtle_draw'
