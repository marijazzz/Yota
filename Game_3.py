import time
import socket

from Player import Player
from Session import GameSession

REMOTE_SERVER = "www.google.com"


def is_connected(hostname):
    try:
        host = socket.gethostbyname(hostname)
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except socket.error:
        pass
    return False


class GameServer:
    PLAYERS_NEED_FOR_GAME = 4  # количество человек в одной игре
    bots_counter = 0  # счётчик ботов для обеспечения уникальности имени и ID

    def __init__(self, send_message, max_turn_duration_sec: int = 90):
        self.send_message = send_message  # сообщение от клиента
        self.waiting_for_game_players = []  # очередь из игроков, ожидающих начала игры
        self.game_sessions = []  # данная игровая сессия
        self._max_turn_duration_sec = max_turn_duration_sec
        self.bots = []

    async def go_go_game(self):
        """
        Запускает игру при наличии достаточного количества игроков
        """
        # для создания игровой сессии нужно взять первых PLAYERS_NEED_FOR_GAME игроков из очереди
        players_to_play = self.waiting_for_game_players[:self.PLAYERS_NEED_FOR_GAME]
        # обновление списка из оставшихся игроков
        self.waiting_for_game_players = self.waiting_for_game_players[self.PLAYERS_NEED_FOR_GAME:]
        # начало игровой сессии
        game_session = GameSession(players=players_to_play,
                                   send_message=self.send_message,
                                   max_turn_duration_sec=self._max_turn_duration_sec)

        self.game_sessions.append(game_session)
        await game_session.start_game()

    def add_bots_for_offline(self):
        for i in range(3):
            print('Adding bot...')
            self.bots_counter += 1
            client = Player(name='Bot {}'.format(self.bots_counter),
                            client_id='bot_id {}'.format(self.bots_counter))
            self.waiting_for_game_players.append(client)  # добавление бота в очередь

    async def on_message(self, client_id: str, message: dict):
        """
        Отклик сервера на различные сообщения
        :param client_id:
        :param message:
        :return:
        """

        async def send_for_all():
            for session in self.game_sessions:
                if session.has_client(client_id):
                    await session.on_message(client_id, message)

        # если игрок нажал "хочу играть"
        if message['type'] == 'HelloIWannaPlay':
            # проверяем наличие интернет-соединения
            if is_connected(REMOTE_SERVER):
                # если есть, то добавляем в очередь игры
                client = Player(client_id=client_id, name=message['user_name'])
                self.waiting_for_game_players.append(client)  # добавление данного игрока в очередь
            # если нет, запускаем игру с ботами
            else:
                self.add_bots_for_offline()  # добавляет трёх ботов
                await self.go_go_game()  # запускает игру

        # если игрок нажал "хочу играть один" и в сессии он один
        elif message['type'] == 'PlayAlone':
            client = Player(client_id=client_id, name=message['user_name'])
            self.waiting_for_game_players.append(client)  # добавление данного игрока в очередь
            self.add_bots_for_offline()  # добавляет трёх ботов
            await self.go_go_game()  # запускает игру

        # если сообщение о том, что игрок положил карту на стол
        elif message['type'] == 'IPutCard':
            await send_for_all()

        # окончание игры
        elif message['type'] == 'endTurn':
            await send_for_all()

        # пропуск хода
        elif message['type'] == 'endTurnAndRewindHand':
            await send_for_all()

        # выход из игры
        elif message['type'] == 'disconnection':
            await send_for_all()

    async def search_game(self):
        """
        Поиск игроков
        """
        # если игроков меньше, чем PLAYERS_NEED_FOR_GAME
        if len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
            # то пока их не станет PLAYERS_NEED_FOR_GAME
            while len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
                # обнуляем таймер
                timer = 0
                # запоминаем количество игроков при запуске таймера
                current_found = self.waiting_for_game_players
                # запускаем минуту ожидания
                while timer < 2:
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
                print('adding bot')
                self.bots_counter += 1
                client = Player(name='Bot {}'.format(self.bots_counter),
                                client_id='bot_id {}'.format(self.bots_counter))
                self.waiting_for_game_players.append(client)  # добавление бота в очередь
            await self.go_go_game()  # запускам игру

        # если игроков стало достаточное количество
        else:
            await self.go_go_game()  # запускам игру
