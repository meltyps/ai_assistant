from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, BigInteger
from datetime import datetime

engine = create_engine('postgresql+psycopg2://postgres:Edikri11*)@localhost:5432/ai_assistant', echo=True)
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks_test'

    id = Column(BigInteger, primary_key=True) # primary_key=True - это уникальный идентификатор строки
    title = Column(String, nullable=False) #nullable говорит нам о том, что данная колонка не может быть пустой
    description = Column(Text) #Column в SQLAlchemy — это объект, который описывает столбец таблицы в базе данных.
    created_at = Column(DateTime, default=datetime.utcnow) #default=datetime.utcnow задает текущию дату по дефолту, если не указывать
    due_date = Column(DateTime)
    is_completed = Column(Boolean, default=False) #default - это указание значения, если мы его не пишем 
    priority = Column(Integer, default=3)
    category = Column(String)

    def __repr__(self):
        return f"<Task(title='{self.title}', completed={self.is_completed})>"

Base.metadata.create_all(engine)
'''
metadata — это специальный объект SQLAlchemy, который содержит описание всей базы данных (на уровне таблиц и столбцов), 
созданное на основе моделей. Это как карта всей структуры таблиц, которые связаны с Base.
*Он сначала анализирует все таблицы, которые я описал в коде, затем через подключение engine
обращается к базе данных и сопоставляет, какие таблицы уже существуют, а какие отсутствуют. После этого создаёт только недостающие таблицы.


create_all - вызывает создание всех таблиц, которые описаны в metadata, в самой базе данных.
То есть он смотрит, какие таблицы и колонки описаны в твоих классах-моделях, и создаёт их, если их ещё нет в базе.
Если таблица уже есть, он её не трогает (чтобы не потерять данные).
'''
#Base.metadata.drop_all(engine) #Удаляем все таблицы