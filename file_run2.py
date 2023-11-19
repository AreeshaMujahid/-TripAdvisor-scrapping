from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re
from urllib.parse import unquote
import pandas as pd
from itertools import zip_longest
import numpy as np

csv_file_path = 'path/to/your/file.csv'


df2 = pd.read_csv("C:/Users/areesha.mujahid/PycharmProjects/imagerecognition/venv/Scripts/data.csv")
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # Optional: Set the window size
chrome_driver_path = "C:/Users/areesha.mujahid/Desktop/chromedriver_win32"
service = Service(executable_path='./chromedriver_win32.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()

csv_file_path = "tripadvisor_attractions_final.csv"
header = ["Location",'Rating','Phone','Email']
Location=[]
Rating=[]
Phone=[]
Email=[]
dff1 = df2[['Name', 'Category']].copy()

with open(csv_file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    for i in df2.places_link:
            driver.get(i)
            print(i)
            time.sleep(3)
            html_source = driver.page_source
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            soup = BeautifulSoup(driver.page_source, 'html5lib')
            rating= soup.find_all("div", class_="biGQs _P fiohW hzzSG uuBRH")
            emph = soup.find_all('div', class_='ZhNYD')
            location = soup.find_all("button", class_="UikNM _G B- _S _W _T c G_ wSSLS wnNQG raEkE")
            for radiv1,epdiv2,lodiv3  in zip_longest(rating,emph,location):
               if epdiv2 is not None:
                  anchor_tags2 = epdiv2.find('a', string='Email')
               if epdiv2 is not None:
                   anchor_tags1 = epdiv2.find('a', string='Call')
               if lodiv3 is not None:
                   location = lodiv3.text

               else:
                   lodiv3 == 'NA'
                   location=lodiv3

               if radiv1 is not None:
                   rating = radiv1.text
               else:
                   rating == 'NA'
               if anchor_tags1 is not None:
                   c=anchor_tags1['href']
                   decoded_number = unquote(c)
                   # Extracting the digits using regex
                   extracted_number = re.sub(r'\D', '', decoded_number)

               else:
                   extracted_number='NA'

               if  anchor_tags2 is not None:
                   e=anchor_tags2['href']
                   email=e[7:]

               else:
                   email='NA'

            writer.writerow([location,rating, extracted_number, email])
dff2 = pd.read_csv("C:/Users/areesha.mujahid/PycharmProjects/imagerecognition/venv/Scripts/tripadvisor_attractions_final.csv")
dff2 = dff2[["Location",'Rating','Phone','Email']]
concatenated_df = pd.concat([dff1, dff2], axis=1)
concatenated_df=concatenated_df.replace('[]', 'NA')
concatenated_df=concatenated_df.fillna('NA')
concatenated_df.to_csv('final_trip.csv')
print('executed')