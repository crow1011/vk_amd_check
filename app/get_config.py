import yaml
import os

print(os.getcwd())
conf_path = 'conf/config.yaml'


def get_config(conf_path=conf_path):
    with open(conf_path, 'r') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf


def get_tg_config(conf_path=conf_path):
    with open(conf_path, 'r') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf['tg']

def get_logger_config(conf_path=conf_path):
    with open(conf_path, 'r') as file:
        conf = yaml.load(file, Loader=yaml.FullLoader)
    return conf['logger']