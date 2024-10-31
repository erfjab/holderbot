import logging


def setup_logger(bot_name, level=logging.INFO):
    logger = logging.getLogger(bot_name)
    logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"data/{bot_name}.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        f"%(asctime)-25s | {bot_name} | %(levelname)-8s | %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger("HolderBot")
