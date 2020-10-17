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

def get_adm_list(group_id, vk_api):
    res = vk_api.groups.getMembers(group_id=group_id, v='5.124', filter=['manages'])
    return res


def check_adm_list_change(group_id, adm_list, index):
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
        # stop and return None if it's first start
        return change_status, None
    es_adm_items = res['hits']['hits'][0]['_source']['adm_items']
    if sorted(es_adm_items) != sorted(adm_list['items']):
        change_status = True
        logger.debug(f'# fix change adm_list last:{es_adm_items} <> actual {adm_list}')
    else:
        change_status = False
        logger.debug(f'# adm_list no change. Last list {es_adm_items}')
    return change_status, es_adm_items


def send_to_es(group_id, adm_list, index, alerter):
    doc = {
        'alerter': str(alerter),
        'group_id': f"{str(group_id)}",
        'adm_count': adm_list['count'],
        'adm_items': adm_list['items'],
        '@timestamp': datetime.utcnow(),
    }
    res = es.index(index=index, body=doc)
    return res

def msg_gen(vk_api, group_id, adm_items, es_adm_items):
    group_name = vk_api.groups.getById(group_ids=group_id, v='5.124')[0]['name']
    msg = f'found a change in the list of admins for the {group_name}({group_id}) group\n'
    last_adm = vk_api.users.get(user_ids=es_adm_items, v='5.124')
    now_adm = vk_api.users.get(user_ids=adm_items,  v='5.124')
    msg += 'Last admins list:\n'
    for adm in last_adm:
        try:
            adm_first_name = adm["first_name"]
        except:
            adm_first_name = ''
        try:
            adm_last_name = adm["last_name"]
        except:
            adm_last_name = ''

        msg += f' - {adm_first_name} {adm_last_name}(user_id: {adm["id"]})'
    msg += '\nNow admins list:\n'
    for adm in now_adm:
        try:
            adm_first_name = adm["first_name"]
        except:
            adm_first_name = ''
        try:
            adm_last_name = adm["last_name"]
        except:
            adm_last_name = ''

        msg += f' - {adm_first_name} {adm_last_name}(user_id: {adm["id"]})'
    print(last_adm)
    print(now_adm)
    print(msg)
    return msg


def send_alert(chat_id, msg):
    bot.send_message(int(chat_id), msg)


def main():
    group_id = conf['vk']['group_id']
    adm_list = get_adm_list(group_id, vk_api)
    logger.debug(f'# adm_list: {adm_list} for group_id{group_id}')
    e_index = conf['es']['index']
    k_index = e_index + '*'
    alerter = conf['server']['name']
    adm_list_change, es_adm_items = check_adm_list_change(group_id, adm_list, k_index)
    print(es_adm_items)
    adm_list_change = True
    if adm_list_change:
        msg = msg_gen(vk_api, group_id, adm_list['items'], es_adm_items)
        send_alert(conf['tg']['chat_id'], msg)
        res = send_to_es(group_id, adm_list, e_index, alerter)
    else:
        if conf['server']['fix_no_change']:
            res = send_to_es(group_id, adm_list, e_index, alerter)
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
