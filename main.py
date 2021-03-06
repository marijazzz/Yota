import socket
import numpy as np
from _thread import * # упрощает работу с потоками и позволяет программировать запуск нескольких операций одновременно
import sys

# Подключение классов, описанных в других файлах
from Cards import *
from Pack import *
from Player import *
from Desk import *
from Errors import *


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) # создание сокета

try:
    sock.bind(('', 48666)) # первый элемент - хост, второй - порт
except socket.error as er:
    print(str(er))

sock.listen() #не установлено кол-во пользователей, способных подключаться к данному порту (?)
conn, addr = sock.accept() # принимаем подключение, conn - новый сокет, addr - адрес клиента

while True: # получение данных от клиента
    data = conn.recv(1024) # "порции данных"
    if not data:
        break
    conn.send(data.upper())

### обработка данных

conn.close() # закрытие соединения