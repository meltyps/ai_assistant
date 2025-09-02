import stanza 

nlp = stanza.Pipeline(lang="ru", processors="tokenize,pos,lemma")
'''
tokenize — разбивка на предложения и слова
pos — определение частей речи
lemma — определение леммы (нормальной формы
'''

doc = nlp("Привет, мама, меня зовут Солнце. Как дела?")

for sentence in doc.sentences:
    print("Новое предложение: ")
    for word in sentence.words:
        print(f"Слово: {word.text}")
'''
word.text	Исходное слово (токен)
word.lemma	Лемма (нормальная форма слова)
word.upos	Universal POS — универсальная часть речи (на англ.)
word.xpos	Языковая часть речи (специфическая для языка)
word.feats	Грамматические признаки (падеж, число, род и т.д.)
'''