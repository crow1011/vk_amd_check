import logging
import time

import yaml

def get_config(conf_path='conf/config.yaml'):
    with open(conf_path, 'r') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf

conf =get_config()

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

logger = get_logger(conf['logger'])


def get_adm_count(group_id, adm_count):
    pass


def check_adm_count_change(group_id, adm_count):
    pass


def send_alert(group_id, adm_count):
    pass


def send_to_es(group_id, adm_count):
    pass



def main():
    group_id = 123
    adm_count = get_adm_count(group_id)
    adm_count_change = check_adm_count_change(group_id, adm_count)
    if adm_count_change:
        send_alert(group_id, adm_count)
    send_to_es(group_id, adm_count)



if __name__ == '__main__':
    logger.debug('# Debug mode')
    while True:
        try:
            #main()
            logger.debug('# start')
        except Exception:
            logger.exception('# Exception')
        time.sleep(conf['server']['query_interval'])