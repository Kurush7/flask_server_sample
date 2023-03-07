# Веб-сервер. API. БД. Python


Пример реализации веб-сервера на python
с использованием Flask и qrookDB.

Является дополнением к [лекции](https://docs.google.com/presentation/d/1Sk0qyoZXA3FUL-WbVS4pAXzNs902p9MTqVIWkMqKA4I/edit?usp=sharing).


## Запуск

1. Установка python зависимостей (python 3.8+):
```shell
pip3 install -r requirements.txt
```

2. Загрузка [датасета](https://www.kaggle.com/datasets/nguyenngocphung/10000-amazon-products-dataset).
Сохранить csv-файл в корень проекта с именем Amazon_Products.csv
3. Запустить базу данных (PostgreSQL) с помощью docker:
```shell
docker-compose up
```
4. Обработка данных и загрузка в БД:
```shell
python3 prepare_database.py
```
5. Запуск сервера:
```shell
python3 server.py
```