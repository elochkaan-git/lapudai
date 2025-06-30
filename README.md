# Telegram-бот для услуг
`![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)
Данный бот позволяет клиентам просматривать и выбирать услуги, добавленные администраторами, а администраторам проверять оставленные заявки. Они автоматически переносятся в календарь, так что редактировать и удалять их придется вручную.

## Содержание
- [Технологии](#технологии)
- [Начало работы](#начало-работы)

## Технологии
- [Google API](https://github.com/googleapis/google-api-python-client)
- [Aiogram](https://github.com/aiogram/aiogram)
- [Asyncpg](https://github.com/MagicStack/asyncpg)

## Начало работы
Для начала работы скопируйте репозиторий. В файл backend/tokenBot.py вставьте API вашего бота
```py
# backend/tokenBot.py
TOKEN = "0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
```
В файл config/admins.txt внесите Telegram ID всех администраторов. Каждый ID на новой строке.
Также нужно создать проект в Google Cloud, подключить Google Calendar API, создать Credentials, скачать их, переименовать файл в credentials.json и поместить в папку config.
После этого выполните
```sh
# Для Windows
setup.exe

# Для Unix/MacOS
chmod +x setup
./setup
```

После входа в аккаунт создатся файл token.json в папке config. Остается только выполнить
```shell
docker-compose up --build -d
```
Может потребоваться дополнительная установка Docker Desktop для Windows/MacOS и для Unix
```shell
pacman -S docker docker-compose

#or
apt-get install docker docker-compose
```
