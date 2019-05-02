from .Exception import AddCardException
from .Desk import Desk
from .Pack import Pack

class GameSession():
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

    def startGame(self):
        """описывает начало игры (до первого хода игрока)"""
        # сгенерировать деку pack
        # выдать по 4 карты на руку каждому игроку
        ## изменить hand у player
        for player in self.players:
            self.sendMessage(
                client_id=player.client_id,
                message={
                    'type': 'hand_state',
                    'hand': [str(card) for card in player.hand.cards]
                # перевод формата numpy в формат обычных list (это нужно для json)
                }
            )
        # положить карту из pack на стол (desk)
        card = self.pack.deal_card()
        self.desk.desk.add_card(card, self.desk.desk[61][61]) # первая карта ставится в центр поля
        for player in self.players:
            self.sendMessage(
                client_id=player.client_id,
                message={
                    'type': 'desk_state',
                    'desk': [list(row) for row in self.desk.desk]
                }
            )

        current_player = self.players[self.current_turn_player_index]
        self.sendMessage(
            client_id=current_player.client_id,
            message={
                'type': 'your_turn',
                'hand': [str(card) for card in current_player.hand.cards]
            }
        )

    def onMessage(self, client_id: str, message: dict):
        if message['type'] == 'IPutCard':
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
                # print(json.dumps([list(a) for a in desk]))
                self.sendMessage(
                    client_id=player.client_id,
                    message={
                        'type': 'desk_state',
                        'desk': [list(row) for row in self.desk.desk] # перевод формата numpy в формат обычных list (это нужно для json)
                    }
                )
        elif message['type'] == 'endTurn':
            player = self.getPlayer(client_id)
            # Довыдать карты из pack так, чтобы на руке было 4 карты или до исчерпания колоды
            # А не конец ли это игры?
            # Посчитать очки

            self.sendMessage(
                client_id=player.client_id,
                message={
                    'type': 'hand_state',
                    'hand': [str(card) for card in player.hand.cards]
                # перевод формата numpy в формат обычных list (это нужно для json)
                }
            )
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
            self.current_turn_player_index = (self.current_turn_player_index + 1) % self.players
            current_player = self.players[self.current_turn_player_index]
            self.sendMessage(
                client_id=current_player.client_id,
                message={
                    'type': 'your_turn',
                    'hand': [str(card) for card in current_player.hand.cards]
                }
            )
        elif message['type'] == 'endTurnAndRewindHand':
            player = self.getPlayer(client_id)
            # все карты замешать в pack
            # из pack взять до 4-х карт и положить их в руку игрока player
            self.sendMessage(
                client_id=player.client_id,
                message={
                    'type': 'hand_state',
                    'hand': [str(card) for card in player.hand.cards] # перевод формата numpy в формат обычных list (это нужно для json)
                }
            )

            self.current_turn_player_index = (self.current_turn_player_index + 1) % self.players
            current_player = self.players[self.current_turn_player_index]
            self.sendMessage(
                client_id=current_player.client_id,
                message={
                    'type': 'your_turn',
                    'hand': [str(card) for card in current_player.hand.cards]
                }
            )
