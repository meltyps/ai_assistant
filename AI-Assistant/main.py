from add_files.sqlTable import engine, Task, Complited
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from add_files.analyze import CommandAnalyzer as cmanls
from add_files.local_database.intents import task_intents

class Function:
    def __init__(self, user_text):
        self.user_text = user_text

    def output(self):
        type_of_info = cmanls(self.user_text).analyze()
        Session = sessionmaker(bind=engine)

        if type_of_info == "show_tasks":
            with Session() as session:
                tasks = session.query(Task.id, Task.title, Task.description, Task.is_completed, Task.due_date, Task.category, Task.priority).all()

                if not tasks:
                    print("У вас пока нет задач.")
                else:
                    for id_, title, description, is_completed, due_date, category, priority in tasks: 
                        status = "Завершено" if is_completed else "В процессе"
                        print(f"\n🔹 ID: {id_}\n📌 Заголовок: {title}\n📝 Описание: {description}\n📅 Дедлайн: {due_date}\n🏷️  Категория: {category}\n⭐ Приоритет: {priority}\n📍 Статус: {status}\n")
        
        elif type_of_info == "add_task":
            user_title = input("Название заголовка: ").strip()
            user_description = input("Описание задачи: ").strip()
            
            while True:
                user_due_date = input("Дедлайн (формат ГГГГ-ММ-ДД): ").strip()
                try:
                    due_date_obj = datetime.strptime(user_due_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Неверный формат даты. Попробуйте снова.")

            while True:
                user_priority = input("Уровень приоритета (От 1 до 3): ").strip()
                if user_priority.isdigit() and 1 <= int(user_priority) <= 3:
                    user_priority = int(user_priority)
                    break
                else:
                    print("Приоритет должен быть числом от 1 до 3. Попробуйте снова.")

            user_category = input("Категория: ").strip()

            new_task = Task(
                title = user_title,
                description = user_description,
                due_date = due_date_obj,
                priority = user_priority,
                category = user_category
            )

            user_answer = input("Вы уверены, что хотите создать эту задачу? ").lower()
            agree = user_answer in task_intents["confirmation"]

            if agree:
                with Session() as session:
                    session.add(new_task)
                    session.commit()
                print("✅ Задача успешно создана!")
            else:
                print("❌ Создание задачи отменено.")

        elif type_of_info == "task_done":
            morph_data = cmanls(self.user_text).morph_analyze()
            morph_count = len(morph_data)

            print(morph_data)
            print(morph_count)
            print(morph_count//3)
            if morph_count//3 == 1:
                with Session() as session:
                    morph_title = morph_data[0]
                    tasks = session.query(Task.id, Task.title, Task.description, Task.is_completed, Task.due_date, Task.category, Task.priority,  Task.created_at,).all()
                    for id_, title_, description_, is_completed_, due_date_, category_, priority_, created_at_ in tasks:
                        if morph_title == title_:
                            print("\n\nВы хотите завершить задачу, что описана снизу?")
                            status = "Завершено" if is_completed_ else "В процессе"
                            print(f"\n🔹 ID: {id_}\n📌 Заголовок: {title_}\n📝 Описание: {description_}\n📅 Дедлайн: {due_date_}\n🏷️  Категория: {category_}\n⭐ Приоритет: {priority_}\n📍 Статус: {status}\n")
                            
                            user_answer = input("Вы уверены, что хотите завершить эту задачу? ").lower()
                            agree = user_answer in task_intents["confirmation"]
                            
                            if agree:
                                new_task_data = Complited(
                                    id = id_,
                                    title = title_,
                                    description = description_,
                                    created_at = created_at_,
                                    due_date = due_date_,
                                    is_completed = True,
                                    priority = priority_,
                                    category = category_
                                )

                                session.add(new_task_data)
                                session.commit()

                            
                           
                
            


Function(input("Enter the text: ")).output()