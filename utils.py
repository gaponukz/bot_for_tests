from json import JSONDecoder
import json

def write(filename: str, text: str) -> None:
    with open(filename, 'r') as filetext:
        filetext = filetext.read()

    with open(filename, 'w') as file:
        file.write(f'{filetext}\n{text}\n\n')

def parse_json(text: str, decoder = JSONDecoder()) -> str:
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result

            pos = match + index
        except ValueError:
            pos = match + 1

def parse_answers(html: str) -> dict:
    data, results = [], []

    for result in parse_json(html):
        data.append(result)

    json_data = ('{"data":' + '[{0}]'.format(", "\
        .join(list(map(lambda x: str(x), data)))) + "}")\
        .replace("'", '"').replace('\t','').replace('\n','')\
        .replace(',}',"}").replace(',]',"]").replace('None', '" "')\
        .replace('в"я', "в'я").replace('б"є', "б'є").replace('з"є', "з'є")\
        .replace('""', '"').replace('д"є', "д’є").replace('"рі', "'рі")\
        .replace('ок"', "ок'").replace('"Во', "'Во").replace('аз"', "аз'")\
        .replace("'Вогн", '"Вогн').replace("обок'", 'обок"').replace("газ'", 'газ"')\
        .replace("Газ'", 'Газ"').replace('"Поп', '"Поп').replace("динок'", 'динок"')\
        .replace('"теплого ящика"', "'теплого ящика'").replace("'рідк", '"рідк')\
        .replace("випадок'", 'випадок"').replace('п"ять', "п'ять")\
        .replace('здоров"ю', "здоров'ю").replace('"кавової гущі"', "'кавової гущі'")\
        .replace("'Водіями", '"Водіями').replace("'Ворота", '"Ворота')\
        .replace('"Про охорону праці"', "'Про охорону праці'")\
        .replace("Пісок'", 'Пісок"').replace("Порошок'", 'Порошок"')\
        .replace("'Вод", '"Вод').replace("розеток'", 'розеток"')\
        .replace("жінок'", 'жінок"').replace("виток'", 'виток"')\
        .replace("шпонок'", 'шпонок"').replace("раз'", 'раз"')\
        .replace("касок'", 'касок"').replace("заглушок'", 'заглушок"')\
        .replace("установок'", 'установок"').replace('"НВ"', "'НВ'")\
        .replace('"НЗ"', "'НЗ'").replace("стулок'", 'стулок"')\
        .replace("виїмок'", 'виїмок"').replace("зв'язок'", 'зв\'язок"')\
        .replace("замок'", 'замок"').replace('"Вогненебезпечно. Газ"', 'Вогненебезпечно. Газ"')\
        .replace("гущі'", 'гущі"').replace("'рік", '"рік').replace("'Вони", '"Вони')\
        .replace("задирок'", 'задирок"').replace("накладок'", 'накладок"')\
        .replace("рукавичок'", 'рукавичок"').replace('пред"являються', "пред'являються")\
        .replace("'Вологі", '"Вологі').replace("площадок'", 'площадок"')\
        .replace("бирок'", 'бирок"').replace("зв’язок'", 'зв’язок"')\
        .replace('"Правил', "'Правил").replace('вачів"', "вачів'")\
        .replace("'Прави", '"Прави')

    try:
        data = json.loads(json_data)
    except:
        # print(json_data)
        return {
            'data': []
        }
    
    for item in data['data']:
        answers = []

        try:
            item['answers']
        except:
            answers.append({
                'title': '',
                'is_true_answer': False,
            })
        else:
            for answer in item['answers']:
                answers.append({"title": answer['title'], \
                    "is_true_answer": answer['value']})
        try:
            results.append({
                "id": item['id'],
                "title": item['title'],
                "answers": answers
            })
        except:
            break

    return {
        "data": results
    }
