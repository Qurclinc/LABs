import socket
MAX_TIMEDELTA = 1 # Максимальная абсолютная разница между временными меткамми
TIMEOUT = 3.0 # Максимальное время ожидания отклика клиента

FIRST_PORT = 55_000
SECOND_PORT = 56_000

def check_server_alive(port: int) -> bool:
    """Проверяет жив ли сервер по заданному порту, пытаясь подключиться к нему. В случае отсутствия
    подключения возвращает код операции вместо исключения

    Аргументы:
        port (int): Порт подключения

    Returns:
        bool: Доступность подключения
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(TIMEOUT) # Если за столько секунд не будет ответа - считается что подключение недоступно
        result = sock.connect_ex(("127.0.0.1", port))
        return result == 0 # Нулевой код считается успехом

def check_timestamp(time1: float, time2: float) -> bool:
    """Определяет валидность временной метки отправки и временной метки получения сообщения.
    В случае если абсолютная разница между ними выше допустимой, транзакция считается невалидной

    Аргументы:
        time1 (float): Первая временная метка
        time2 (float): Вторая временная метка

    Returns:
        bool: Результат сравнения
    """
    result = abs(time2 - time1) < MAX_TIMEDELTA
    if not(result):
        raise DeltatimeException()
    return True

class DeltatimeException(Exception):
    def __str__(self):
        return "Сообщение не актуально."