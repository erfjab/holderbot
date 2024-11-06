"""
Logging setup module for the HolderBot.

This module provides a function to set up a logger for the bot,
allowing logging to both the console and a file.
"""

import logging


class BotLogger:
    """
    A class to set up and manage a logger for the bot.
    This class allows logging to both the console and a file.
    """

    def __init__(self, bot_name: str, level: int = logging.INFO):
        """
        Initialize the logger for the specified bot.

        Args:
            bot_name (str): The name of the bot for which the logger is set up.
            level (int): The logging level (default is INFO).
        """
        self.bot_name = bot_name
        self.level = level
        self.bot_logger = logging.getLogger(bot_name)
        self.bot_logger.setLevel(level)
        self._setup_handlers()

    def _setup_handlers(self):
        """
        Set up the console and file handlers for logging.
        """
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(f"data/{self.bot_name}.log")
        file_handler.setLevel(logging.INFO)

        # Formatter for both handlers
        formatter = logging.Formatter(
            f"%(asctime)-25s | {self.bot_name} | %(levelname)-8s | %(message)s"
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.bot_logger.addHandler(console_handler)
        self.bot_logger.addHandler(file_handler)

    def get_logger(self):
        """
        Get the configured logger instance.

        Returns:
            logging.Logger: The configured logger instance.
        """
        return self.bot_logger

    def set_log_level(self, level: int):
        """
        Set the logging level for the logger.

        Args:
            level (int): The logging level to set.
        """
        self.bot_logger.setLevel(level)
