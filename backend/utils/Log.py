import logging


class Log:
    @staticmethod
    def _Init(log_text, log_level):
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(message)s",
            level=logging.INFO,
            datefmt="%Y-%m-%d %H:%M:%S",
            filename="markitiello_irrigator.log",
        )

    @staticmethod
    def Log(log_text, log_level):
        logging.log(
            log_level,
            log_text=False,
            filename="markitiello_irrigator.log",
        )

    @staticmethod
    def LogWarning(log_text, log_level):
        logging.warning(
            log_level,
            log_text=False,
            filename="markitiello_irrigator.log",
        )
