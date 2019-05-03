from Desk import *
from Player import *

class GameSession():

    MAX_CARDS_IN_HAND = 4
    """Класс описывает игровую сессию"""
    def __init__(self, players, sendMessage): # - список игроков, посылаемые сообщения
        self.players = players
        self.sendMessage = sendMessage
        self.desk = Desk()
        self.pack = Pack()
        self.current_turn_player_index = 0

    def hasClient(self, client_id):
        """возвращает список id игроков данной сессии"""
        return any([p.client_id == client_id for p in self.players])

    def getPlayer(self, client_id):
        """идентификация игрока"""
        result = None
        for player in self.players:
            if player.client_id == client_id:
                result = player
                break
        return result

    def isValidPutCard(self, message, client_id):
        """проверка корректности хода каждого игрока"""
        #return True (or False)
        pass

    def changeTurn(self):
        """Передача хода другому игроку"""
        self.current_turn_player_index = (self.current_turn_player_index + 1) % self.players # выбор следующего игрока (по индексу заполнения очереди)
        current_player = self.players[self.current_turn_player_index]
        self.sendMessage(
            client_id=current_player.client_id,
            message={
                'type': 'YourTurn',
                'hand': [str(card) for card in current_player.hand.cards]
            }
        )

    def DeskStateMessage(self, player):
        """Сообщение о состоянии игрового поля"""
        self.sendMessage(
            client_id=player.client_id,
            message={
                'type': 'DeskState',
                'desk': [list(row) for row in self.desk.desk]
            # перевод формата numpy в формат обычных list (это нужно для json)
            }
        )

    def HandStateMessage(self, player):
        """Сообщение о состоянии руки"""
        self.sendMessage(
            client_id=player.client_id,
            message={
                'type': 'HandState',
                'hand': [str(card) for card in player.hand.cards]
            # перевод формата numpy в формат обычных list (это нужно для json)
            }
        )

    def startGame(self):
        """описывает начало игры (до первого хода игрока)"""
        # сдача четырёх карт на руку каждому игроку
        for player in self.players:
            for i in range(self.MAX_CARDS_IN_HAND):
                card = self.pack.deal_card()
                player.hand.add_card(card)
        for player in self.players:
            self.HandStateMessage(player)

        card = self.pack.deal_card() # берём верхнюю карту из колоды
        self.desk.add_card_first_time(card) # первая карта ставится в центр поля
        for player in self.players:
            self.DeskStateMessage(player)

        self.changeTurn()

    def onMessage(self, client_id: str, message: dict):
        if message['type'] == 'IPutCard':
            # проверить, что сообщение пришло от игрока, у которого сейчас ход
            #message['card'] - это ДОЛЖНО приходить
            #message['desk_position'] - это ДОЛЖНО приходить

            try:
                self.desk.add_card(message['card'], message['desk_position'])
            except AddCardException as e:
                self.sendMessage(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Так нельзя! Потому что: {str(e)}'
                    }
                )

            # валидации (...)
            # Обовление self.desk
            # Обновление hand у игрока который сейчас ходит (убрать карту, которую он выложил)
            # Послать ВСЕМ клиентам игроков обновленный стол
            for player in self.players:
                self.DeskStateMessage(player)

        elif message['type'] == 'endTurn':
            # проверить, что сообщение пришло от игрока, у которого сейчас ход
            player = self.getPlayer(client_id)

            # TODO Довыдать карты из pack так, чтобы на руке было 4 карты или до исчерпания колоды
            # А не конец ли это игры?
            #TODO дописать это нормально
            lenght_pack = self.pack.lenght() # узнаём, сколько карт осталось в колоде
            score_per_this_turn = self.desk.countScoreThisTurn() # Подсчёт очков

            if player.hand.get_amount == 0:
                score_per_this_turn *= 2

            player.score += score_per_this_turn

            self.HandStateMessage(player)

            for player in self.players:
                self.sendMessage(
                    client_id=player.client_id,
                    message={
                        'type': 'current_score',
                        'desk': [
                            {'name': player.name ,'score' : player.score}
                            for player in self.players
                        ] # перевод формата numpy в формат обычных list (это нужно для json)
                    }
                )
                self.desk.resetScore()
                self.changeTurn()

        elif message['type'] == 'endTurnAndRewindHand': # пропуск хода и обновление руки
            # проверить, что сообщение пришло от игрока, у которого сейчас ход
            player = self.getPlayer(client_id)
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

            self.HandStateMessage(player)

            self.changeTurn()


