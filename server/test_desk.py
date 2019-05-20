from Desk import Desk
from Cards import Card
from Exception import AddCardException
import unittest


class DeskTestCase(unittest.TestCase):
    def setUp(self):
        self.desk = Desk()

    def test_first_add_card(self):
        card = Card('1', '1', '1')

        self.desk.add_card_first_time(card)

        # assert что карта точно добавилась в цнтр

    def test_add_card1(self):
        self.desk.add_card_first_time(Card('1', '1', '1'))
        card = Card('2', '1', '1')

        self.desk.add_card(card, (50, 51))

        self.assertEqual(self.desk.desk[50, 51], card)
        # assert что карта точно добавилась в цнтр

    def test_add_card2(self):
        self.desk.add_card_first_time(Card('1', '1', '1'))
        self.desk.add_card(Card('2', '2', '1'), (50, 51))

        with self.assertRaises(AddCardException):
            self.desk.add_card(Card('2', '2', '2'), (49, 51))

        self.assertEqual(self.desk.desk[49, 51], None)  # or 0

    def test_add_card_all_different(self):
        self.desk.add_card_first_time(Card('1', '1', '1'))
        self.desk.add_card(Card('2', '2', '1'), (50, 51))

        with self.assertRaises(AddCardException):
            self.desk.add_card(Card('3', '2', '1'), (49, 51))

        self.assertEqual(self.desk.desk[49, 51], None)  # or 0

    def test_score1(self):
        self.desk.add_card_first_time(Card('1', '1', '1'))
        self.desk.add_card(Card('2', '2', '1'), (50, 51))
        self.desk.add_card(Card('3', '3', '1'), (49, 51))

        score = self.desk.count_score_this_turn()

        self.assertEqual(score, 6)

    def test_score2(self):
        self.desk.add_card_first_time(Card('1', '1', '1'))
        self.desk.add_card(Card('2', '2', '1'), (50, 51))
        self.desk.add_card(Card('3', '3', '1'), (49, 51))
        self.desk.add_card(Card('4', '4', '1'), (48, 51))

        score = self.desk.count_score_this_turn()

        self.assertEqual(score, 20)

    def test_removeDuplicatesInLines(self):
        c_input = [
            [Card('2', '2', '1'), Card('2', '2', '2')],
            [Card('2', '2', '2'), Card('2', '2', '1')],
            [Card('2', '2', '3'), Card('2', '2', '2')],
        ]

        output = self.desk.remove_duplicate_in_lines(c_input)

        self.assertEqual(output, [
            [Card('2', '2', '1'), Card('2', '2', '2')],
            [Card('2', '2', '3'), Card('2', '2', '2')],
        ])


if __name__ == '__main__':
    unittest.main()