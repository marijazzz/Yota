from Session_test import *
import unittest

from Player import *

def send_message(client_id, message):
    print(client_id)
    print(message)

class SessionTestCase(unittest.TestCase):


    def setUp(self):
        self.player_1 = Player(name='name_1', client_id='id_1')
        self.player_2 = Player(name='name_2', client_id='id_2')
        self.player_3 = Player(name='name_3', client_id='id_3')
        self.player_4 = Player(name='name_4', client_id='id_4')
        self.game_session = GameSession(players=(self.player_1, self.player_2, self.player_3, self.player_4), send_message=send_message)

    def test_has_client(self):
        test_client_id = 'id_1'
        self.game_session.has_client(test_client_id)

    def test_get_player(self):
        test_client_id = 'id_1'
        self.game_session.get_player(test_client_id)

    def test_change_turn(self):
        self.game_session.change_turn()

    def test_desk_state_message(self):
        player = self.player_1
        self.game_session.desk_state_message(player)

    def test_hand_state_message(self):
        player = self.player_1
        self.game_session.hand_state_message(player)

    def test_start_game(self):
        self.game_session.start_game()

    def test_message_time_limit(self):
        player = self.player_1
        self.game_session.message_time_limit(player)

    def test_on_message(self):
        client_id = 'id_1'
        message = {
                        'type': 'error',
                        'reason': f'AAA'
                    }
        self.game_session.on_message(client_id, message)


if __name__ == '__main__':
    unittest.main()