import logging
from aiogram.fsm.state import StatesGroup, State

class Service:
    """Класс для более удобного представления и хранения услуг.
    Поля класса соответсвуют столбцам в таблице.
    """

    def __init__(
        self, 
        id: int, 
        name: str, 
        description: str, 
        price: str, 
        age: str, 
        imgpath: str
    ):
        self.id: int          = id
        self.name: str        = name
        self.description: str = description
        self.price: str       = price
        self.age: str         = age
        self.imgpath: str     = imgpath

    def format(self) -> str:
        text_lines = [
            f"<b>{self.name}</b>",
            f"<b>Описание:</b> {self.description}",
            f"<b>Цена:</b> {self.price}"
        ]

        return "\n\n".join(text_lines) 

class Task:
    """Класс для более удобного представления и хранения заявок.
    Поля класса соответсвтуют столбцам в таблице.
    """

    def __init__(
        self, 
        id: str, 
        cliend_id: str, 
        number: str, 
        name: str, 
        services: str, 
        guests: str, 
        datetime: str
    ):
        self.id: str        = id
        self.cliend_id: str = cliend_id
        self.number: str    = number
        self.name: str      = name
        self.services: str  = services
        self.guests: str    = guests
        self.datetime: str  = datetime

    def format(self, **kwargs) -> str:
        text_lines = [
            f"<b>Клиент:</b> {[i for i in self.name.split('///')][0]}",
            f"<b>Номер телефона:</b> {[i for i in self.number.split('///')][0]}",
            ""
        ]

        try:
            if kwargs['number'] >= 0:
                services = self.services.split('///')[:-1]
                guests = self.guests.split('///')[:-1]
                datetime = self.datetime.split('///')[:-1]

                text_lines.append("<b>Услуга:</b> " + services[int(kwargs['number'])])
                text_lines.append("<b>Количество гостей:</b> " + guests[int(kwargs['number'])])
                text_lines.append("<b>Дата:</b> " + datetime[int(kwargs['number'])])
            
                return "\n".join(text_lines)
        except:
            pass

        for i in zip(self.services.split('///')[:-1], self.guests.split('///')[:-1], self.datetime.split('///')[:-1]):
            text_lines.append("<b>Услуга:</b> " + i[0])
            text_lines.append("<b>Количество гостей:</b> " + i[1])
            text_lines.append("<b>Дата:</b> " + i[2])
            text_lines.append("")

        return "\n".join(text_lines)

class User:
    """Класс для более удобного представления пользователей. Поля соответсвуют
    столбцам таблицы users
    """

    def __init__(self, id: int, phone: str, name: str):
        self.id = id
        self.phone = phone
        self.name = name

class ChooseService(StatesGroup):
    """Состояния пользователя в роли клиента.
    """

    back = State()      # Для возвращения в главное меню
    more = State()      # Если пользователь захотел выбрать больше услуг
    ages = State()      # Выбор возраста основной аудитории
    month = State()     # Выбор месяца
    day = State()       # Выбор дня
    guests = State()    # Указание количества гостей
    number = State()    # Отправка номера телефона
    name = State()      # Отправка имени клиента
    waiting = State()   # Общение с менеджером

class AdminsActions(StatesGroup):
    """Состояния пользователя в роли администратора
    """

    accepting = State() # Проверка заявок
    end = State()       # Окончание проверки
    apply = State()     # Начало процесса обработки клиента
    date = State()      # Назначение даты
    start = State()     # Назначение времени начала
    end = State()       # Назначение времени конца
    waiting = State()   # Ожидание оплаты


class CustomFormatter(logging.Formatter):
    """Класс кастомного логгера. Взят со StackOverflow
    """

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# Настройка корневого логгера для цветного вывода
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(CustomFormatter())

fileHandler = logging.FileHandler("./log.txt")
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(CustomFormatter())

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)