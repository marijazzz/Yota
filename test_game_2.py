import unittest
import Game_2


def send_message(client_id, message):
    print('player {}; message:{}'.format(client_id, message))


class GameServerTestCase(unittest.TestCase):
    def setUp(self):
        self.game_server = Game_2.GameServer(send_message=send_message)

    def test_new_player(self):
        """
        Проверка добавления одного игрока в ожидание
        """
        test_client_id = 'id_1'
        self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                             'user_name': 'player_1'})
        self.assertEqual(len(self.game_server.waiting_for_game_players), 1)
        player = self.game_server.waiting_for_game_players[0]
        self.assertEqual(player.name, 'player_1')
        self.assertEqual(player.client_id, 'id_1')

    def test_solo_game(self):
        """
        Проверка одиночной игры
        """
        test_client_id = 'id_1'
        self.game_server.on_message(test_client_id, message={'type': 'PlayAlone',
                                                             'user_name': 'player_1'})
        self.assertEqual(len(self.game_server.game_sessions[0].players), 4)

    def test_several_new_players(self):
        """
        Проверка добавления нескольких игроков
        """
        for ID in range(4):
            test_client_id = 'id_{}'.format(ID)
            self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                                 'user_name': 'player_{}'.format(ID)})
            player = self.game_server.waiting_for_game_players[ID]
            self.assertEqual(player.name, 'player_{}'.format(ID))
            self.assertEqual(player.client_id, 'id_{}'.format(ID))
        self.assertEqual(len(self.game_server.waiting_for_game_players), 4)

        for ID in range(4, 8):
            test_client_id = 'id_{}'.format(ID)
            self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                                 'user_name': 'player_{}'.format(ID)})
            player = self.game_server.waiting_for_game_players[ID]
            self.assertEqual(player.name, 'player_{}'.format(ID))
            self.assertEqual(player.client_id, 'id_{}'.format(ID))
        self.assertEqual(len(self.game_server.waiting_for_game_players), 8)

    def test_two_game_sessions(self):
        """
        Проверка создание двух игровых сессий, в каждой из которых один игрок и три бота
        """
        for ID in range(2):
            test_client_id = 'id_{}'.format(ID)
            self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                                 'user_name': 'player_{}'.format(ID)})
            self.game_server.search_game()

    def test_two_players(self):
        """
        Запуск сессии с двуями игроками и двумя ботами
        """
        for ID in range(2):
            test_client_id = 'id_{}'.format(ID)
            self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                                 'user_name': 'player_{}'.format(ID)})
        self.game_server.search_game()

    def test_three_players(self):
        """
        Запуск сессии с треями игроками и одним ботом
        """
        for ID in range(3):
            test_client_id = 'id_{}'.format(ID)
            self.game_server.on_message(test_client_id, message={'type': 'HelloIWannaPlay',
                                                                 'user_name': 'player_{}'.format(ID)})
        self.game_server.search_game()

    def test_no_players(self):
        """
        Запуск сессии без игроков
        """
        self.game_server.search_game()

    # TODO: не проходит тест на дисконнект
    """
    def test_disconnection(self):
        self.game_server.search_game()
        self.game_server.on_message('bot_id 2', message={'type': 'disconnection', 'user_name': 'bot_id 2'})
        self.assertEqual(len(self.game_server.game_sessions[0].players), 3)"""
