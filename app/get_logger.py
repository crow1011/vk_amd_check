import logging


def get_logger(logger_conf):
    log_file = logger_conf['log_dir'] + logger_conf['log_file']
    logger = logging.getLogger(__name__)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log_level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR
    }
    logger.setLevel(log_level[logger_conf['log_level']])
    return logger