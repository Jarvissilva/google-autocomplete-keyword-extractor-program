import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 

options = Options() 
  
# this parameter tells Chrome that 
# it should be run without UI (Headless) 
options.headless = True
  
# initializing webdriver for Chrome with our options 
driver = webdriver.Chrome(options=options) 
alphabets = ['','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
main_keyword = ""
keywords_to_search = []

def save_to_excel(df):
    autocomplete_results_file = "autocomplete_results.xlsx"
    if os.path.isfile(autocomplete_results_file):
        existing_df = pd.read_excel(autocomplete_results_file)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(autocomplete_results_file, index=False)

def scrape_autocomplete_results():
    global main_keyword
    global keywords_to_search
    
    driver.get("https://www.google.com")
    
    try:
        while True:
            for letter in alphabets:
                keyword = main_keyword + " " + letter

                # Getting and searching the search bar
                search_bar = driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
                search_bar.click()
                time.sleep(2)
                search_bar.clear() 
                search_bar.send_keys(keyword)
                time.sleep(2)

                # Getting the autocomplete data 
                autocomplete_results_container = driver.find_element(By.XPATH,'//*[@id="Alh6id"]/div[1]/div/ul')
                autocomplete_results = autocomplete_results_container.find_elements(By.TAG_NAME, 'li')

                # Final autocomplete data 
                autocomplete_results_data = [result.text for result in autocomplete_results]
                keywords_to_search.extend(autocomplete_results_data)

            # Remove main_keyword from keywords_to_search
            keywords_to_search = [keyword for keyword in keywords_to_search if keyword != main_keyword]

            df = pd.DataFrame(keywords_to_search, columns=["Autocomplete Results"])
            save_to_excel(df)

            if keywords_to_search:
                main_keyword = keywords_to_search[0]
            else: 
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    driver.quit()

if __name__ == "__main__":
    scrape_autocomplete_results()
    print(keywords_to_search)
