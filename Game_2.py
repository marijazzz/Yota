import time
import socket
from Player import Player
from Session import GameSession


REMOTE_SERVER = "www.google.com"


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        socket.create_connection((host, 80), 2)
        return True
    except socket.error:
        pass
    return False


class GameServer:
    PLAYERS_NEED_FOR_GAME = 4  # количество человек в одной игре

    def __init__(self, send_message):
        self.send_message = send_message  # сообщение от клиента
        self.waiting_for_game_players = []  # очередь из игроков, ожидающих начала игры
        self.game_sessions = []  # данная игровая сессия

    def on_message(self, client_id: str, message: dict):
        """
        Отклик сервера на различные сообщения
        :param client_id:
        :param message:
        :return:
        """
        # если игрок нажал "хочу играть"
        if message['type'] == 'HelloIWannaPlay':
            # проверяем наличие интернет-соединения
            if is_connected(REMOTE_SERVER):
                # если есть, то добавляем в очередь игры
                client = Player(client_id=client_id, name=message['user_name'])
                self.waiting_for_game_players.append(client)  # добавление данного игрока в очередь
            # если нет, запускаем игру с ботами
            else:
                """
                Bots
                """
                pass
        # если игрок нажал "хочу играть один" и в сессии он один
        elif (message['type'] == 'PlayAlone') and (self.waiting_for_game_players == 1):
            """
            Bots
            """
            pass

        # если сообщение о том, что игрок положил карту на стол
        elif message['type'] in ['IPutCard']:
            for game_session in self.game_sessions:
                if game_session.has_client(client_id):
                    game_session.on_message(client_id, message)

        # окончание игры
        elif message['type'] == ['endTurn']:
            for game_session in self.game_sessions:
                if game_session.has_client(client_id):
                    game_session.on_message(client_id, message)

        # пропуск хода
        elif message['type'] == ['endTurnAndRewindHand']:
            for game_session in self.game_sessions:
                if game_session.has_client(client_id):
                    game_session.on_message(client_id, message)

        # выход из игры
        elif message['type'] == ['disconnection']:
            for game_session in self.game_sessions:
                if game_session.has_client(client_id):
                    game_session.on_message(client_id, message)

    def search_game(self):
        """
        Поиск игроков
        """
        # если игроков меньше, чем PLAYERS_NEED_FOR_GAME
        if len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
            # то пока их не станет PLAYERS_NEED_FOR_GAME
            while len(self.waiting_for_game_players) != self.PLAYERS_NEED_FOR_GAME:
                # обнуляем таймер
                timer = 0
                # запоминаем количество игроков при запуске таймера
                current_found = self.waiting_for_game_players
                # запускаем минуту ожидания
                while timer <= 60:
                    # каждую секунду проверяем, изменилось ли количество игроков
                    if len(self.waiting_for_game_players) == current_found:
                        # если их столько же, итерируем ещё секунду
                        time.sleep(1)
                        timer += 1
                    # если изменилось, но все ещё не 4, то обнуляем счётчик и снова ждём
                    else:
                        current_found = len(self.waiting_for_game_players)
                        timer = 0

                # если за 60 секунд никого не нашёл, добавляем на пустые места ботов
                if timer == 60:
                    """
                    Bots
                    """
                    pass
        # если игроков стало достаточное количество
        if len(self.waiting_for_game_players) >= self.PLAYERS_NEED_FOR_GAME:
            # для создания игровой сессии нужно взять первых PLAYERS_NEED_FOR_GAME игроков из очереди
            players_to_play = self.waiting_for_game_players[:self.PLAYERS_NEED_FOR_GAME]
            # обновление списка из оставшихся игроков
            self.waiting_for_game_players = self.waiting_for_game_players[self.PLAYERS_NEED_FOR_GAME:]
            # начало игровой сессии
            game_session = GameSession(players=players_to_play, send_message=self.send_message)
            self.game_sessions.append(game_session)
            game_session.start_game()
