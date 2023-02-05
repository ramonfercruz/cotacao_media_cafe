import requests
import pandas as pd
from bs4 import BeautifulSoup

from constante import Constante


class ParseHtml:
    def __init__(self):
        constante = Constante()
        self.__url = constante.URL
        self.__parser = None
        self.__tables = None
        self.__months = []
        self.__column_name = ['dolar', 'real', 'quantidade']
        self.__title = None
        self.__subtitle = []
        self.__list_df = []

    def __request_html(self):
        page = requests.get(self.__url)
        self.__parser = BeautifulSoup(page.text, "html.parser")

    def __get_table(self):
        self.__tables = self.__parser.select('Table')

    def __get_months(self):
        for children in self.__tables[0].find_all('thead')[0].children:
            for i in children:
                try:
                    month = i.getText()
                    if month != 'Ano' and month != '\n':
                        self.__months.append(i.getText())
                except AttributeError:
                    pass

    def __get_data_frame(self):
        self.__get_months()
        for table in self.__tables:
            dict_year_values = {}
            for children in table.find_all('tbody')[0].children:
                for i in children:
                    try:
                        attrs = i.attrs
                        value = i.getText().strip()
                        if value != '' and value != '\n':
                            if attrs:
                                if attrs['class'][0] == 'r':
                                    value = i.getText().strip()
                                    if value != '':
                                        dict_year_values[year].append(value)
                            else:
                                year = value
                                dict_year_values.setdefault(year, [])

                    except AttributeError:
                        pass
            df = pd.DataFrame.from_dict(dict_year_values, orient='index')
            df.columns = self.__months
            self.__list_df.append(df)

    def __get_title(self):
        title = self.__parser.select('Title')[0]
        self.__title = title.getText()

    def __get_subtitle(self):
        for sub_title in self.__parser.select('H2'):
            sub_title = sub_title.getText()
            if not 'href' in sub_title and not 'pdf' in sub_title:
                self.__subtitle.append(sub_title)

    def process(self):
        self.__request_html()
        self.__get_table()
        self.__get_data_frame()
        self.__get_title()
        self.__get_subtitle()
        print("Dado dado coletado")


    def list_df(self):
        for i in range(len(self.__list_df)):
            yield self.__list_df[i], self.__subtitle[i], self.__title, self.__column_name[i]
