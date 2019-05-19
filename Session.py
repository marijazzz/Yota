from Desk import *
from Player import *
from Pack import *
import time
import asyncio


class GameSession:
    """Класс описывает игровую сессию"""

    MAX_CARDS_IN_HAND = 4


    def __init__(self, players, send_message, max_turn_duration_sec: int = 90):
        """
        :param players: список игроков
        :param send_message: посылаемые сообщения
        :param max_turn_duration_sec: максимальная продолжительность хода 90 секунд
        """
        self.players = players
        self.send_message = send_message
        self.desk = Desk()
        self.pack = Pack()
        self.current_turn_player_index = 0
        self.loop = asyncio.get_event_loop()
        self.time_is_over_task = None
        self._max_turn_duration_sec = max_turn_duration_sec


    def has_client(self, client_id):
        """
        Возвращает список id игроков данной сессии
        :param client_id:
        :return:
        """
        return any([p.client_id == client_id for p in self.players])


    def get_player(self, client_id):
        """
        Идентификация игрока
        :param client_id:
        :return:
        """
        result = None
        for player in self.players:
            if player.client_id == client_id:
                result = player
                break
        return result


    async def time_is_over_coroutine(self):
        """
        Контроль времени хода
        :return:
        """
        await asyncio.sleep(self._max_turn_duration_sec) # ожидание по времени 90 секунд
        await self.change_turn() # передача хода другому игроку по истечении 90 секунд


    async def change_turn(self):
        """
        Передача хода другому игроку
        :return:
        """
        self.current_turn_player_index = (self.current_turn_player_index + 1) % 4 # выбор следующего игрока (по индексу заполнения очереди)

        current_player = self.players[self.current_turn_player_index]
        current_player.label = 'turn'
        self.send_message(
            client_id=current_player.client_id,
            message={
                'type': 'YourTurn',
                'hand': [str(card) for card in current_player.hand.cards]
            }
        )


    def desk_state_message(self, player):
        """
        Сообщение о состоянии игрового поля
        :param player:
        :return:
        """
        self.send_message(
            client_id=player.client_id,
            message={
                'type': 'DeskState',
                'desk': [list(row) for row in self.desk.desk]
            # перевод формата numpy в формат обычных list (это нужно для json)
            }
        )


    def hand_state_message(self, player):
        """
        Сообщение о состоянии руки
        :param player:
        :return:
        """
        self.send_message(
            client_id=player.client_id,
            message={
                'type': 'HandState',
                'hand': [str(card) for card in player.hand.cards]
            # перевод формата numpy в формат обычных list (это нужно для json)
            }
        )


    async def start_game(self):
        """
        Описывает начало игры (до первого хода игрока)
        :return:
        """
        # сдача четырёх карт на руку каждому игроку
        for player in self.players:
            for i in range(self.MAX_CARDS_IN_HAND):
                card = self.pack.deal_card()
                player.hand.add_card(card)
        for player in self.players: # отправка информации о картах на руке каждому игроку
            self.hand_state_message(player)

        card = self.pack.deal_card() # берём верхнюю карту из колоды
        self.desk.add_card_first_time(card) # первая карта ставится в центр поля
        for player in self.players: # передаём игрокам информацию об изменении состояния игрового поля
            self.desk_state_message(player)

        if self.time_is_over_task is not None: # отменяем предыдущую задачу
            self.time_is_over_task.cancel()
        self.time_is_over_task = self.loop.create_task(self.time_is_over_coroutine()) # запускаем "счётчик" заново

        await self.change_turn() # передача хода другому игроку


    async def on_message(self, client_id: str, message: dict):
        """
        Функция ответа сервера на разные сообщения от клиента
        :param client_id:
        :param message:
        :return:
        """
        if message['type'] == 'IPutCard':
            # проверка того, что сообщение пришло от игрока, у которого сейчас ход
            if self.players[self.current_turn_player_index].client_id != client_id:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Не твой ход'
                    }
                )
                return

            if self.time_is_over_task is not None: # отменяем предыдущую задачу
                self.time_is_over_task.cancel()
            self.time_is_over_task = self.loop.create_task(self.time_is_over_coroutine()) # запускаем "счётчик" заново

            player = self.get_player(client_id) # идентификация игрока

            try:
                self.desk.add_card(message['card'], message['desk_position']) # добавление карты в указанное место
            except AddCardException as e:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Так нельзя! Потому что: {str(e)}'
                    }
                )

            player.hand.play_card(message['card'])  # убираем карту из руки
            self.hand_state_message(player) # посылаем игроку сообщение о состоянии его руки

            # Посылаем всем клиентам игроков обновленный стол
            for player in self.players:
                self.desk_state_message(player)

        elif message['type'] == 'endTurn':
            # проверка того, что сообщение пришло от игрока, у которого сейчас ход
            if self.players[self.current_turn_player_index].client_id != client_id:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Не твой ход'
                    }
                )
                return

            if self.time_is_over_task is not None: # отменяем предыдущую задачу
                self.time_is_over_task.cancel()
            self.time_is_over_task = self.loop.create_task(self.time_is_over_coroutine()) # запускаем "счётчик" заново

            player = self.get_player(client_id)

            while player.hand.get_amount() != 4:
                if self.pack.lenght() != 0:
                    card = self.pack.deal_card()
                    player.hand.add_card(card)
                else: # конец колоды
                    break

            score_per_this_turn = self.desk.count_score_this_turn() # Подсчёт очков

            if player.hand.get_amount == 0:
                score_per_this_turn *= 2

            player.score += score_per_this_turn

            self.hand_state_message(player)

            for player in self.players:
                self.send_message(
                    client_id=player.client_id,
                    message={
                        'type': 'current_score',
                        'desk': [
                            {'name': player.name ,'score' : player.score}
                            for player in self.players
                        ] # перевод формата numpy в формат обычных list (это нужно для json)
                    }
                )
                self.desk.reset_score()
                await self.change_turn() # передача хода другому игроку

            if player.hand.get_amount() == 0 and self.pack.lenght() == 0:
                for player in self.players:
                    self.send_message(
                        client_id=player.client_id,
                        message={
                            'type': 'endGame',
                            'matter': f'Игра окончена'
                        }
                    )

        elif message['type'] == 'endTurnAndRewindHand': # пропуск хода и обновление руки
            # проверка того, что сообщение пришло от игрока, у которого сейчас ход
            if self.players[self.current_turn_player_index].client_id != client_id:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Не твой ход'
                    }
                )
                return

            if self.time_is_over_task is not None: # отменяем предыдущую задачу
                self.time_is_over_task.cancel()
            self.time_is_over_task = self.loop.create_task(self.time_is_over_coroutine()) # запускаем "счётчик" заново

            player = self.get_player(client_id)
            # возвращаем все карты в колоду
            for i in range(player.hand.get_amount()):
                card = player.hand.play_card() # забираем карту у игрока
                self.pack.addCard(card) # кладём карту в колоду
            self.pack.shuffle() # перемешиваем колоду
            # добавляем 4 карты в руку игроку
            if self.pack.lenght() >= 4: # если в колоде осталось больше 4 карт
                for i in range(4):
                    card = self.pack.deal_card() # забираем карту из колоды
                    player.hand.add_card(card) # добавляем карту в руку игроку
            else: # если в колоде осталось меньше 4 карт
                for i in range(self.pack.lenght()):
                    card = self.pack.deal_card() # забираем карту из колоды
                    player.hand.add_card(card) # добавляем карту в руку игроку

            self.hand_state_message(player)
            await self.change_turn() # передача хода другому игроку

        # игрок решил покинуть игру, при этом все его карты остаются на столе, карты с его руки добавляются в колоду, последняя перемешивается
        elif message['type'] == 'disconnection':
            player = self.get_player(client_id)
            self.players.remove(player) # находим и удаляем данного игрока из очереди

            # Посылаем всем игрокам сообщение о том, какой игрок решил покинуть игру
            for player_ in self.players:
                self.send_message(
                    client_id=player_.client_id,
                    message={
                        'type': 'removePlayer',
                        'matter': [{'name': player.name}, f'Вышел из игры']
                    }
                )

            # добавляем карты из руки данного игрока в колоду
            while player.hand.get_amount() != 0:
                card = player.hand.play_card(0)
                self.pack.addCard(card)

            self.pack.shuffle() # перемешиваем колоду