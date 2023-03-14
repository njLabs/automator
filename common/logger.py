import logging


def configure_logging():
    logging.basicConfig(
            filename='./logs/example.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='w', level=logging.DEBUG
    )
    logging.getLogger(__name__).setLevel(logging.WARNING)
