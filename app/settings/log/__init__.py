from ._log import LoggerSetup

logger = LoggerSetup(name="HolderBot").get_logger()

__all__ = ["logger"]