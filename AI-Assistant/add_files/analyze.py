try: 
    from local_database.intents import task_intents
    import stanza
    import sqlalchemy
    from sqlalchemy.orm import sessionmaker
    from sqlTable import engine, Task
except ImportError:
    from add_files.local_database.intents import task_intents
    import stanza
    import sqlalchemy
    from sqlalchemy.orm import sessionmaker
    from add_files.sqlTable import engine, Task
# from add_files.local_database.intents import task_intents

class CommandAnalyzer:
    _nlp = stanza.Pipeline(lang="ru", processors="tokenize,pos,lemma", tokenize_no_ssplit=True)  
    _Session = sessionmaker(bind=engine)

    def __init__(self, user_text: str):
        self.user_text = user_text
        self.user_lemmas = self._text_to_lemmas(user_text)

    @classmethod
    def _text_to_lemmas(cls, text: str) -> set:
        """Преобразует текст в множество лемм."""
        doc = cls._nlp(text)
        return {word.lemma for sentence in doc.sentences for word in sentence.words}

    def analyze(self):
        for intents, phrases in task_intents.items():
            if any(phrase in self.user_text.lower() for phrase in phrases):
                return intents

            
    def morph_analyze(self):
        """Находит задачи с наибольшим количеством совпадений лемм."""
        matches = []  # список (title, description, count)
        max_count = -1

        with self._Session() as session:
            tasks = session.query(Task.title, Task.description).all()

            for title, description in tasks:
                task_lemmas = self._text_to_lemmas(f"{title} {description}")
                count = len(self.user_lemmas & task_lemmas)

                if count > max_count:
                    max_count = count
                    matches = [(title, description, count)]  # сбрасываем, если нашли лучше
                elif count == max_count:
                    matches.append((title, description, count))  # добавляем, если равны

        if not matches:
            print("❌ Похожих задач не найдено.")
            return None

        # Если совпадение одно — сразу возвращаем
        if len(matches) == 1:
            return matches[0]

        # Если совпадений несколько — показываем их и спрашиваем пользователя
        print("🔍 Найдено несколько совпадений:")
        for i, (title, desc, cnt) in enumerate(matches, start=1):
            print(f"\n{i}. 📌 {title}\n📝 {desc}\nСовпадений лемм: {cnt}")

        while True:
            choice = input("\nВведите номер задачи, которую нужно удалить (или 0, если ничего не удалять): ").strip()
            if choice.isdigit():
                choice = int(choice)
                if 0 <= choice <= len(matches):
                    break
            print("⚠ Введите корректный номер.")

        if choice == 0:
            return matches  # возвращаем все, ничего не удаляя
        else:
            removed = matches.pop(choice)
            print(f"❌ Задача '{removed[0]}' удалена из результатов.")
            return matches

'''           
"word"	word	Оригинальное слово из текста
"normal_form"	parsed.normal_form	Лемма — начальная форма слова. Например, у слова "шёл" будет "идти"
"part_of_speech"	str(parsed.tag.POS)	Часть речи: NOUN (существительное), VERB (глагол), ADJF (прилагательное) и т.д.
"tag"	str(parsed.tag)	Полный грамматический разбор: часть речи + род, число, падеж и др.
'''
            
#print(CommandAnalyzer(input("Enter the text: ")).analyze())
#print(CommandAnalyzer(input("Enter the text: ")).morph_analyze())
