import Player
import Desk
from Exception import AddCardException


def key_with_max_val(d):
    """
        a) create a list of the dict keys and values;
        b) return the key with the max value
    """
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def find_free_pos():
    """
    Пробегает всё поле, находит пустые позиции, добавляет их в возможные варианты хода
    :return: список позиций для хода
    """
    # TODO: нужно перестать рассматривать все пустые позиции, так как туда заведомо нельзя положить карту
    variants = list()
    for x in range(len(Desk.Desk.desk)):
        for y in range(len(Desk.Desk.desk)):
            if Desk.Desk.desk[x][y] == 0:
                variants.append((x, y))
    return variants


def find_best_pos(variants_list):
    """
    Пробегает всю руку игрока. Для каждой карты проходит по всем незанятым клеткам и создаёт список
    возможного увеличения счёта.
    :param variants_list: список незанятых позиций на поле
    :return: кортеж (карта, позиция) с наибольшим увеличением счёта
    """
    prom_values = dict()
    for card in Player.hand.cards:
        for elem in variants_list:
            try:
                Desk.Desk.add_card(card, elem)
                prom_values.update({(card, elem): Desk.Desk.countScoreThisTurn()})
                Desk.Desk.resetScore()
            except AddCardException:
                continue

    return key_with_max_val(prom_values)


def make_step(selected):
    Desk.Desk.add_card(selected)
