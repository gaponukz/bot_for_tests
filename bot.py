from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from time import sleep
from os import system
from utils import parse_answers
from config import file_name
import json, sys, os
import xlsxwriter

class ParseAnswers(object):
    def __init__(self, show = False) -> None:
        options = Options()
        if not show: options.add_argument("--headless")
        self.driver = webdriver.Chrome(options = options)

    def login(self, username: str, password: str) -> None:
        self.driver.get("https://perevirkaznan.com/")
        self.driver.find_element_by_xpath('/html/body/nav/div/div/a').click()
        self.driver.find_element_by_xpath('//*[@id="q"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="qw"]').send_keys(password)
        sleep(1)
        self.driver.find_element_by_xpath('//*[@id="login"]/form/div[3]/label/span').click()
        self.driver.find_element_by_xpath('//*[@id="login"]/form/button').click()

    def parse(self, index = '1') -> dict:
        sleep(1)
        self.driver.find_element_by_css_selector('body > nav > div > div > div > div:nth-child(4) > a').click()
        self.driver.find_element_by_xpath(f'/html/body/section[2]/div/div/div[{index}]/div/div[2]/a').click()
        sleep(1)
        self.driver.find_element_by_css_selector('body > section.course-detail-page > div > div.course-rules-page__btns > a.btn.btn-blue-transparent.course-rules-page__btn').click()
        num = self.driver.current_url.split('/quiz/')[-1]

        return parse_answers(self.driver.page_source), num

    def close(self) -> None:
        self.driver.close()

if __name__ == "__main__":
    username = 'qwerty'
    password = '777777'
    epoch = 40
    PATH_TO_DATA = os.path.dirname(os.path.abspath(__file__)) + '\\data\\'

    for j in range(1, epoch + 1):
        os.mkdir(PATH_TO_DATA + str(j))
        for i in range(1, 20):
            try:
                parser = ParseAnswers()
                parser.login(username, password)
                data, num = parser.parse(index = str(i))
                parser.close()

                # for write json files
                # with open (PATH_TO_DATA + str(j) + '\\' + f'{num}.json', 'w') as f:
                #     f.write(json.dumps(data, indent = 4, sort_keys = True))
                
                workbook = xlsxwriter.Workbook(PATH_TO_DATA + str(j) + '\\' + f'{file_name[str(i)]}.xlsx') 
                worksheet = workbook.add_worksheet()
                
                row, column = 0, 0
                titles = ['Вопрос', 'Все ответи', 'Правильний ответ']
                for item in titles: 
                    worksheet.write(row, column, item) 
                    column += 1

                row = 1
                for item in data['data']:
                    column = 0
                    all_answers = ''
                    true_answer = ''

                    for answer in item['answers']:
                        all_answers += answer['title'] + '\n'
                        if answer['is_true_answer']:
                            true_answer = answer['title']

                    worksheet.write(row, column, item['title'])
                    worksheet.write(row, column + 1, all_answers)
                    worksheet.write(row, column + 2, true_answer)

                    row += 1

                workbook.close()

                print(f'Parsed {num} successfully')

            except Exception as error:
                print(error)
