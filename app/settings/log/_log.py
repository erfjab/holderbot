import logging


class LoggerSetup:
    def __init__(self, name: str, level: int = logging.INFO):
        self.bot_logger = logging.getLogger(name)
        self.bot_logger.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)-25s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        self.bot_logger.addHandler(console_handler)

    def get_logger(self):
        return self.bot_logger