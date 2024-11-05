"""
Logging setup module for the HolderBot.

This module provides a function to set up a logger for the bot,
allowing logging to both the console and a file.
"""

import logging


def setup_logger(bot_name, level=logging.INFO):
    """
    Set up a logger for the specified bot.
    """
    bot_logger = logging.getLogger(bot_name)
    bot_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(f"data/{bot_name}.log")
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        f"%(asctime)-25s | {bot_name} | %(levelname)-8s | %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    bot_logger.addHandler(console_handler)
    bot_logger.addHandler(file_handler)

    return bot_logger


# Initialize the logger for HolderBot
logger = setup_logger("HolderBot")
