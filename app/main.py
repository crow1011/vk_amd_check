import logging
import time
from datetime import datetime
import elasticsearch
import yaml
import vk
import telebot

def get_config(conf_path='conf/config.yaml'):
    with open(conf_path, 'r') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf


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


# get config from default path conf/config.yaml
conf = get_config()
logger = get_logger(conf['logger'])
session = vk.Session(access_token=conf['vk']['access_token'])
vk_api = vk.API(session)
es = elasticsearch.Elasticsearch(conf['es']['host'])
bot = telebot.TeleBot(conf['tg']['api_key'])

def get_adm_count(group_id, vk_api):
    res = vk_api.groups.getMembers(group_id=group_id, v='5.124', filter=['manages'])
    return res


def check_adm_count_change(group_id, adm_count, index):
    change_status = None
    res = es.search(index=index, body={
        "size": 1,
        "sort": {"@timestamp": "desc"},
        "query": {
            "term": {'group_id':{"value": f"{str(group_id)}"}}
        }
    })
    if res['hits']['total']['value']==0:
        logger.debug('# index or group_id not found')
    elif res['hits']['hits'][0]['_source']['adm_count']!=adm_count:
        change_status = True
        last_count = res['hits']['hits'][0]['_source']['adm_count']
        logger.debug(f'# fix change adm_count last:{last_count} != actual {adm_count}')
    elif res['hits']['hits'][0]['_source']['adm_count']!=adm_count:
        change_status = False
        last_count = res['hits']['hits'][0]['_source']['adm_count']
        logger.debug('# adm_count no change')
    return change_status


def send_to_es(group_id, adm_count, index, alerter):
    doc = {
        'alerter': str(alerter),
        'group_id': f"{str(group_id)}",
        'adm_count': adm_count,
        '@timestamp': datetime.utcnow(),
    }
    res = es.index(index=index, body=doc)
    return res

def send_alert(group_id, adm_count):
    #for send
    pass


def main():
    group_id = conf['vk']['group_id']
    adm_count = get_adm_count(group_id, vk_api)['count']
    logger.debug(f'# adm_count: {adm_count} for group_id{group_id}')
    e_index = conf['es']['index']
    k_index = e_index + '*'
    alerter = conf['server']['name']
    adm_count_change = check_adm_count_change(group_id, adm_count,k_index)
    if adm_count_change:
        send_alert(group_id, adm_count)
        res = send_to_es(group_id, adm_count, e_index, alerter)
    else:
        if conf['server']['fix_no_change']:
            res = send_to_es(group_id, adm_count, e_index, alerter)
    return True


if __name__ == '__main__':
    logger.debug('# Debug mode')
    while True:
        try:
            logger.debug('# start')
            print('# start')
            print(main())
        except Exception:
            logger.exception('# Exception')
            print(Exception)
        time.sleep(conf['server']['query_interval'])
