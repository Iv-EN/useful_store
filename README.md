[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
<div align="center">
    <h1>useful_store</h1> 
    <p>
        Это учебный проект.
    </p>
</div>

---

# Описание
Этот проект создан для изучения основ Django.

---
## На первом этапе создано: 
 - приложение `catalog`
 - два HTML-шаблона: для домашней страницы и для страницы с контактной информацией. Для стилизации страниц использовался Bootstrap
 - созданы контроллеры для отображения страниц
 - настроена маршрутизация для этих контроллеров
 - на странице контактов реализована форма обратной связи
 - настроена обработка данных формы в контроллере для отображения сообщения об успешной отправке данных
 - Введённые данные сохраняются в корне проекта в файле `сообщение_от_'введённое пользователем имя'.txt`

## На втором этапе сделано:
 - подключена СУБД PostgreSQL
 - в приложении `catalog` созданы модели `Product`, `Category`
 - созданы и применены миграции
 - все модели зарегистрированы в админке
 - выполнены тестовые задания в `Django shell` (скриншоты находятся в директории `screenshots`)
 - для моделей `Product`, `Category` сформирована фикстура `fixtures/catalog_data.json`
 - создана команда `import_json` которая сначала удаляет все существующие данные из базы, а затем добавляет данные из фикстуры в базу
 - в контроллер отображения главной страницы добавлена выборка 5 последних созданных продуктов с последующим их выводом в консоль
 - создана модель для хранения контактных данных `Contact`. Существующие в базе данные выводятся на страницу с контактами.

## На третьем этапе (домашка по шаблонизации) выполнено:
- Создан новый контроллер и шаблон для отображения страницы с подробной информацией о товаре. На этой странице отображается вся информация о товаре.
- Добавлен в шаблон главной страницы код для отображения списка товаров с помощью цикла.
- Выделены базовый шаблон, шаблоны контактов и одного товара, а также подшаблоны для меню, подвала, пагинации
- Реализована страница с формой, которая позволяет пользователю добавлять новые товары.
- Добавлен постраничный вывод товаров на главной странице.

## Рефакторинг приложения:
- Все имеющиеся контроллеры переведены с FBV на CBV
- Создано новое приложение `blog` с моделью `BlogPost`
- Для работы с блогом реализован полный CRUD с использованием CBV
- При открытии отдельной статьи увеличивается счётчик просмотров данной статьи
- На страницу списка статей выводятся только статьи, которые имеют положительный признак публикации
- После успешного создания или редактирования статьи происходит перенаправление пользователя на страницу отредактированной статьи

---
<div align="center">
    <h3 align="center">
        <p>Использовались языки и инструменты:</p>
        <div>
            <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original-wordmark.svg" title="Python" alt="Python" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/django/django-plain-wordmark.svg" title="Django" alt="Django" width="40" height="40"/>&nbsp;
            <img src="https://github.com/devicons/devicon/blob/master/icons/bootstrap/bootstrap-original-wordmark.svg" title="Bootstrap" alt="Bootstrap" width="40" height="40"/>
        </div>
    </h3>
</div>

---
## Локальная установка проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Iv-EN/useful_store.git
```
2. Создайте и активируйте виртуальное пространство:
```bash
python3 -m venv venv
```
```bash
sourse venv/bin/activate
```
3. Обновите pip и установите зависимости:
```bash
python3 -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

## Подключение к базе данных
1. Создайте базу данных `PostgreSQL`
2. В корневом каталоге создайте файл `.env` и укажите в нём переменные окружения:
```bash
SECRET_KEY=секретный ключ Django
DEBUG=True/False
NAME=имя вашей базы данных
USER=имя пользователя PostgreSQL
PASSWORD=пароль пользователя PostgreSQL
HOST=адрес сервера базы данных
PORT=порт, на котором работает PostgreSQL, обычно 5432
```
3. Примените миграции
```bash
python3 manage.py migrate
```
4. Создайте суперпользователя
```bash
python3 manage.py createsuperuser
```

## Загрузка данных из фикстуры
1. Убедитесь, что файл `fixtures/catalog_data.json` существует
2. Выполните команду для загрузки данных
```bash
python3 manage.py import_json
```

## Запуск проекта

1. Для запуска проекта из корня проекта выполните команду:
```bash
python3 manage.py runserver
```
___

<h3 align="center">
    <p><img src="https://media.giphy.com/media/iY8CRBdQXODJSCERIr/giphy.gif" width="30" height="30" style="margin-right: 10px;">Автор: Евгений Иванов. </p>
</h3>
<p align="center">
    <div align="center"  class="icons-social" style="margin-left: 10px;">
        <a href="https://vk.com/engenivanov" target="blank" rel="noopener noreferrer">
            <img src="https://img.shields.io/badge/%D0%92%20%D0%BA%D0%BE%D0%BD%D1%82%D0%B0%D0%BA%D1%82%D0%B5-blue?style=for-the-badge&logo=VK&logoColor=white" alt="В контакте Badge"/>
        </a>
        <a href="https://t.me/IvENauto" target="blank" rel="noopener noreferrer">
            <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white"/>
        </a>
    </div>
