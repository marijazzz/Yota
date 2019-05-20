# Документация по работе сервера:
# Файл Card.py

Содержит класс `Card`.

## Class Card

Описывает характеристики обычных карт.

### method __init__(self, color, value, form)

*color*: параметр цвета карты <br>
*value*: числовой параметр карты <br>
*form*: параметр формы карты <br>


### method __eq__(self, other)

Сравнение карт по свойствам. <br>
Возвращает `True`, если свойства карт эквиваленты, `False` в противном случае.

### method color(self)

Возвращается значение, отвечающее определённому цвету. <br>
1: Красный <br>
2: Синий <br>
3: Зелёный <br>
4: Жёлтый <br>


### method value(self)

Возвращается значение, отвечающее определённому численному значению. <br>
1: 1 <br>
2: 2 <br>
3: 3 <br>
4: 4 <br>

### method form(self)

Возвращается значение, отвечающее определённой форме. <br>
1: Треугольник <br>
2: Крест <br>
3: Круг <br>
4: Квадрат <br>

# Файл Pack.py

Содержит класс `Pack`. <br>
Импортирован класс `Card` из файла `Cards`. <br>
Импортирован метод `shuffle` из библиотеки `random`. <br>

## Class Pack

Описывает колоду карт.

### method __init__(self)

Генератор списков создающий колоду из 64 карт: <br>
```
self.cards = [Card(s, v, f)
              for s in color
              for v in value
              for f in form]
```

`self.shuffle()` - перетасовка колоды карт

### method shuffle(self)

Перемешивание карт.
```
shuffle(self.cards)

```
### method add_card(self, card: Card)

Добавление переданной карты в колоду.

```
self.cards.append(card)
```

### method deal_card(self)

Сдача карты из колоды. <br>
Удаляется последний элемент из колоды.<br>
```
return self.cards.pop()
```


### method length(self)

Возвращает количество карт в колоде.
```
return len(self.cards)
```

# Файл Player.py

Содержит классы `Hand`, `Player`. <br>


## Class Hand

Описание состояния руки.

### method __init__(self)

Создаётся массив с картами. Изначально рука пустая: <br>
```
self.cards = []
```

### method add_card(self, card)

Добавление карт в руку игрока.<br>
*card*: карта, которую нужно добавить в руку игроку.

```
self.cards.append(card)
```


### method get_amount(self)

Возвращает количество карт.

```
return len(self.cards)
```

### method play_card(self, number)

Убирает карту из руки и передает карту на обработку, чтобы положить на поле. <br>
*number*: удаляемая карта.<br>

```
for elem in self.cards:
    if elem.__repr__() == number.__repr__():
        self.cards.remove(elem)
        return elem
```


## Class Player

Описывает идентификационные параметры игрока, количество очков у игрока, состояние руки игрока.

### method  __init__(self, name, client_id)

*name*: имя игрока <br>
*client_id*: id <br>

### method  add_card(self, card)

Добавление карт. <br>
*card*: карта, которая добавляется в руку данному игроку. <br>

```
self.hand.add_card(card)
```


# Файл Desk.py

Содержит класс `Desk`. <br>
Импортированы `defaultdict` из библиотеки `collections` и `List` из библиотеки `typing`.<br>
Импортирован полностью файл `Exception`.<br>


## Class Desk

Описание игрового поля.

### method __init__(self)

Создаётся словарь, с пустыми значениями в виде None; максимальным считаем размер поля 103 * 103. <br>
```
self.desk = defaultdict(return_none)
```
Изначально считаем, что карт на поле нет.<br>
```
self.positions_of_cards_added_this_turn = []
```

### method add_card_first_time(self, card)

Добавление первой карты в центр поля. <br>
*card*: карта, которую нужно добавить в центр поля (51, 51). 
```
self.desk[(51, 51)] = card
```

### method is_line_validation(line: List[Card])

Проверка корректности постановки данной карты по отношению к другим картам в линии. <br>
*line*: список карт <br>
Функция включает проверку длины линии, если она превышает 4, то игроку отправляется сообщение об ошибке: <br>
```
if len(line) > 4:  
raise LineException('Линия очень длинная')
```
Проверка на соответствие свойствам карт линии выбранной карты. В случае несоответствия игроку посылается сообщение об ошибке:<br>
```
 for property_idx in range(Card.PROPERTY_NUM):
            line_property_values = [card.properties[property_idx] for card in line]

            if not (len(set(line_property_values)) == 1
                    or len(line_property_values) == len(set(line_property_values))):
                raise LineException("""Все карты в линии должны иметь либо одинковое значение,
                                       либо у всех карт разное значвение по каждому из 3-х свойств!""")
```

### method get_lines_that_has_position(desk: defaultdict, position: tuple)

Поиск линий, расположенных рядом с заданной позицией. <br>
*desk*: словарь <br>
*position*: координаты переданного положения на поле (кортеж) <br>

Сдвиг по координатам от указанного положения поля производится на единицу вправо, влево, вверх и вниз: <br>
```
offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
```
Создаём массивы с горизонтальными и вертикальными линиями, которыё могут быть расположены с указанной позицией:<br>
```
result_horizontal_line = [desk[position]]  
result_vertical_line = [desk[position]]
```
Проверка соседних позиций: <br>
```
for offset in offsets:
            cards_in_direction = []
            current_position = (position[0] + offset[0], position[1] + offset[1])
            current_card = desk[current_position]
            while current_card is not None:
                cards_in_direction.append(current_card)
                current_position = (current_position[0] + offset[0], current_position[1] + offset[1])
current_card = desk[current_position]
```
Классифицируем найденные линии и возвращаем массив с таковыми:<br>
```
if offset[0] == 0:
                result_vertical_line += cards_in_direction
            else:
                result_horizontal_line += cards_in_direction

return [result_vertical_line, result_horizontal_line]
```

### method add_card(self, card, position: tuple)

Добавление карт на поле. <br>
*card*: карта, которую нужно поставить на поле <br>
*position*: координаты переданного положения на поле  <br>

Проверка того, что карта добавляется на пустое место. Если в указанном месте лежит карта, игроку посылается сообщение об ошибке:<br>
```
 if self.desk[position] is not None:
            raise AddCardException('Сюда поставить карту нельзя, там уже есть карты')

        desk_copy = self.desk.copy()
        desk_copy[position] = card
        lines = self.get_lines_that_has_position(desk_copy, position)
cards_this_turn = [self.desk[position] for position in self.positions_of_cards_added_this_turn]
```
Проверка того, что все выложенные карты составляют одну линию. Если условия не выполняются, клиенту посылается сообщение об ошибке. <br>
```
lines_that_contains_all_cards_this_turn = [
            line for line in lines if set(cards_this_turn).issubset(set(line))
        ]
        if len(lines_that_contains_all_cards_this_turn) != 1:
AddCardException(f'Все карты, выложенные в этот ход, должны составлять одну линию')
```
Проверка того, что около карты находится другая карта. Если условия не выполняются, клиенту посылается сообщение об ошибке. <br>
```
if all(len(line) == 1 for line in lines):
AddCardException(f'Карта должна примыкать к одной из выложенных карт')
```

Проверка того, что карта соответсвует свойствам карт данной линии. Если условия не выполняются, клиенту посылается сообщение об ошибке:<br>
```
for line in lines:
            
    try:
        self.is_line_validation(line)
    except LineException as e:
        raise AddCardException(f'Сюда поставить карту нельзя. Ошибка линии: {str(e)}')

self.desk[position] = card
self.positions_of_cards_added_this_turn.append(position)
```

### method reset_score(self)

Сброс очков. <br>
```
self.positions_of_cards_added_this_turn = []
```

### method remove_duplicate_in_lines(lines)

При пересечение линий исключается подсчёт очков для одной общей карты дважды.<br>
*lines*: список линий, выложенных на столе <br>


### method count_score_this_turn(self)

Подсчёт очков за один ход. <br>
Изначально считаем, что нет очков за ход и количество измененных линий представляет собой пустой массив.<br>
```
lines_that_changes_this_turn = []
score = 0
```
Заполняем массив с изменёнными линиями: <br>
```
for position in self.positions_of_cards_added_this_turn:
            lines = self.get_lines_that_has_position(self.desk, position)
lines_that_changes_this_turn += lines
```
Нужно удалить все дубликаты: <br>
```
lines_that_changes_this_turn = self.remove_duplicate_in_lines(lines_that_changes_this_turn)
```
Подсчёт очков в каждой изменённой за 1 ход линии: <br>
```
for line in lines_that_changes_this_turn:  
            if len(line) > 1:
                for card in line:
score += int(card.value)
```
Удваивание очков, если вся линия полна: <br>
```
if self.positions_of_cards_added_this_turn == 4:
score *= 2
```

# Файл Session.py

Содержит класс `GameSession`. <br>
Импортирована библиотека `asyncio`. <br>
Импортированы полностью файлы `Pack` и `Desk`. <br>


## Class GameSession

Описание игровой сессии. <br>

### method __init__(self, players, send_message, max_turn_duration_sec: int = 90)

*players*: список игроков<br>
*send_message*: посылаемые сообщения<br>
*max_turn_duration_sec*: максимальная продолжительность хода 90 секунд<br>
```
self.players = players
self.send_message = send_message
self.desk = Desk()
self.pack = Pack()
self.current_turn_player_index = 0
self.loop = asyncio.get_event_loop()
self.time_is_over_task = None
self._max_turn_duration_sec = max_turn_duration_sec
self.bots = []
```

### method has_client(self, client_id)

Возвращает список id игроков данной сессии. <br>
*client_id*: id <br>
```
 return any([p.client_id == client_id for p in self.players])
```

### method get_player(self, client_id)

Идентификация игрока. Возвращает определённого игрока. <br>
*client_id*: id <br>
```
result = None
for player in self.players:
    if player.client_id == client_id:
        result = player
        break
return result

```

### async method time_is_over_coroutine(self)

Контроль времени хода. Через 90 секунд ход передаётся следующему игроку. <br>
Ожидание по времени 90 секунд:<br>
```
await asyncio.sleep(self._max_turn_duration_sec) 
```
Передача хода другому игроку по истечении 90 секунд:<br>
```
await self.change_turn()
```

### async method change_turn(self)

Передача хода другому игроку. <br>
Выбор следующего игрока (по индексу заполнения очереди):<br>

При наличии ботов обеспечивает работоспособность каждому боту. При переходе к следующему игроку 
```
self.current_turn_player_index = (self.current_turn_player_index + 1) % 4
```

и отправке необходимых сообщений клиенту (по подобию `desk_state_message(self, player)`), происходит проверка 
соответствия найденного игрока некоторому боту. В случае обнаружения бота запускается алгоритм его логики. После этого 
запускается остальной функционал сервера, чтобы не было лишних отправок на клиент. 

Функция обёрнута в конструкцию `try - except`, чтобы не было итерации к несуществующему игроку. 

Если, все же, это происходит, игра заканчивается преждевременно (или же вовремя, если карты кончились)



Отправка игроку сообщения о том, что начался его код, а также состояние его руки: <br>
```
current_player = self.players[self.current_turn_player_index]
current_player.label = 'turn'
self.send_message(
    client_id=current_player.client_id,
    message={
        'type': 'YourTurn',
        'hand': [str(card) for card in current_player.hand.cards]
    }
)
```

### method desk_state_message(self, player)

Сообщение о состоянии игрового поля. Отправляется всем игрокам. <br>

Аналогичным образом отправляется состояние боту. 

*player*: игрок, которому будет отправлено данное сообщение. <br>
```
 self.send_message(
            client_id=player.client_id,
            message={
                'type': 'DeskState',
                'desk': [list(row) for row in self.desk.desk]
                # перевод формата numpy в формат обычных list (это нужно для json)
            }
        )

```


### method hand_state_message(self, player)

Сообщение о состоянии руки указанного игрока. Отправляется только указанному игроку. <br>

Аналогичным образом отправляется сообщение боту. 

*player*: игрок, которому будет отправлено данное сообщение. <br>
```
self.send_message(
            client_id=player.client_id,
            message={
                'type': 'HandState',
                'hand': [str(card) for card in player.hand.cards]
                # перевод формата numpy в формат обычных list (это нужно для json)
            }
)
```

### async method start_game(self)

Описывает начало игры (до первого хода игрока).<br>
Вначале происходит сдача четырёх карт на руку каждому игроку:<br>
```
for player in self.players:
            for i in range(self.MAX_CARDS_IN_HAND):
                card = self.pack.deal_card()
player.hand.add_card(card)
```
Каждому игроку отправляется сообщение о его картах на руке: <br>
```
for player in self.players:  
self.hand_state_message(player)
```
Берём верхнюю карту из колоды: <br>
```
card = self.pack.deal_card()
```
Первая карта ставится в центр поля: <br>
```
self.desk.add_card_first_time(card)  
```
Передаём игрокам информацию об изменении состояния игрового поля:<br>
```
for player in self.players: 
    self.desk_state_message(player)
```
Передача хода другому игроку:<br>
```
await self.change_turn()
```

### async method on_message(self, client_id: str, message: dict)

Функция ответа сервера на разные сообщения от клиента. <br>
*client_id*: id <br>
*message*: сообщение, поступившие от клиента <br>

Обработка сообщения от клиента `IPutCard`:<br>
Вначале проверяется, что сообщение пришло от игрока, чей сейчас ход:<br>
```
if self.players[self.current_turn_player_index].client_id != client_id:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Не твой ход'
                    }
                )
    return False
```

Идентифицируем игрока и добавляем карту в указанное место: <br>
```
player = self.get_player(client_id)  

            try:
                self.desk.add_card(message['card'], message['desk_position'])  
            except AddCardException as e:
                self.send_message(
                    client_id=client_id,
                    message={
                        'type': 'error',
                        'reason': f'Так нельзя! Потому что: {str(e)}'
                    }
)
```

Убираем карту из руки: <br>
```
player.hand.play_card(message['card'])
```
Посылаем игроку сообщение о состоянии его руки: <br>
```
self.hand_state_message(player)
```
Посылаем всем клиентам игроков обновленный стол: <br>
```
for player in self.players:
    self.desk_state_message(player)
```
Смена хода. <br>

Обработка сообщения от клиента `endTurn`:<br>
Вначале проверяется, что сообщение пришло от игрока, чей сейчас ход.<br>
Проверка того, не окончание ли это игры. Проверяется количество карт в колоде и количество карт на руке у игрока: <br>
```
while player.hand.get_amount() != 4:
                if self.pack.length() != 0:
                    card = self.pack.deal_card()
                    player.hand.add_card(card)
                else:  # конец колоды
                    break
```
Подсчёт очков:<br>
```
score_per_this_turn = self.desk.count_score_this_turn()
```
Начисление удвоенного количества очков, если после хода рука у игрока остаётся пустой: <br>
```
if player.hand.get_amount == 0:
                score_per_this_turn *= 2

player.score += score_per_this_turn
```
Игроку посылаетя сообщение о сообщение о состоянии руки: <br>
```
self.hand_state_message(player)
```
Всем игрокам передаётся информация о количестве баллов, полученных игроком за данный ход: <br>
```
for player in self.players:
                self.send_message(
                    client_id=player.client_id,
                    message={
                        'type': 'current_score',
                        'desk': [
                            {'name': player.name, 'score': player.score}
                            for player in self.players
                        ]  # перевод формата numpy в формат обычных list (это нужно для json)
                    }
                )
                self.desk.reset_score()
                await self.change_turn() 
```
Обработка сообщения от клиента `endTurnAndRewindHan`:<br>
Вначале проверяется, что сообщение пришло от игрока, чей сейчас ход:<br>
Возвращаем все карты в колоду:<br>
```
for i in range(player.hand.get_amount()):
                card = player.hand.play_card() 
                self.pack.add_card(card)  
                self.pack.shuffle() 
```
Добавляем 4 карты в руку игроку: <br>
```
if self.pack.length() >= 4:  
                for i in range(4):
                    card = self.pack.deal_card()  
                    player.hand.add_card(card)  
            else:  # если в колоде осталось меньше 4 карт
                for i in range(self.pack.length()):
                    card = self.pack.deal_card() 
                    player.hand.add_card(card)
```
Смена хода. <br>

Обработка сообщения от клиента `disconnection`:<br>
Находим и удаляем данного игрока из очереди: <br>
```
player = self.get_player(client_id)
self.players.remove(player) 
```
Посылаем всем игрокам сообщение о том, какой игрок решил покинуть игру: <br>
```
for player_ in self.players:
    self.send_message(
        client_id=player_.client_id,
        message={
            'type': 'removePlayer',
            'matter': [{'name': player.name}, f'Вышел из игры']
            }
       )
```
Добавляем карты из руки данного игрока в колоду: <br>
```
while player.hand.get_amount() != 0:
    card = player.hand.play_card(0)
    self.pack.add_card(card)
```


# Файл Exception

Содержит классы `AddCardException(Exception)` и `LineException(Exception)`. Используются при обработке ошибок. 

# Файл Game_3

Содердит класс `GameServer`. <br>
Импортированы библиотеки `time`, `socket`. <br>
Из файла `Player` импортирован класс `Player`. <br>
Из файла `Session` импортирован класс `GameSession`. <br>


## GameServer
 Описывает взаимодействие игроков и сервера. <br>

### method __init__(self, send_message, max_turn_duration_sec: int = 90)

*send_message*: сообщение от клиента
*self.waiting_for_game_players*: очередь из игроков, ожидающих начала игры
*game_sessions *: данная игровая сессия
*_max_turn_duration_sec*: максимальное врмя хода 90 секунд


### async method go_go_game(self)

Запускает игру при наличии достаточного количества игроков. <br>
Для создания игровой сессии нужно взять первых PLAYERS_NEED_FOR_GAME игроков из очереди:<br>
```
players_to_play = self.waiting_for_game_players[:self.PLAYERS_NEED_FOR_GAME]
```

Oбновление списка из оставшихся игроков:<br>
```
self.waiting_for_game_players = self.waiting_for_game_players[self.PLAYERS_NEED_FOR_GAME:]
```
Начало игровой сессии: <br>
```
game_session = GameSession(players=players_to_play,
                                   send_message=self.send_message,
                                   max_turn_duration_sec=self._max_turn_duration_sec)
self.game_sessions.append(game_session)
await game_session.start_game()

```

### method add_bots_for_offline(self)
Добавление трёх ботов, если нет соединения.<br>
Каждому боту присваивается имя и id: <br>
```
 for i in range(3):
            self.bots_counter += 1
            client = Player(name='Bot {}'.format(self.bots_counter),
            client_id='bot_id {}'.format(self.bots_counter))
```
Добавление бота в очередь: <br>
```
self.waiting_for_game_players.append(client)
```

### async method on_message(self, client_id: str, message: dict)

Отклик сервера на различные сообщения. <br>
*client_id*: id <br>
*message*: сообщения, приходящие от клиентов <br>

Обработка сообщения от клиента `HelloIWannaPlay`:<br>
Проверка наличие интернет-соединения: <br>
Если соединение есть, то добавляем клиента в очередь игры: <br>
```
if is_connected(REMOTE_SERVER):
    client = Player(client_id=client_id, name=message['user_name'])
    self.waiting_for_game_players.append(client) 
```

Если нет соединения, то добавляем трёх ботов и запускаем с ними игру: <br>
```
else:
    self.add_bots_for_offline()  
    await self.go_go_game() 
```
Обработка сообщения от клиента `PlayAlone`:<br>
Добавление трёх ботов и запуск игры: <br>
```
client = Player(client_id=client_id, name=message['user_name'])
self.waiting_for_game_players.append(client)  
self.add_bots_for_offline()  
await self.go_go_game() 
```
Обработка сообщения от клиента `IPutCard`:<br>
```
elif message['type'] == 'IPutCard':
    await send_for_all()
```

Обработка сообщения от клиента `endTurn`:<br>
```
elif message['type'] == 'endTurn':
    await send_for_all()
```

Обработка сообщения от клиента `endTurnAndRewindHand`:<br>
```
elif message['type'] == 'endTurnAndRewindHand':
    await send_for_all()
```

Обработка сообщения от клиента `disconnection`:<br>
```
elif message['type'] == 'disconnection':
    await send_for_all()
```

### async method search_game(self)

Поиск игроков. <br>

Если игроков меньше, чем PLAYERS_NEED_FOR_GAME (4), 
```
if len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
```
пока игроков не станет PLAYERS_NEED_FOR_GAME
```
while len(self.waiting_for_game_players) < self.PLAYERS_NEED_FOR_GAME:
```
обнуляем таймер
```
timer = 0
```
запоминаем количество игроков при запуске таймера
```
current_found = self.waiting_for_game_players
```
                
запускаем минуту ожидания
```
while timer < 2
```
каждую секунду проверяем, изменилось ли количество игроков
```
if len(self.waiting_for_game_players) == current_found:
```
если их столько же, итерируем ещё секунду
```
time.sleep(1)
timer += 1
```
если изменилось, но все ещё не 4, то обнуляем счётчик и снова ждём
```
else:
    current_found = len(self.waiting_for_game_players)
    timer = 0
```
если за 60 секунд никого не нашёл, добавляем на пустые места ботов
```
    self.bots_counter += 1
    client = Player(name='Bot {}'.format(self.bots_counter),
                client_id='bot_id {}'.format(self.bots_counter))
    self.waiting_for_game_players.append(client)  # добавление бота в очередь
await self.go_go_game()
```
 
 Если игроков стало достаточное количество, то запускается игра.


## Файл Bot.py

Содержит класс `Bot.py(bot_id)

### method init(self, bot_id)

```
__init__(self, bot_id):
        self.bot_id = bot_id
        self.W_AREA = Desk.Desk.MAX_DIMENSION
        self.current_state = []
        self.hand = []
        self.this_card = 0
```

### method current_desk_state(self, engaged)

Определяет состояние поля, получая на вход списки координат занятых клеток. 

Возвращает массив с нулями на свободных местах и единицами на занятых


```
current_state = [[0 for _ in range(self.W_AREA)] for _ in range(self.W_AREA)]
        for elem in engaged:
            current_state[elem[0]][elem[1]] = 1
        return current_state
```

### method score_best(self, this_card)

Логика бота. Пробегает всю матрицу, полученную в `current_desk_state()`. 

Для точки, которая точно имеет рядом с собой хотя бы одну единицу, но при этом сама хранит значение нуля, бот пытается 
поставить карту, определённую в 'on_message()'. 

Если поставить карту не удаётся по каким-то причинам, бот заканчивает ход. 

Если у бота нет карт в `self.hand`, то он отключается от игры. 

Карта ставится формирование сообщения вида 

```
message = {'type': 'IPutCard',
           'card': Card(card[:1], card[1:2], card[2:3]),
           'desk_position': (x, y)}
```

Параметры класса `Card` намеренно переданы таким образом, чтобы не было противоречий с `Session.GameSession`. 

_ох уж этот legacy код :-)_


Отключение и завершение хода формируются следующими сообщениями соответственно: 

```
message = {'type': 'disconnection'}
```


```
message = {'type': 'endTurn'}
```

## method on_message(self, message)

Бот "ловит сообщения" от сервера до того, как они попадут на клиент. 

В зависимости от характера сообщения:  

1) `if message['type'] == 'error'` переключает карту в руке на следующую, тем самым влияя на `score_bes(this_card)`. 

2) `if message['type'] == 'HandState'` обновляет состояние руки бота при каждом обновлении от сервера 

3) `elif message['type'] == 'DeskState'` обновляет знания бота об игровом поле

4) `elif message['type'] == 'YourTurn'` запускает `best_score`, предварительно обновив `self.hand`. Не то что бы это
было необходимо, однако раз сообщение позволяет это сделать, происходит повторная проверка. 
 
_____________________
 
#Докуметация по графике


### ***Class ImageWidget***


```python
    def __init__(self, parent):
        super(ImageWidget, self).__init__()
        self.image = QPixmap()
        self.image.load('logo.png')
        self.parent = parent
```

Инициализация виджета с заставкой для игры, добавление на него изображения


```python
    def paintEvent(self, QPaintEvent):
        painter = QPainter()
        painter.begin(self)
        rect = QtCore.QRect(0, 0, self.parent.width(), self.parent.height())
        painter.fillRect(rect, QtCore.Qt.white)
        painter.drawPixmap(0, 0, self.parent.width(), self.parent.height(), self.image)
        painter.end()
```

Отрисовка заставки

### ***Class Card***


```python
    def __init__(self):
        self.card = None
        self.image = QPixmap()
```

Инициализация параметров карты - ее цифровая кодировка и изображение


```python
    def set_card(self, card):
        self.card = card
        self.image.load(str(self.card) + '.png')
```

Добавление параметра карты и ее изображение

### ***Class Tile***


```python
    def __init__(self):
        self.card = None
        self.piece_image = None
```

Инициализация параметров клетки - наличия карты и ее изображения


```python
    def set_image(self, image):
        self.card = 1
        self.piece_image = image
```

При вызове функции на клетку добавляется карта (т.е. карта есть в наличие) и ее изображение


```python
    def get_image(self):
        return self.piece_image
```

При вызове функции возвращается изображение карты, если в клетке она есть, иначе *None*

### ***class CardWidget***


```python
    def __init__(self, parent=None):
        super(CardWidget, self).__init__()
        self.parent = parent
        self.field_size = 103
        self.tile_size = 100
        self.play_field = [[0] * self.field_size for i in range(self.field_size)]
        for i in range(self.field_size):
            for j in range(self.field_size):
                self.play_field[i][j] = Tile()
        self.card_images = []
        self.card_rectangles = []
        self.setAcceptDrops(True)
        self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
        self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
        self.tile_image = self.load_tile_image('tile.png')
        self.central_tile_image = self.load_tile_image('tile.png')
```

Инициализация характеристик игрового поля, положений карт, самих карт и поля


```python
    def zoom_in(self):
        if self.tile_size < 100:
            self.tile_size += 5
            self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.update()
            self.parent.scroll_area.horizontalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * self.parent.CardWidget.field_size // 2)
            self.parent.scroll_area.verticalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * self.parent.CardWidget.field_size // 2)
```

 *zoom in* поля с центрированием положения слайдеров


```python
    def zoom_out(self):
        if self.tile_size > 30:
            self.tile_size -= 5
            self.setMinimumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.setMaximumSize(self.tile_size * self.field_size, self.tile_size * self.field_size)
            self.update()
            self.parent.scroll_area.horizontalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * (self.parent.CardWidget.field_size - 3) / 2)
            self.parent.scroll_area.verticalScrollBar().setSliderPosition(
                self.parent.CardWidget.tile_size * (self.parent.CardWidget.field_size - 1) / 2)
```

 *zoom out* поля с центрированием положения слайдеров


```python
    def clear(self):
        self.play_field = [[0] * self.field_size for i in range(self.field_size)]
        self.update()
```

Очистка игрового поля


```python
    def load_tile_image(self, path=None):
        new_image = QPixmap()
        if not new_image.load(path):
            QMessageBox.warning(self, "Open Image", "The image file could not be loaded.", QMessageBox.Cancel)
            return
        return new_image
```

Открытие изображения для клеток игрового поля


```python
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('card'):
            event.accept()
        else:
            event.ignore()
```

Проверка на допустимость *dragEvent*


```python
    def dragLeaveEvent(self, event):
        self.update()
        event.accept()
```

Добавление допустимости выхода *dragEvent*


```python
    def dragMoveEvent(self, event):
        square = self.target_square(event.pos())
        if event.mimeData().hasFormat('card') and (self.play_field[square.x() // self.tile_size]
        [square.y() // self.tile_size].get_image()) is None:
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()
        self.update()
```

Организация самого *dragEvent* с проверкой на то, что объект, который хотят сдвинуть имеет необходимый тип


```python
    def dropEvent(self, event):
        if event.mimeData().hasFormat('card'):
            card_data = event.mimeData().data('card')
            stream = QtCore.QDataStream(card_data, QtCore.QIODevice.ReadOnly)
            square = self.target_square(event.pos())
            image = QPixmap()
            stream >> image
            self.update(square)
            event.setDropAction(QtCore.Qt.MoveAction)
            if (self.play_field[square.x() // self.tile_size][square.y() // self.tile_size].get_image()) is None:
                if self.parent.client.check_card(image) == 1:
                    self.play_field[square.x() // self.tile_size][square.y() // self.tile_size].set_image(image)
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()
```

Организация самого *dropEvent* с проверкой на то, что объект, который хотят помстить на поле имеет необходимый тип, и место доступно для опускания


```python
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        r = QtCore.QRect(0, 0, self.field_size * self.tile_size, self.field_size * self.tile_size)
        painter.fillRect(r, QtCore.Qt.white)
        for x in range(self.field_size):
            for y in range(self.field_size):
                if self.play_field[x][y].card is None:
                    if x == 52 and y == 52:
                        painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                           self.central_tile_image)
                    else:
                        painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                           self.tile_image)
                else:
                    painter.drawPixmap(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size,
                                       self.play_field[x][y].get_image())

        painter.end()
```

Отрисовка поля, клеток и карт


```python
    def target_square(self, position):
        return QtCore.QRect(position.x() // self.tile_size * self.tile_size,
                            position.y() // self.tile_size * self.tile_size, self.tile_size, self.tile_size)
```

Определение клетки, куда собираются опустить карту

### ***class CardModel***





```python
    def __init__(self, parent=None):
        super(CardModel, self).__init__(parent)
        self.image_stack = []
        self.images = []
```

Инициализация переменных - колоды кард и их изображений


```python
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DecorationRole:
            return QIcon(self.images[index.row()].scaled(60, 60,
                                                         QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        if role == QtCore.Qt.UserRole:
            return self.images[index.row()]
        return None
```

Проверка на валидность индекса в модели, проверка на то, что данные это что-либо, что можно использовать для декорации, и проверка на необходимость показа карт в списке (выполняется при необходимом типе приходящих данных)


```python
    def add_card(self, image):
        else:
            row = len(self.images)
        self.beginInsertRows(QtCore.QModelIndex(), row, row)
        self.images.insert(row, image)
        self.endInsertRows()
```

Добавление одной карты в список карт, определение ее позиции там


```python
    def flags(self, index):
        if index.isValid():
            return (QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsDragEnabled)
        return QtCore.Qt.ItemIsDropEnabled
```

Проверка на валидность объекта для перетаскивания


```python
 def removeRows(self, row, count, parent):
        if parent.isValid():
            return False
        if row >= len(self.images) or row + count <= 0:
            return False
        begin_row = max(0, row)
        end_row = min(row + count - 1, len(self.images) - 1)
        self.beginRemoveRows(parent, begin_row, end_row)
        del self.images[begin_row:end_row + 1]
        self.endRemoveRows()
        return True
```

Удаление рядов при переносе и установке карты на поле


```python
    def mimeTypes(self):
        return ['card']
```

Возвращает допустимые типы данных


```python
    def mimeData(self, indexes):
        mime_data = QtCore.QMimeData()
        encoded_data = QtCore.QByteArray()
        stream = QtCore.QDataStream(encoded_data, QtCore.QIODevice.WriteOnly)
        for index in indexes:
            if index.isValid():
                image = QPixmap(self.data(index, QtCore.Qt.UserRole))
                stream << image
        mime_data.setData('card', encoded_data)
        return mime_data
```

Присвоение добавляемым элементам необходимого типа данных *card*


```python
    def rowCount(self, parent):
        if parent.isValid():
            return 0
        else:
            return len(self.images)
```

Функция, возвращающая количество рядов в модели


```python
    def supportedDropActions(self):
        return QtCore.Qt.CopyAction | QtCore.Qt.MoveAction
```


```python
Поддержка перемещения и копирования данных на *CardWidget*
```


```python
    def set_stack(self, images):
        self.image_stack = images
```

Создание колоды в модели


```python
    def add_cards(self):
        for y in range(len(self.images), 4):
            if len(self.image_stack) != 0:
                img = self.image_stack.pop(0)
                card_image = img.image.copy(0, 0, 500, 500)
                self.add_card(card_image
```

Добавление не более четырех кард в видимый список. Выполняется в начале игры, после конца хода и только при наличии карт в колоде

### ***class MainWindow***


```python
 def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.frame = QFrame()
        self.frameLayout = QGridLayout(self.frame)
        self.cardList = QListView()
        self.model = CardModel(self)
        self.CardWidget = CardWidget(parent=self)
        self.scroll_area = QScrollArea()
        self.scroll_widget = self.CardWidget
        self.splitter = QSplitter()
        self.rulesButton = QPushButton('Правила')
        self.playButton = QPushButton('Играть')
        self.zoom_inButton = QPushButton('zoom in')
        self.zoom_outButton = QPushButton('zoom out')
        self.end_turnButton = QPushButton('Закончить ход')
        self.exitButton = QPushButton('Exit')
        self.splitter2 = QSplitter()
        self.buttons = QFrame()
        self.buttonLayout = QHBoxLayout(self.buttons)
        self.player_name = QLineEdit()
        self.set_nameButton = QPushButton('Ввести имя')
        self.tmp_widget = ImageWidget(self)
        self.cardImage = QPixmap()
        self.setGeometry(200, 200, 400, 400)
        self.set_up_menus()
        self.set_up_widgets()
        self.player = 'Player'
        self.setWindowTitle("Ёпта")
        self.client = client.Client()
```

Данная функция отвечает за инициализацию специфических параметров для главного окна - виджетов, клиента, игрока, размеров, а так же вызывает расположение виджетов и создание  меню, подключение кнопок к функциям разных виджетов


```python
    def open_image(self):
        new_image = []
        z = ['411', '212', '312', '112', '342', '321', '234', '322', '333', '242', '222', '444']
        for i in range(12):
            temporary_image = Card()
            temporary_image.set_card(z[i])
            new_image.append(temporary_image)
        self.cardImage = new_image
        self.set_up_card()
```

Функция *open_image* после получения колоды с сервера создает все 64 объекта *Card*, присваивая им "название" карты и пиксмап с ее изображением. Затем она вызывает функцию *set_up_card* класса *MainWindow*


```python
    def set_up_card(self):
        self.model.set_stack(self.cardImage)
        self.model.add_cards()
        self.CardWidget.clear()
```

Данная функция отвечает за создание колоды и добавление карт в модель, что вызывается функциями *add_cards*, *set_stack* класса *CardModel*, а так же очищает все, что могло было быть на виджете с полем методом *clear* класса *CardWidget*


```python
 def set_up_menus(self):
        game_menu = self.menuBar().addMenu("&Game")
        exit_action = game_menu.addAction("E&xit")
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(qApp.quit)
        rules_action = game_menu.addAction('Rules')
        rules_action.triggered.connect(self.show_message)
        rules_action.setShortcut("Ctrl+R")
```

Метод *set_up_menus* создает строку меню, добавляя туда возможность выйти и открыть правила, а так же быстрые ссылки на них


```python
 def set_up_widgets(self):
        self.cardList.setDragEnabled(True)
        self.cardList.setViewMode(QListView.IconMode)
        self.cardList.setIconSize(QtCore.QSize(80, 80))
        self.cardList.setGridSize(QtCore.QSize(90, 90))
        self.cardList.setSpacing(10)
        self.cardList.setMovement(QListView.Snap)
        self.cardList.setAcceptDrops(True)
        self.cardList.setDropIndicatorShown(True)
        self.cardList.setModel(self.model)
        self.cardList.setMaximumWidth(100)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 10) / 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 5) / 2)
        self.splitter.addWidget(self.cardList)
        self.splitter.addWidget(self.scroll_area)
        self.buttonLayout.addWidget(self.rulesButton)
        self.buttonLayout.addWidget(self.playButton)
        self.buttonLayout.addWidget(self.zoom_inButton)
        self.buttonLayout.addWidget(self.zoom_outButton)
        self.buttonLayout.addWidget(self.end_turnButton)
        self.buttonLayout.addWidget(self.exitButton)
        self.buttonLayout.addWidget(self.set_nameButton)
        self.player_name.setText('Player')
        self.splitter2.setOrientation(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.splitter)
        self.splitter2.addWidget(self.buttons)
        self.frameLayout.addWidget(self.player_name)
        self.frameLayout.addWidget(self.splitter2)
        self.setCentralWidget(self.frame)
        self.set_nameButton.clicked.connect(self.set_name)
        self.rulesButton.clicked.connect(self.show_message)
        self.playButton.clicked.connect(self.start_game)
        self.zoom_inButton.clicked.connect(self.zoom_in)
        self.zoom_outButton.clicked.connect(self.zoom_out)
        self.end_turnButton.clicked.connect(self.end_turn)
        self.exitButton.clicked.connect(qApp.quit)
        self.player_name.hide()
        self.frameLayout.addWidget(self.tmp_widget)
        self.tmp_widget.show()
        self.set_nameButton.show()
        self.end_turnButton.hide()
        self.zoom_inButton.hide()
        self.zoom_outButton.hide()
        self.splitter2.hide()
        self.splitter.hide()
```

Установление виджетов согласно лэйаутам, расположение сплиттеров, изначальное срасположение кнопок


```python
    def set_name(self):
        text_box_value = self.player_name.text()
        self.player = text_box_value
```

Функция обновления имени игрока


```python
    def logo(self):
        self.tmp_widget.hide()
        self.splitter2.show()
        self.player_name.show()
```

Показ заставки, и затем начального игрового окна


```python
    def start_game(self):
        self.playButton.hide()
        self.rulesButton.hide()
        self.zoom_inButton.show()
        self.zoom_outButton.show()
        self.end_turnButton.show()
        self.splitter.show()
```

Функция вызываемая с помощью  *self.playButton*. Начинает игру обновляя экран и показывая необходимые для игры виджеты.


```python
    def end_turn(self):
        self.model.add_cards()
```

Функция вызываемая *end_turnButton*.  Означает конец хода игрока, вызывает добавление карт в модель методом  *add_cards* класса *CardModel*


```python
    def zoom_in(self):
        self.CardWidget.zoom_in()
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * self.CardWidget.field_size // 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * self.CardWidget.field_size // 2)
```

Функция *zoom in* для поля


```python
    def zoom_out(self):
        self.CardWidget.zoom_out()
        self.scroll_area.horizontalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 3) / 2)
        self.scroll_area.verticalScrollBar().setSliderPosition(
            self.CardWidget.tile_size * (self.CardWidget.field_size - 1) / 2)
```

Функция *zoom out* для поля

### ***Main***


```python
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.open_image()
    window.show()
    tmr = QtCore.QTimer()
    tmr.setSingleShot(True)
    tmr.timeout.connect(window.logo)
    tmr.start(1500)
    sys.exit(app.exec_())
```

Создание игрового окна и таймаут заставки






```python

```
