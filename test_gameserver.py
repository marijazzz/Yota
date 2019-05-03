from Game import GameServer
import unittest

def sendMessage(client_id, message):
    print(client_id)
    print(message)

class GameServerTestCase(unittest.TestCase):
    def setUp(self):
        self.game_server = GameServer(sendMessage=sendMessage)

    def test_new_player(self):

        test_client_id = 'id_1'
        self.game_server.onMessage(test_client_id, message={
            'type': 'HelloIWannaPlay',
            'user_name': 'p1'
        })
        self.assertEqual(len(self.game_server.waiting_for_game_players), 1)
        player = self.game_server.waiting_for_game_players[0]
        self.assertEqual(player.name, 'p1')
        self.assertEqual(player.client_id, 'id_1')

    def test_new_game_session(self):
        for i in range(4):
            test_client_id = f'id_{str(i)}'

            self.game_server.onMessage(test_client_id, message={
                'type': 'HelloIWannaPlay',
                'user_name': f'p{str(i)}'
            })

        self.assertEqual(len(self.game_server.game_sessions), 1)
        game_session = self.game_server.waiting_for_game_players[0]
        self.assertEqual(len(game_session.players), 4)

class DeskTestCase(unittest.TestCase):
    def setUp(self):
        self.desk = GameServer(sendMessage=sendMessage)
if __name__ == '__main__':
    unittest.main()