import logging
import os

def setup_logger(name=__name__):
    """
    Настройка и получение логгера.
    Создает папку logs/ если её нет.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Проверяем, есть ли уже обработчики, чтобы не дублировать логи
    if not logger.handlers:
        # Форматтер
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Файловый обработчик
        file_handler = logging.FileHandler(os.path.join(log_dir, "test_execution.log"), encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Консольный обработчик
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
