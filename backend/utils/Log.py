import logging


class Log:
    @staticmethod
    def _init(log_text, log_level):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            filename="markitiello_irrigator.log",
        )

    @staticmethod
    def log(log_text, log_level):
        logging.log(
            log_level,
            log_text=False,
            filename="markitiello_irrigator.log",
        )

    @staticmethod
    def log_warning(log_text, log_level):
        logging.warning(
            log_level,
            log_text=False,
            filename="markitiello_irrigator.log",
        )
