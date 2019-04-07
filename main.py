import socket
import numpy as np
from _thread import * # упрощает работу с потоками и позволяет программировать запуск нескольких операций одновременно

# Подключение классов, описанных в других файлах
from Card import Cards
from Card import Joker
from Card import Pack
from Card import Hand
from Card import Line
from Card import Player
from Errors import MyException


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