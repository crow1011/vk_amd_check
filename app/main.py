# stock
import time
from datetime import datetime
# install
import elasticsearch
import vk
import telebot
# new
from get_config import get_config
from get_logger import get_logger



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
    elif res['hits']['hits'][0]['_source']['adm_count']==adm_count:
        change_status = False
        last_count = res['hits']['hits'][0]['_source']['adm_count']
        logger.debug(f'# adm_count no change. Last count {last_count}')
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

def send_alert(chat_id, msg):
    bot.send_message(int(chat_id), msg)


def main():
    group_id = conf['vk']['group_id']
    adm_count = get_adm_count(group_id, vk_api)['count']
    logger.debug(f'# adm_count: {adm_count} for group_id{group_id}')
    e_index = conf['es']['index']
    k_index = e_index + '*'
    alerter = conf['server']['name']
    adm_count_change = check_adm_count_change(group_id, adm_count,k_index)
    adm_count_change = True
    if adm_count_change:
        msg = f"Changing adm_count for group_id: {str(adm_count)}. Now count: {str(adm_count)}"
        send_alert(conf['tg']['chat_id'], msg)
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
