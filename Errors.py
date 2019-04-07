class MyException(Exception):
    """класс, описывающий ошибки в работе программы"""
    def __init__(self, message: str):
        self.message = message