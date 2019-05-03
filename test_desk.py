from Desk import Desk
from Cards import RegularCard
from Exception import AddCardException
import unittest

class DeskTestCase(unittest.TestCase):
    def setUp(self):
        self.desk = Desk()

    def test_first_add_card(self):
        card = RegularCard('1', '1', '1')

        self.desk.add_card_first_time(card)

        # assert что карта точно добавилась в цнтр

    def test_add_card1(self):
        self.desk.add_card_first_time(RegularCard('1', '1', '1'))
        card = RegularCard('2', '1', '1')

        self.desk.add_card(card, [60, 61])

        self.assertEqual(self.desk.desk[60][61], card)
        # assert что карта точно добавилась в цнтр

    def test_add_card2(self):
        self.desk.add_card_first_time(RegularCard('1', '1', '1'))
        self.desk.add_card(RegularCard('2', '2', '1'), [60, 61])

        with self.assertRaises(AddCardException):
            self.desk.add_card(RegularCard('2', '2', '2'), [59, 61])

        self.assertEqual(self.desk.desk[59][61], 0.0) # or 0

    def test_add_card_all_different(self):
        self.desk.add_card_first_time(RegularCard('1', '1', '1'))
        self.desk.add_card(RegularCard('2', '2', '1'), [60, 61])

        with self.assertRaises(AddCardException):
            self.desk.add_card(RegularCard('3', '2', '1'), [59, 61])

        self.assertEqual(self.desk.desk[59][61], 0.0) # or 0

    def test_score1(self):
        self.desk.add_card_first_time(RegularCard('1', '1', '1'))
        self.desk.add_card(RegularCard('2', '2', '1'), [60, 61])
        self.desk.add_card(RegularCard('3', '3', '1'), [59, 61])

        score = self.desk.countScoreThisTurn()

        self.assertEqual(score, 6)


        # assert что карта точно добавилась в центр


if __name__ == '__main__':
    unittest.main()