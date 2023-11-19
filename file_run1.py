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

# This part scrapes the categories and their links
url = "https://www.tripadvisor.com/Attractions-g293995-Activities-c36-Riyadh_Riyadh_Province.html"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")  # Optional: Set the window size
chrome_driver_path = "C:/Users/areesha.mujahid/Desktop/chromedriver_win32"
service = Service(executable_path='./chromedriver_win32.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome()
# It navigates to the TripAdvisor URL and extracts category names and their associated links
driver.get(url)
html_source = driver.page_source
# The extracted data is stored in separate lists and then transformed into a DataFrame
# containing Category and Categories_link columns
soup = BeautifulSoup(html_source, 'html.parser')
job_elements = soup.find_all("a", class_="KoOWI")
csv_file_path = "tripadvisor_attractions.csv"
header = ["Category", "Places","Rating",'location','Phone','email']
category=[]
product=[]

Categories_link = []
places_link = []
extracted_number = ''
email = ''

for job_element in job_elements:
    categories = job_element.text
    category.append(categories )
    print(categories)
    categories_links = job_element['href']
    full_url = f"https://www.tripadvisor.com{categories_links}"
    Categories_link.append(full_url)
    time.sleep(4)




d1 = {'category': category, "Categories_link" : Categories_link }
df = pd.DataFrame.from_dict(d1)
print(df)
c1=[]
i=0
# Later, it iterates through each category's link to scrape subcategory details
for i in df.Categories_link:
    driver.get(i)
    time.sleep(4)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    job_elements2 = soup.find_all("div", class_="alPVI eNNhq PgLKC tnGGX")
    # for restaurant
    i = 0
# This part navigates to each category link and extracts subcategory names and their links
    for job_element2 in job_elements2:
        categoriess = job_element2.text
        print(categoriess)
        product.append(categoriess)
        links = job_element2.a['href']
        full_urll = f"https://www.tripadvisor.com{links}"
        places_link.append(full_urll)
        i=i+1
    c1.append(i)

print(c1)
print(category)
# It collects this information in lists and creates a DataFrame 'df2' containing Category, Name, and places_link
driver.get(full_url)
result_list = [s for n, s in zip(c1, category) for _ in range(n)]
print(result_list)
d1 = {'Category': result_list,'Name': product, "places_link" : places_link }
df2 = pd.DataFrame.from_dict(d1)
print(df2)
df2.to_csv('data.csv')



