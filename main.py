from os import system

try:
    from bot import ParseAnswers as Bot
    from utils import parse_answers
    from selenium import webdriver
    from bs4 import BeautifulSoup
    from threading import Thread
    from datetime import datetime
    import json, random, time
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
        time.sleep(random.choice([.5, .4]))
        try:
            self.driver.find_element_by_css_selector('body > section.course-detail-page > div > div.course-rules-page__btns > a.btn.btn-blue-transparent.course-rules-page__btn').click()
        except:
            return print('Тест уже решен.')

        time_to_refresh = 0
        while (answers := parse_answers(self.driver.page_source)['data']) == []:
            self.driver.refresh()
            if time_to_refresh == 3:
                return
            
            time_to_refresh = time_to_refresh + 1
        
        html = BeautifulSoup(self.driver.page_source, 'html.parser')
        
        if not html.find('div', {'class': 'test__info-value'}).text == '3':
            return # print('Тест уже решен.')
        
        with open('solve_tests.js', 'r', encoding = 'utf-8') as script:
            self.driver.execute_script(script.read())
        
        time.sleep(random.choice([2, 2.5, 3]))
    
    @staticmethod
    def clean(text: str) -> str:
        return text.replace('\t', ' ').replace('\n', ' ').strip()

def generate():
    i = 0
    while True:
        yield i, i + 1, i + 2
        i += 3

if __name__ == '__main__':
    wb = xlrd.open_workbook(easygui.fileopenbox())
    sheet, row = wb.sheet_by_index(0), 1
    users, tests_solved = [], 0
    startTime = datetime.now()

    while True:
        try:
            username: str = sheet.cell_value(row, 1)
            password: str = sheet.cell_value(row, 2)
            users.append([username, password]); row += 1
        except: break

    def solve_tests(username: str, password: str):
        bot, index = AutomaticTest(show = False), 1
        bot.login(username, password)
        global tests_solved

        while True:
            try:
                bot.solve(index)
                index += 1 # print(f'Solve {index} test for {username}')

            except: break

        bot.close()
        tests_solved += 1
    
    generator = generate()

    while True:
        try:
            one, two, three = generator.__next__()

            tread1 = Thread(target = solve_tests, args = (users[one][0], users[one][1]))
            tread2 = Thread(target = solve_tests, args = (users[two][0], users[two][1]))
            tread3 = Thread(target = solve_tests, args = (users[three][0], users[three][1]))
            
            tread1.start(); tread2.start(); tread3.start()
            tread1.join(); tread2.join(); tread3.join()

            system('cls || clear')
            print(f'{tests_solved}/{len(users)} аккаунтов прошло тесты.')
        
        except IndexError: break
        except: continue
    
    # Find out time it took for a python script to complete execution
    print('Время за которое были выполнены все тесты', end = ' ')
    print(datetime.now() - startTime)
