# Документация
Контент документации:
1. Архитектура Базы Данных
2. Установка проекта и запуск

## Архитектура Базы Данных
Архитектура базы данных в приведена в файле docs/ТЗ.docx

## Установка проекта и запуск
```
Install python3.10

pip3 install pipenv
cd project_dir
pipenv install
pipenv shell
python manage.py runserver
```

## API документация
1. GET список кафешек: /cafes/
2. GET кафе: /cafes/{:cafeId}/
3. GET все места в одном кафе: /cafes/{:cafeid}/places/
4. GET список броней: /reserves/{:caféid}/?day={dd-MM-YYYY}  
Пример: GET /reserves/1/?day=08-06-2022
5. POST новая бронь: /reserves/
В тело запроса записать:
```
{
  'place': 1,
  'reserve_start_time': '2022-06-12T00:00:01',
  'reserve_duration': 3600
}
```
place - ID of place  
reserve_start_time - must be in format 'YYYY-MM-DDThh:mm:ss'  
reserve_duration - time of reservation in seconds
Response will be:
```
Not successful
{
  "status": "0"
}
Successful
{
  "status": "1"
}
```

6. GET брони пользователя: /reserves/
7. GET конкретная бронь: /reserve/{:reserveId}/
8. PATCH менять инфу о броне (время): /reserve/{reserveId}/
9. DELETE удаление брони: /reserve/{reserveId}/
10. GET получить инфу о юзере: /user/
11. PATCH менять инфу о юзере: /user/
12. DELETE удаление аккаунта со всеми резервами сразу: /user/
