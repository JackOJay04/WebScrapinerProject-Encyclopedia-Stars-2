#Step 1: Importing Files

#Used to parse
import selenium
#Used for web
from selenium import webdriver
#Setting browser
browser = webdriver.Edge()
from bs4 import BeautifulSoup
#Used to make the code sleep
import time
#Used for csv extensions
import csv

#Step 2: The Link

#Creating The Link
start_url = "https://en.wikipedia.org/wiki/Lists_of_stars"
#Setting Up The Link With Chrome
browser = webdriver.Edge("C:/Users/Jayan/WebScraper/msedgedriver.exe")
#Getting The Link Ready With Chrome
browser.get(start_url)

#Step 3: Info

def Scrape():
    #Setting Header Names
    Headers = ["Name", "Light Years From Earth", "Mass", "Stellar Magnitude", "Discovery Date", "Hyperlink"]
    #Setting Planet Data To Nothing
    Planet_Data = []
    #Opening The Browser Using BeautifulSoup And Then Parsing
    Soup = BeautifulSoup(browser.page_source, "html.parser")
    #Taking The Current Page/Website Number
    Current_Page_Num = int(Soup.find_all("Input", attrs = {"class", "Page_Num"})[0].get(["value"]))
    #Redirecting To Different Pages
    if Current_Page_Num < i:
        browser.find_element(By.XPATH, value = '//*[@id = primary_column]/footer/div/div/div/nav/span[2]/a').click()
    elif Current_Page_Num > i:
        browser.find_element(By.XPATH, value = '//*[@id = primary_column]/footer/div/div/div/nav/span[1]/a').click()
    else:
        break

    #Setting Header Names
    Headers = ["Name", "Light Years From Earth", "Mass", "Stellar Magnitude", "Discovery Date"]
    #Setting Planet Data To Nothing
    Planet_Data = []
    #Opening The Browser Using BeautifulSoup And Then Parsing
    Soup = BeautifulSoup(browser.page_source, "html.parser")
    #Finding All The Tags With Class And Exoplanet
    for UL_Tag in Soup.find_all("UL", attrs = {"class", "exoplanet"}):
        #Setting LI_Tags
        LI_Tags = UL_Tag.find_all("LI")
        #Setting temp_list To An Empty List
        temp_list = []
    #Checking HTML With EdgeDriver
        for Index, LI_Tags in enumerate(LI_Tags):
            #Sorting Names Into Alphabetical Order
            if Index == 0:
                temp_list.append(LI_Tags.find_all("a")[0].contents[0])
            else:
                try:
                    temp_list.append(LI_Tags.contents[0])
                except:
                    temp_list.append("")
            #Setting Hyperlink Tags
            Hyperlink_LI_Tag = LI_Tags[0]
            #Organizing Alphabettically
            temp_list.append("https://exoplanets.nasa.gov" + Hyperlink_LI_Tag.find_all("a", href = True)[0]["href"])
            #Updating Planet_Data With Collected Data
            Planet_Data.append(temp_list)

browser.find_element(By.XPATH, value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

print(f"Page {i} scraping completed")


New_Planet_Data = []

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
      
        soup = BeautifulSoup(page.content, "html.parser")

        temp_list = []

        for tr_tag in soup.find_all("tr", attrs={"class": "fact_row"}):
            td_tags = tr_tag.find_all("td")
          
            for td_tag in td_tags:
                try: 
                    temp_list.append(td_tag.find_all("div", attrs={"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        New_Planet_Data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

#Calling method

for index, data in enumerate(Planet_Data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink {index+1} is completed.")

print(New_Planet_Data[0:10])

Final_Planet_Data = []

for index, data in enumerate(Planet_Data):
    New_Planet_Data_Element = New_Planet_Data[index]
    New_Planet_Data_Element = [elem.replace("\n", "") for elem in New_Planet_Data_Element]
    New_Planet_Data_Element = New_Planet_Data_Element[:7]
    Final_Planet_Data.append(data + New_Planet_Data_Element)

with open("final.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(Headers)
        csvwriter.writerows(Final_Planet_Data)