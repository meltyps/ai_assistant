from sqlalchemy.orm import sessionmaker
from sqlTable import Task, engine
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy import inspect

inspector = inspect(engine)
columns = inspector.get_columns('tasks')

for column in columns:
    print(f"{column['name']} ({column['type']})")
    
Session = sessionmaker(bind=engine)
session = Session()

new_task = Task(
    title = "Улучшить базу данных ассистента ИИ",
    description = "Написать хорошую базу данных, с которой я смогу взаимодействовать, а также граммотное управление ею, помимо этого создать новую таблицу, куда будут помещаться мои завершенные задачи, а в данной таблицы удаляться",
    due_date = datetime(2025, 8, 8),
    priority = 1,
    category = "Проект"
)