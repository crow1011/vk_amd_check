
import get_config, get_logger
import unittest
import sys


class ColorPrint:

    @staticmethod
    def print_fail(message, end = '\n'):
        sys.stderr.write('\x1b[1;31m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_pass(message, end = '\n'):
        sys.stdout.write('\x1b[1;32m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_warn(message, end = '\n'):
        sys.stderr.write('\x1b[1;33m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_info(message, end = '\n'):
        sys.stdout.write('\x1b[1;34m' + message.strip() + '\x1b[0m' + end)

    @staticmethod
    def print_bold(message, end = '\n'):
        sys.stdout.write('\x1b[1;37m' + message.strip() + '\x1b[0m' + end)


class ConfigTest(unittest.TestCase, ColorPrint):
    def setUp(self):
        # case: check syntax yaml in config file
        self.print_info('\nGet Config file')
        self.conf = get_config.get_config()
        self.print_pass('Done')

    def test_conf(self):
        self.print_bold('---------------------------')
        self.print_bold('Case: check required fields')
        self.print_bold('---------------------------')
    def test_conf_server(self):
        # start server block
        self.print_info('Checking server->name type is string and is not empty ""')
        self.assertEqual(type(self.conf['server']['name']), str)
        self.assertNotEqual(len(self.conf['server']['name']), 0)
        self.print_pass('Done')

        self.print_info('Checking type of field server->query_interval is number and is bigger than 0')
        self.assertEqual(type(self.conf['server']['query_interval']), int)
        self.assertEqual(self.conf['server']['query_interval'] > 0, True)
        self.print_pass('Done')

        self.print_info('Checking server->fix_no_change type  is boolean')
        self.assertEqual(type(self.conf['server']['fix_no_change']), bool)
        self.print_pass('Done')
        # end server block
    def test_conf_vk(self):
        # start vk block
        self.print_info('Checking vk->access_token type is string and is not empty "" ')
        self.assertEqual(type(self.conf['vk']['access_token']), str)
        self.assertNotEqual(len(self.conf['vk']['access_token']), 0)
        self.print_pass('Done')

        self.print_info('Checking vk->group_id type is string and is not empty ""')
        self.assertEqual(type(self.conf['vk']['group_id']), str)
        self.assertNotEqual(len(self.conf['vk']['group_id']), 0)
        self.print_pass('Done')
        # end vk block

    def test_conf_es(self):
        # start es block
        self.print_info('Checking es->host type is string and is not empty ""')
        self.assertEqual(type(self.conf['es']['host']), str)
        self.assertNotEqual(len(self.conf['es']['host']), 0)
        self.print_pass('Done')

        self.print_info('Checking es->index type is string and is not empty ""')
        self.assertEqual(type(self.conf['es']['index']), str)
        self.assertNotEqual(len(self.conf['es']['index']), 0)
        self.print_pass('Done')
        # end es block

    def test_conf_tg(self):
        # start tg block
        self.print_info('Checking tg->api_key type is string and is not empty ""')
        self.assertEqual(type(self.conf['tg']['api_key']), str)
        self.assertNotEqual(len(self.conf['tg']['api_key']), 0)
        self.print_pass('Done')

        self.print_info('Checking tg->chat_id type is string and is not empty ""')
        self.assertEqual(type(self.conf['tg']['chat_id']), str)
        self.assertNotEqual(len(self.conf['tg']['chat_id']), 0)
        self.print_pass('Done')
        # end tg block

    def test_conf_logger(self):
        # start logger block
        self.print_info('Checking logger->log_level type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_level']), str)
        self.assertNotEqual(len(self.conf['logger']['log_level']), 0)
        self.print_pass('Done')

        self.print_info('Checking logger->log_file type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_file']), str)
        self.assertNotEqual(len(self.conf['logger']['log_file']), 0)
        self.print_pass('Done')

        self.print_info('Checking logger->log_dir type is string and is not empty ""')
        self.assertEqual(type(self.conf['logger']['log_dir']), str)
        self.assertNotEqual(len(self.conf['logger']['log_dir']), 0)
        self.print_pass('Done')
        # end logger block



