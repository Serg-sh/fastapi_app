import logging


def logging_config(level=logging.INFO):
    logging.basicConfig(level=level,
                        format='[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')