# Мониторинг списка администраторов паблика vk

Скрипт проверяет список администраторов через интервал указанный в параметре query_interval. 
В случае изменения списка администраторов скрипт отправит уведомление в телеграмм.

Для запуска потребуется:

- [ ] [VK access token](https://vk.com/dev/access_token)
- [ ] [Telegram bot token](https://core.telegram.org/bots)
- [ ] [VK group ID - можно взять из url группы](https://vk.com/dev/groups.get)
- [ ] Telegram chat id - id вашего с ботом чата. Получить можно на шаге 2.1

# *config.yaml*

\* - обязательное поле

- *server>name - хранит пользовательское название скрипта
- *server>query_interval - хранит числовое значение интервала проверок в секундах
- *server>fix_no_change - включение/отключение записи в elasticsearch результата запроса в случае отсутствия изменений
- *vk>access_token - api-токен сообщества позволяющий получить доступ к списку администраторов группы
- *vk>group_id - идентификатор группы vk
- *es>host - адрес elasticsearch. По умолчанию равен адресу контейнера "http://es:9200"
- *es>index - название индекса в elasticsearch(если не существует то будет создан автоматически). По умолчанию vk-adm-check
- *tg>api_key - api-token бота в телеграм
- *tg>chat_id - chat_id чата, в который бот должен отправлять уведомления
- *logger>log_level - задает уровень логирования скрипта. Допустимые значения debug, info, warning, error
- *logger>log_file - название лог-файла
- *logger>log_dir - путь до директории, в которую будет записан лог-файл. При изменении необходимо изменить путь в docker-compose файлах.

# Инструкция
*1* Склонируйте репозиторий в любую директорию:
```bash
git clone https://github.com/crow1011/vk_amd_check.git
```
*2* Переименуйте файл vk_amd_check/app/conf/config.yaml.example в vk_amd_check/app/conf/config.yaml и заполните обязательные поля.
```bash
cd vk_amd_check
mv app/conf/config.yaml.example app/conf/config.yaml
```
*2.1* В случае если у вас нет tg>chat_id, заполните все поля кроме этого и 
```bash
docker-compose -f docker-compose-get_my_id.yml up -d
```
Это запустит контейнер с простым ботом, отвечающим на команду /get_my_id или /my_id текущим chat_id

После успешного получения chat_id остановите и удалите контейнер с ботом командой
```bash
docker-compose -f docker-compose-get_my_id.yml down -v
```
*3* Запустите тесты:
```bash
sudo apt install python3-pytest
cd app/
pytest-3 -s
cd ../
```
В случае успешного прохождения всех тестов можете переходить к следующему. Если тестирование выявило ошибки ознакомьтесь с
выводом и проверьте свой конфигурационный файл. 

*4* выполните команды для сбора и запуска контейнеров с elasticsearch и кодом(vk_amd_check/app):
```bash
docker-compose up -d
```

Для удаления контейнеров запустите
```bash
docker-compose down -v
```

Если вам потребуется изменить конфигурацию достаточно изменить конфигурационный файл и перезапустить контейнеры.