from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium.webdriver.chrome.service import Service
import requests
import pandas as pd

START_URL = "https://en.wikipedia.org/w/index.php?title=List_of_brightest_stars_and_other_record_stars&oldid=1003217499"
service=Service(executable_path="C:/Users/Raghav/Desktop/WhiteHat/Python projects/Project 127/chromedriver.exe")

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=service,options=options)
browser.get(START_URL)
time.sleep(10)

scraped_data = []

def scrape_more_data(hyperlink):
    print(hyperlink)
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []

        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")

            for x in td_tags:
                try:
                    temp_list.append(x.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        scraped_data.append(temp_list)
    
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

stars_data = [] 

for i in range(0,len(scraped_data)): 
    Star_names = scraped_data[i][1] 
    Distance = scraped_data[i][3] 
    Mass = scraped_data[i][5] 
    Radius = scraped_data[i][6] 
    Lum = scraped_data[i][7] 
    required_data = [Star_names, Distance, Mass, Radius, Lum] 
    stars_data.append(required_data) 

print(stars_data)

# Define Header 
headers = ['Star_name','Distance','Mass','Radius','Luminosity']

# Define pandas DataFrame 
star_df_1 = pd.DataFrame(stars_data, columns=headers) 

#Convert to CSV 
star_df_1.to_csv('scraped_data.csv',index=True, index_label="id")