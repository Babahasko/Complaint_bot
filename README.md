# Complaint_bot
**Состояние проекта:** в разработке

# Предназначение
Телеграмм бот для ведения статистик жалоб отслеживаемых объектов.
Разработан на основе API [complaint_statistic](https://github.com/Babahasko/complaint_statistic)

Вам надоело, что ваши коллеги постоянно жалуются? Не знаете куда
от этого деваться и что с этим делать? Начните вести статистику!
В этом телеграмм боте вы можете создавать отслеживаемые объекты(Нытиков),
создавать темы их жалоб и записывать, кто и на что жаловался.
А затем получить красивые графики с ТОПом самых больших жалобщиков и душнил!.
Кроме того вы также можете проанализировать, на что вам жалуются чаще всего.

## Описание проекта
Проект написан на aiogram и полностью зависит от [complaint_statistic](https://github.com/Babahasko/complaint_statistic)

## Реализованный функционал
1. Регистрация пользователей
2. Добавление, получение списка и удаление тем на которые жалуются ваши объекты


## Запуск бота
Перед запуском проекта, у вас должно быть развернуто и работать в docker приложение complaint_statistic
Копируем проект
```shell
git clone https://github.com/Babahasko/Complaint_bot
cd Сomplaint_statistic
```

Создаём виртуальное окружение и активируем его
```shell
python -m venv .venv
.venv/Scripts/activate
```

Загружаем зависимости
```shell
pip install poetry
poetry install
```
или
```shell
pip install -r requirements.txt
```

Прописываем переменные окружения в файле ".env.template" и переименовываем его в ".env",
а именно BOT_TOKEN, который мы получаем у **BotFather**. Инструкция по получению токена от BotFather-> [клик](https://core.telegram.org/bots/tutorial#registering-the-bot)
```
BOT_TOKEN=<your_bot_token>
```
Запускаем проект с помощью docker-compose
```shell
docker-compose up -d --build
```
Запуск проекта в консоли
```shell
python main.py
```

## Планы на будущее
Развернуть бота на арендуемом сервере и наслждаться