import json
from Player import Player
from Session import GameSession
from Desk import *

class GameServer():
    """Класс описывает ход игры"""
    PLAYERS_NEED_FOR_GAME = 4 # количество человек в одной игре

    def __init__(self, sendMessage):
        self.sendMessage = sendMessage # сообщение от клиента
        self.waiting_for_game_players = [] # очередь из игроков, ожидающих начала игры
        self.game_sessions = [] # данная игровая сессия

    def onMessage(self, client_id: str, message: dict):
        """Отклик сервера на различные сообщения"""
        if message['type'] == 'HelloIWannaPlay': # сообщение о начале игры
            client = Player(client_id=client_id, name=message['user_name'])
            self.waiting_for_game_players.append(client) # добавление данного игрока в очередь
            if len(self.waiting_for_game_players) >= self.PLAYERS_NEED_FOR_GAME:
                # для создания игровой сессии нужно взять первых PLAYERS_NEED_FOR_GAME игроков из очереди
                players_to_play = self.waiting_for_game_players[:self.PLAYERS_NEED_FOR_GAME]
                self.waiting_for_game_players = self.waiting_for_game_players[self.PLAYERS_NEED_FOR_GAME:] # обновление списка из оставшихся игроков

                game_session = GameSession(players=players_to_play, sendMessage=self.sendMessage) # начало игровой сессии
                self.game_sessions.append(game_session)

                game_session.startGame()
          

        elif message['type'] in ['IPutCard']: # сообщение о том, что игрок положил карту на стол
            for game_session in self.game_sessions:
                if game_session.hasClient(client_id):
                    game_session.onMessage(client_id, message)
            # TODO А что будет если сессии нет никакой?