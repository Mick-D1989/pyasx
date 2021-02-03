import requests
from selenium import webdriver
from bs4 import BeautifulSoup
from pyasx.utils.utils import *


class Ticker:
    def __init__(self, tick):
        self.tick = tick
        self.history = None
        self.income_statement = None
        self.balance_sheet = None
        self.cash_flow = None
        self._url_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/50.0.2661.102 Safari/537.36'}
        self._window_options = ['--headless',
                                '--window-size=1920,1480',
                                '--no-sandbox',
                                '--disable-dev-shm-usage',
                                '--start-maximized']  # default to suppress window from opening

    def get_history(self, **kwargs):
        period = kwargs['period'] if 'period' in kwargs else '1y'
        interval = kwargs['interval'] if 'interval' in kwargs else '1d'
        start = kwargs['start'] if 'start' in kwargs else None
        end = kwargs['end'] if 'end' in kwargs else None

        base_url = 'https://query1.finance.yahoo.com/v8/finance/chart/'
        url = f'{base_url}{self.tick.upper()}'
        params = {
            'range': period.lower(),
            'interval': interval.lower()}

        # TODO: add logic to handle conditionals for start & end dates - also needs to override the periods if user
        #       selects

        data = requests.get(url=url, params=params, headers=self._url_headers).json()
        self.history = json_to_df(data)
        return data

    def get_financials(self, fin_type='financials'):
        base_url = 'https://finance.yahoo.com/quote/'
        url = f'{base_url}{self.tick.upper()}/{fin_type}'
        options = webdriver.ChromeOptions()
        for arg in self._window_options:
            options.add_argument(arg)
            # TODO: need to figure out why headless mode stops click() from working
            #  Change to options=options for headless mode
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        # Yahoo used react, so have to manually expand rows before reading HTML
        driver.find_element_by_xpath('//*[@id="Col1-1-Financials-Proxy"]/section/div[2]/button').click()

        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')
        driver.quit()

        features = soup.find_all('div', class_='D(tbr)')
        headers = []
        temp_list = []
        final = []
        index = 0
        # create headers
        for item in features[0].find_all('div', class_='Fw(b)'):
            headers.append(item.text)
        # statement contents
        while index <= len(features) - 1:
            # filter for each line of the statement
            temp = features[index].find_all('div', class_='D(tbc)')
            for line in temp:
                # each item adding to a temporary list
                temp_list.append(line.text)
            # temp_list added to final list
            final.append(temp_list)
            # clear temp_list
            temp_list = []
            index += 1
        df = pd.DataFrame(final[1:])
        df.columns = headers
        df = df_to_numeric(df)
        return df

    def get_statistics(self):
        url = f'https://finance.yahoo.com/quote/{self.tick}/key-statistics'
        req = requests.get(url)

        soup = BeautifulSoup(req.text, 'lxml')
        tables = soup.find_all('tbody')
        row_data = {}
        for table_cnt in range(len(tables) - 1):
            row = tables[table_cnt].find_all('tr')
            for row_cnt in range(len(row) - 1):
                data = row[row_cnt].find_all('td')
                row_data[data[0].text] = data[1].text
        return pd.DataFrame(row_data, index=[0])


# TODO: this whole bit
class SaveLoad(Ticker):
    def save(self):
        # Concatenate DFs and save as JSON
        pass

    def load(self):
        # Load data for JSON into object
        pass
