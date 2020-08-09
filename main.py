try:
    from os import system
    from time import sleep
    from bot import ParseAnswers as Bot
    from utils import parse_answers
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from threading import Thread
    import json, random
    import xlrd, xlsxwriter
    import easygui

except ImportError:
    print('Installation of some modules, please wait for a moment.')
    system('python -m pip install -r requirements.txt')

class AutomaticTest(Bot):
    def solve(self, index: int) -> None:
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath('/html/body/nav/div/div/div/div[4]/a').click()
        self.driver.find_element_by_xpath(f'/html/body/section[2]/div/div/div[{index}]/div/div[2]/a').click()
        sleep(random.choice([.5, .4]))
        try:
            self.driver.find_element_by_css_selector('body > section.course-detail-page > div > div.course-rules-page__btns > a.btn.btn-blue-transparent.course-rules-page__btn').click()
        except:
            print('Тест уже решен.'); return
        
        answers = parse_answers(self.driver.page_source)
        html = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        if not html.find('div', {'class': 'test__info-value'}).text == '3':
            print('Тест уже решен.'); return
        
        tests = html.find_all('div', {'class': 'test-item'})
        data = []

        for test in tests:
            data.append({
                'title': test.find('div', {'class': 'test-item__question'}).text,
                'answers': list(map(lambda x: str(x.text), test.find('div', {'class': 'test-item__answers-row'})\
                .find_all('div', {'class': 'test-item__answer'})))
            })

        for test in data:
            index_of_test = data.index(test) + 1
            try:
                self.driver.implicitly_wait(1)
                answer_tests = list(filter(lambda x: AutomaticTest.clean(x['title']) \
                    in AutomaticTest.clean(test['title']), answers['data']))[0]
                answer = list(filter(lambda x: x['is_true_answer'] == 1, answer_tests['answers']))
            except:
                element = self.driver.find_element_by_css_selector(f"#app-quiz > div > div.test__list > div:nth-child({index_of_test}) > div.test-item__answers > div > div:nth-child({random.choice([1, 2])}) > label > span")
                self.driver.execute_script("arguments[0].click()", element)

            index_of_correct = random.choice([1, 2]) if not answer else answer_tests['answers'].index(answer[0]) + 1

            result_element = self.driver.find_element_by_css_selector(f"#app-quiz > div > div.test__list > div:nth-child({index_of_test}) > div.test-item__answers > div > div:nth-child({index_of_correct}) > label > span")
            self.driver.execute_script("arguments[0].click()", result_element)

            sleep(random.choice([.1, .2, .3]))
        
        sleep(random.choice([2, 2.5, 3]))
    
    @staticmethod
    def clean(text: str) -> str:
        return text.replace('\t', ' ').replace('\n', ' ').strip()

def solve_test(index: int, username: str, password: str) -> None:
    bot = AutomaticTest(show = False)
    bot.login(username, password)
    bot.solve(index)
    bot.close()

def generate():
    i = 0
    while True:
        yield i, i + 1, i + 2
        i += 3

if __name__ == '__main__':
    wb = xlrd.open_workbook(easygui.fileopenbox())
    sheet, row = wb.sheet_by_index(0), 1
    users = []

    while True:
        try:
            username = sheet.cell_value(row, 1)
            password = sheet.cell_value(row, 2)
            users.append([username, password])
            row += 1
        except:
            break

    def solve_tests(username: str, password: str):
        index = 1
        while True:
            try:
                solve_test(
                    index = index,
                    username = username,
                    password = password
                )
                # print(f'Solve {index} test for {username}')
                index += 1
            except:
                break
    
    generator = generate()
    tests_solved = 0
    while True:
        try:
            one, two, three = generator.__next__()

            tread1 = Thread(target = solve_tests, args = (users[one][0], users[one][1]))
            tread2 = Thread(target = solve_tests, args = (users[two][0], users[two][1]))
            tread3 = Thread(target = solve_tests, args = (users[three][0], users[three][1]))
            
            tread1.start(); tread2.start(); tread3.start()
            tread3.join()

            tests_solved += 3
            
            print(f'{tests_solved}/{len(users)} аккаунтов прошло тесты.')
        
        except IndexError:
            break

        except:
            continue
