# функции обработчики
import uuid
#uuid - уникальный идентификатор
from .Game import *
#Сообщения - словарь: ключ - тип, значение - смысловая нагрузка

def onHello(uuid): # сообщение о подключении к игре
    pass

print(uuid.uuid4()) #проверка - генерация уникального кода

def gameStartedMessage(uuid, hand, desk): # сюда нужно послать пакет данных
    pass

def yourTurnMessage(uuid): # сообщение, посылаемое клиенту о начале хода (разрешение на выбор карт)
    pass

def onClientTurn(uuid, card, position): # сообщение на сервер, проверка того, можно ли сюда положить нужную карту и т.д. + сюда нужно про функции ответа подумать
    pass

# https://websockets.readthedocs.io/en/stable/
import asyncio
#import websockets
import json

async def echo(websocket, path):

     async for message in websocket:
         #game_server.onMessage(json.loads(message))
         await websocket.send(message)

def sendMessage(client_id: str, message: dict):
    pass
