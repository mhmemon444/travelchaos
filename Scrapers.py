from typing import List
from time import sleep
import numpy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager


CHROME_PATH = '/Users/danielraad/Desktop/chromedriver.exe'
HEATRHOW_DEPARTURES = 'https://www.heathrow.com/departures'
GATWICK_DEPARTURES = 'https://www.gatwickairport.com/flights/?type=departures'

class Scraper: 
    def __init__(self): 
        ''' Path to your chrome driver '''
        chromedriver_path = CHROME_PATH
        ''' Setting up the Selenium driver and directing Selenium to a specific website '''
        self.driver = webdriver.Chrome(service=Service(executable_path=chromedriver_path))


    def heathrow_departures(self) -> List[pd.DataFrame]: 
        dataframes = []

        driver = self.driver
        driver.get(HEATRHOW_DEPARTURES)

        ''' XPATH location for the time you wish to start collecting plane data from - on Heathrow Departures this is a drop down '''
        time_selector = Select(driver.find_element(By.XPATH, '//*[@id="airline-list-from-time"]'))
        time_selector.select_by_index(1)

        ''' the element for each separate terminal '''
        terminal2 = driver.find_element(By.XPATH, '//*[@id="flight-list-app"]/div/div[1]/div/form/div[2]/div/button[2]')
        terminal3 = driver.find_element(By.XPATH, '//*[@id="flight-list-app"]/div/div[1]/div/form/div[2]/div/button[3]')
        terminal4 = driver.find_element(By.XPATH, '//*[@id="flight-list-app"]/div/div[1]/div/form/div[2]/div/button[4]')
        terminal5 = driver.find_element(By.XPATH, '//*[@id="flight-list-app"]/div/div[1]/div/form/div[2]/div/button[5]')

        # terminals = [terminal2, terminal3, terminal4, terminal5]
        terminals = [terminal2]

        load_next = driver.find_element(By.XPATH, '//*[@id="flight-list-app"]/div/div[2]/div[2]/div/div[3]/button')
        columns = ['Time', 'Flight Number', 'Departing to', 'Airline', 'Terminal Number', 'Flight Status', 'Code Share flights']

        ''' go through and select each terminal, collecting all the data into DataFrames dependent on terminal  '''
        for terminal in terminals: 
            terminal_df = pd.DataFrame(columns=columns)
            driver.execute_script("arguments[0].click()", terminal)
            xp_sections = 'airline-listing-line-item'
            while(True): 
                sections = driver.find_elements(By.CLASS_NAME, xp_sections)
                for i, flight in enumerate(sections, 1): 
                    time = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[1]')
                    flight_num = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[2]/div[1]/div[1]')
                    departing_to = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[2]/div[1]/div[2]')
                    airline = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[2]/div[1]/div[3]')
                    terminal_num = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[2]/div[1]/div[4]')
                    flight_status = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[3]')
                    codeshare_flight = flight.find_element(By.XPATH, f'//*[@id="flight-list-app"]/div/div[2]/div[2]/div/a[{i}]/div[2]/div[2]')
                    terminal_df = terminal_df.append({'Time':time.text, 'Flight Number':flight_num.text, 'Departing to':departing_to.text, 'Airline':airline.text, 'Terminal Number':terminal_num.text, 'Flight Status':flight_status.text, 'Code Share flights':codeshare_flight.text}, ignore_index=True)
            

                ''' while load next is available, continue loading the data on the page '''
                if load_next.get_property('disabled') is True: 
                    dataframes.append(terminal_df)
                    break
                else: 
                    driver.execute_script("arguments[0].click()", load_next)


        return dataframes



    def gatwick_departures(self) -> List[pd.DataFrame]:
        dataframes = [] 
        driver = self.driver
        driver.get(GATWICK_DEPARTURES)

        later = driver.find_element(By.XPATH, '//*[@id="later-button"]')
        xp_sections = 'flight-info-row'
        while(True):
            sections = driver.find_elements(By.CLASS_NAME, xp_sections)
            for flight in sections: 
                print(flight.text)

            '''' TODO: think about how to find the :after tag '''
            print(later.get_attribute())
            if later.get_attribute('innerHTML').find('::after') != -1: 
                driver.execute_script("arguments[0].click()", later)
            else: 
                break 

        return dataframes

        



scraper = Scraper() 

# heathrow_flights_dfs: List[pd.DataFrame] = scraper.heathrow_departures()
# for frame in heathrow_flights_dfs: 
#     print(frame)

gatwick_flights_dfs: List[pd.DataFrame] = scraper.gatwick_departures()
for frame in gatwick_flights_dfs: 
    print(frame)