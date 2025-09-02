from sqlalchemy.orm import sessionmaker
from sqlTable_test import engine, Task
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import text
from sqlalchemy import inspect #Библиотека для того, чтобы проверить, какие колонки есть в таблице БД

inspector = inspect(engine) # Это способ получить доступ к информации о базе данных, на которую указывает engine, через специальный объект инспектора.
columns = inspector.get_columns('tasks') # get_columns('tasks') - Он вернёт список словарей, где каждый словарь описывает одну колонку таблицы.
for column in columns:
    print(f"{column['name']} ({column['type']})")

Session = sessionmaker(bind=engine) 
#Ты создаёшь класс Session — он как шаблон для будущих сессий.
'''
sessionmaker(bind=engine) - это подключение к нашей базе 
данных через engine

Это просто заготовка — как форма или инструкция:
"Когда тебя вызовут — ты должен подключиться к этой базе."

bind переводится, как связать, здесь он говорит свяжи себя
с этой базой данных, которая передается через присваивание
'''
session = Session()
# Ты создаёшь объект (экземпляр) этого класса, т.е. 
# настоящую сессию, с помощью которой можешь работать с базой.

# Создаём объект задачи
new_task = Task(
    title="Сделать отчёт",
    description="Подготовить финансовый отчёт за месяц",
    due_date=datetime(2025, 8, 10),
    priority=1
)

# Добавляем в сессию
#session.add(new_task)
'''
Подготовь этот объект (new_task) к добавлению в базу данных.
Я хочу сохранить его как новую строку в таблице
'''

# Фиксируем изменения в базе
# session.commit()

task = session.query(Task).filter_by(id=1).first()  
''' 
получить задачу с id=1
методы из библиотеки sqlalchemy.orm

query - это метод, который создаёт базу для запроса (как SELECT * FROM tasks в SQL)

filter_by - это метод, который добавляет условие WHERE к запросу.

first() - это метод, который выполняет запрос и возвращает первую найденную строку.
'''

if task:
    task.is_completed = True
    session.commit()
'''
Тогда Python автоматически преобразует task в логическое значение:
если task — это объект → True
если task — это None → False
'''

tasks = session.query(Task).filter(Task.id >= 1, Task.id <= 4).all()
'''
tasks - переменная, которая становится типом данных list

filter(Task.id >= 1, Task.id <= 4) - это более сложный аналог filter_by, где можно писать условие в виде if/elif/else
all() - это метод, который принимает в себя все таблицы, которые соответствуют условию
'''
if tasks:
    for object in tasks:
        session.delete(object) #delete() удаляет только один из даных таблицы, поэтому нужен for ... in ...
        session.commit()
    #print(f"Удалены объекты: {tasks}")
'''
session.execute(text('ALTER SEQUENCE "tasks-test_id_seq" RESTART WITH 1')) #начинает отсчет id с нуля
session.commit()
'''